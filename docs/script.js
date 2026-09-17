const runBtn = document.getElementById('runBtn');
const refreshBtn = document.getElementById('refreshBtn');
const statusEl = document.getElementById('status');
const logsEl = document.getElementById('logs');

async function fetchJSON(url) {
    const res = await fetch(url);
    return res.json();
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
        const [inputData, outputData, logs] = await Promise.all([
            fetchJSON('/api/input'),
            fetchJSON('/api/output'),
            fetchJSON('/api/logs')
        ]);
        renderTable('inputTable', inputData);
        renderTable('outputTable', outputData);
        logsEl.textContent = logs.logs || 'No logs yet';
    } catch (e) {
        statusEl.textContent = 'Error loading data';
        console.error(e);
    }
}

async function runPipeline() {
    statusEl.textContent = 'Running...';
    runBtn.disabled = true;
    try {
        const res = await fetch('/api/run', { method: 'POST' });
        const data = await res.json();
        statusEl.textContent = data.message || 'Done';
        await loadData();
    } catch (e) {
        statusEl.textContent = 'Error running pipeline';
        console.error(e);
    } finally {
        runBtn.disabled = false;
    }
}

runBtn.addEventListener('click', runPipeline);
refreshBtn.addEventListener('click', loadData);

loadData();
setInterval(loadData, 5000);
