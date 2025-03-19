async function fetchSummaries() {
    const sources = document.getElementById('sources').value.split(',').map(s => s.trim());
    const response = await fetch('/summarize_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sources: sources })
    });

    const summaries = await response.json();
    const summariesDiv = document.getElementById('summaries');
    summariesDiv.innerHTML = '';

    summaries.forEach(summary => {
        const summaryDiv = document.createElement('div');
        summaryDiv.classList.add('summary');
        summaryDiv.innerHTML = `<h3>${summary.source}</h3><p>${summary.summary}</p>`;
        summariesDiv.appendChild(summaryDiv);
    });
}

async function chatWithAI() {
    const article = document.getElementById('article').value;
    const question = document.getElementById('question').value;

    const response = await fetch('/chat_with_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ article: article, question: question })
    });

    const chatResponse = await response.json();
    document.getElementById('chat-response').innerHTML = `<p>${chatResponse.answer}</p>`;
}