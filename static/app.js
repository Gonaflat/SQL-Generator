function highlightBlueKeywords(sql) {
    const keywords = ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE'];
    let regex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'gi');
    return sql.replace(regex, '<span class="highlight-blue">$1</span>');
}

document.getElementById('queryForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('queryInput').value;
    axios.post('/generate-sql/', { text: query })
        .then(function(response) {
            const sqlElement = document.getElementById('sqlOutput');
            sqlElement.innerHTML = highlightBlueKeywords(response.data.sql_query);
            hljs.highlightBlock(sqlElement);
        })
        .catch(function(error) {
            console.error('Error:', error);
        });
});

document.getElementById('queryInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('queryForm').dispatchEvent(new Event('submit', {cancelable: true}));
    }
});
