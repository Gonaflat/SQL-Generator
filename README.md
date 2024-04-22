# SQL-Generator
This project was built on the GPT-3-turbo model from OpenAI. Vector search was implemented using Embeddings (text-embedding-3-small model) and Faiss (Facebook model). The implementation of the project can be seen on a deployed FastAPI server. Further instructions can be found below.

The first step is to go to your IDE and set up a virtual environment. For Windows users:
1. Open Command Prompt (cmd) or PowerShell.
2. Navigate to the directory where you want to create the virtual environment using the `cd` command: `cd path\to\directory`
3. Execute the following command to create the virtual environment: `python -m venv environment_name`

For macOS and Linux users:
1. Open a terminal.
2. Navigate to the directory where you want to create the virtual environment: `cd path/to/directory`
3. Execute the following command: `python3 -m venv environment_name`

Step 3: Activating the Virtual Environment
After creating the virtual environment, you need to activate it to start using it.

For Windows:
In Command Prompt or PowerShell, run: environment_name\Scripts\activate

For macOS and Linux:
In the terminal, run: source environment_name/bin/activate

4. The next step is to create a .env file at the root of your project. Inside it, enter your Open_api_key as shown in the picture.

![image](https://github.com/Gonaflat/SQL-Generator/assets/127900470/648e6ddd-2d6f-4327-a6da-06082c1b4cdd)

5. Please make sure that you have access to GPT-3.5-turbo, text-embedding-3-small.

You need to visit the OpenAI API website and on the left side, you will find tabs describing your profile, API keys, and so on. The tab you need is called 'Settings'. By navigating to it, you should go to the 'Limits' tab, and to add models, click 'Edit' and select GPT-3.5-turbo, text-embedding-3-small from the list.

![image](https://github.com/Gonaflat/SQL-Generator/assets/127900470/e0530709-5eb7-4486-8947-8d3681f25f30)

6. Installing necessary libraries. I have included a requirements.txt file in this repository, where you can find the versions of the libraries used in this project.
You can simply copy and execute the command in the terminal: pip install.
Regarding the Faiss library, it is very important to specify the correct version; copy it from the requirements.*   

7. In this project, I include the 'Static' directory, which contains HTML, CSS, and JS files for the visual component of the server. There is also a main.py file with FastAPI settings, as well as a model.py file containing the model.
8.To start the server, enter the command in the terminal: uvicorn main:app --reload and follow the instructions. You will need to enter the following command in the address bar (should look something like that): http://127.0.0.1:8000/static/index.html
9. And here you go, You can enter your request and receive a working SQL query.
