from openai import OpenAI
import os
from dotenv import load_dotenv
import torch
import faiss
import numpy as np

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
load_dotenv()
client = OpenAI()
table_descriptions = {
    "customers": """
        Table Name: Customers
        Description: Stores information about customers including unique identifier, name, age, and contact information. Used for tracking individual customer details and can be joined with the Orders table to view complete order histories.
        Fields:
            customer_id - INT, primary key, unique, not null, Unique identifier for each customer.
            name - VARCHAR(255), not null, Full name of the customer.
            age - INT, Age of the customer.
            email - VARCHAR(255), unique, Email address of the customer.
            registration_date - DATE, The date on which the customer was registered.
        Relationships:
            Joined with Orders on customer_id to link customers with their orders.
    """,

    "orders": """
        Table Name: Orders
        Description: Contains records of orders placed by customers, linked to the Customers table by customer_id. Includes details such as order date and total amount. Can be joined with OrderDetails to retrieve detailed items of each order.
        Fields:
            order_id - INT, primary key, unique, not null, Unique identifier for each order.
            customer_id - INT, foreign key, not null, References customer_id in the Customers table.
            order_date - DATE, not null, The date on which the order was placed.
            amount - DECIMAL(10,2), not null, Total amount of the order.
        Relationships:
            Joined with OrderDetails on order_id to provide a complete breakdown of each order.
    """,

    "order_details": """
        Table Name: OrderDetails
        Description: Provides a detailed list of items for each order, including product ID, quantity, and price per unit. Essential for generating detailed receipts and can be joined with the Products table for comprehensive product descriptions.
        Fields:
            order_detail_id - INT, primary key, unique, not null, Unique identifier for each order detail entry.
            order_id - INT, foreign key, not null, References order_id in the Orders table.
            product_id - INT, foreign key, not null, References product_id in the Products table.
            quantity - INT, not null, Quantity of the product ordered.
            price_per_unit - DECIMAL(10,2), not null, Price per unit of the product.
        Relationships:
            Joined with Products on product_id to retrieve detailed product information.
    """,

    "products": """
        Table Name: Products
        Description: Maintains information about products available for ordering, including product name, description, and current price. Frequently joined with OrderDetails for order reporting and analytics.
        Fields:
            product_id - INT, primary key, unique, not null, Unique identifier for each product.
            product_name - VARCHAR(255), not null, Name of the product.
            description - TEXT, Detailed description of the product.
            price - DECIMAL(10,2), not null, Current price of the product.
        Relationships:
            Information used in conjunction with OrderDetails to provide context for each ordered item.
    """
}

def get_embedding(table_descriptions, model = "text-embedding-3-small"):
    embeddings = {}
    for table_name, description in table_descriptions.items():
        response = client.embeddings.create(
        input = description, model=model).data[0].embedding
        embeddings[table_name] = response
    return embeddings

embeddings = get_embedding(table_descriptions)

def setup_faiss_index(embeddings):
    dimension = len(next(iter(embeddings.values())))
    index = faiss.IndexFlatL2(dimension)
    vectors = np.array(list(embeddings.values()))
    index.add(vectors)
    return index

index = setup_faiss_index(embeddings)

def vector_search(query, embeddings, index, table_names, top_n=4):
    response = client.embeddings.create(
        input = query, model = "text-embedding-3-small").data[0].embedding
    query_vector = np.atleast_2d(response)
    D, I = index.search(query_vector, top_n)
    best_match_tables = [table_names[idx] for idx in I[0]] if I.size > 0 else ['No matching tables found']
    return best_match_tables


def generate_sql(query, table_names):
    formatted_tables = ", ".join(table_names)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
      "role": "system",
      "content": f"Given the following SQL tables {formatted_tables}, your job is to write queries given a user’s request {query}"
    },
  ],
  temperature=0.7,
  max_tokens=150,
  top_p=1
)
    sql_query = response.choices[0].message.content
    return sql_query


