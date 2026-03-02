document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const processBtn = document.getElementById('process-btn');
    const iqrSlider = document.getElementById('iqr-threshold');

    // Navigation entre onglets
    window.showTab = (id) => {
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        event.currentTarget.classList.add('active');
        if(id === 'history-tab') loadHistory();
    };

    // UI Events
    iqrSlider.oninput = (e) => document.getElementById('iqr-val').innerText = e.target.value;
    dropZone.onclick = () => fileInput.click();
    fileInput.onchange = () => { if(fileInput.files[0]) dropZone.innerText = fileInput.files[0].name; };

    // API Call
    processBtn.onclick = async () => {
        if(!fileInput.files[0]) return alert("Fichier manquant");
        processBtn.innerText = "PROCESSING...";

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('impute_method', document.getElementById('impute-method').value);
        formData.append('iqr_threshold', iqrSlider.value);
        formData.append('force_int', document.getElementById('force-int').checked);

        const res = await fetch('/upload', { method: 'POST', body: formData });
        const data = await res.json();

        document.getElementById('uploadArea').style.display = 'none';
        document.getElementById('resultsArea').style.display = 'block';
        document.getElementById('res-rows').innerText = data.stats.rows;
        document.getElementById('res-outliers').innerText = data.stats.outliers;

        // Preview Table
        const thead = document.getElementById('thead');
        const tbody = document.getElementById('tbody');
        thead.innerHTML = "<tr>" + Object.keys(data.preview[0]).map(k => `<th>${k}</th>`).join('') + "</tr>";
        tbody.innerHTML = data.preview.map(row =>
            "<tr>" + Object.values(row).map(v => `<td>${v ?? 'NaN'}</td>`).join('') + "</tr>"
        ).join('');
    };
});

async function loadHistory() {
    const res = await fetch('/history');
    const data = await res.json();
    document.getElementById('historyList').innerHTML = data.history.map(h => `
        <div style="padding:10px; border-bottom:1px solid #333">📁 <b>${h.filename}</b> | ${h.rows_out} lignes | ${h.date}</div>
    `).join('');
}