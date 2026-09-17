const runBtn = document.getElementById('runBtn');
const refreshBtn = document.getElementById('refreshBtn');
const statusEl = document.getElementById('status');
const logsEl = document.getElementById('logs');

runBtn.disabled = true;
statusEl.textContent = 'Run Pipeline requires local Flask server';

const REPO = 'jeyamalinimcse29-max/python-data-processing-pipeline';
const BRANCH = 'master';
const raw = (path) => `https://raw.githubusercontent.com/${REPO}/${BRANCH}/${path}`;

function parseCSV(text) {
    const lines = text.trim().split(/\r?\n/);
    if (lines.length < 2) return [];
    const headers = lines[0].split(',').map(h => h.trim());
    return lines.slice(1).map(line => {
        const values = line.split(',');
        const obj = {};
        headers.forEach((h,i) => obj[h] = values[i] ? values[i].trim() : '');
        return obj;
    });
}

function renderTable(tableId, data) {
    const table = document.getElementById(tableId);
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');
    thead.innerHTML = '';
    tbody.innerHTML = '';
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="100%">No data</td></tr>';
        return;
    }
    const headers = Object.keys(data[0]);
    const trHead = document.createElement('tr');
    headers.forEach(h => {
        const th = document.createElement('th');
        th.textContent = h;
        trHead.appendChild(th);
    });
    thead.appendChild(trHead);
    data.forEach(row => {
        const tr = document.createElement('tr');
        headers.forEach(h => {
            const td = document.createElement('td');
            td.textContent = row[h];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

async function loadData() {
    try {
        const [inputText, outputText] = await Promise.all([
            fetch(raw('input.csv')).then(r => r.text()),
            fetch(raw('output.csv')).then(r => r.text())
        ]);
        const inputData = parseCSV(inputText);
        const outputData = parseCSV(outputText);
        renderTable('inputTable', inputData);
        renderTable('outputTable', outputData);
        logsEl.textContent = 'Static GitHub Pages view. Run Pipeline is available only on local Flask server at http://localhost:5000';
        statusEl.textContent = '';
    } catch (e) {
        statusEl.textContent = 'Error loading data';
        console.error(e);
    }
}

async function runPipeline() {
    statusEl.textContent = 'Run Pipeline is only available on local Flask server';
}

runBtn.addEventListener('click', runPipeline);
refreshBtn.addEventListener('click', loadData);

loadData();
setInterval(loadData, 5000);
