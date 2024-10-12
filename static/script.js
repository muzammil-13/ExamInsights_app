// static/script.js
document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = document.getElementById('exam-paper').files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        const results = await response.json();
        displayResults(results);
    } catch (error) {
        console.error('Error:', error);
    }
});

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <h2>Analysis Results</h2>
        <p>Total Questions: ${results.question_count}</p>
        <h3>Frequent Topics:</h3>
        <ul>
            ${results.frequent_topics.map(([topic, count]) => `<li>${topic}: ${count}</li>`).join('')}
        </ul>
    `;
}