document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById('file-input');
    const processBtn = document.getElementById('process-btn');
    const dropZone = document.getElementById('drop-zone');
    const historyBtn = document.getElementById('viewHistoryBtn');
    const historyList = document.getElementById('historyList');

    dropZone.onclick = () => fileInput.click();

    processBtn.onclick = async () => {
        if (!fileInput.files[0]) return alert("SÉLECTIONNEZ UN FICHIER");

        // Animation Barre
        const progContainer = document.getElementById('progressContainer');
        const progBar = document.getElementById('progressBar');
        progContainer.style.display = "block";
        processBtn.style.display = "none";

        let progress = 0;
        const interval = setInterval(() => {
            progress += 15;
            if (progress <= 90) progBar.style.width = progress + "%";
        }, 200);

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/upload', { method: 'POST', body: formData });
            if (!response.ok) throw new Error();

            progBar.style.width = "100%";
            clearInterval(interval);

            // Update Stats
            document.getElementById('res-rows').textContent = response.headers.get("X-Stats-Rows");
            document.getElementById('res-dups').textContent = response.headers.get("X-Stats-Dups");
            document.getElementById('res-outliers').textContent = response.headers.get("X-Stats-Outliers");
            document.getElementById('res-cols').textContent = response.headers.get("X-Stats-Cols");

            // File Link
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const dl = document.getElementById('downloadLink');
            dl.href = url;
            dl.download = "NEXUS_CLEANED.xlsx";

            setTimeout(() => {
                document.getElementById('uploadArea').style.display = "none";
                document.getElementById('resultsArea').style.display = "block";
            }, 500);

        } catch (e) {
            alert("ERREUR MOTEUR");
            location.reload();
        }
    };

    historyBtn.onclick = async () => {
        const res = await fetch('/history');
        const data = await res.json();
        historyList.innerHTML = data.history.map(item => `
            <div style="padding:8px; border-bottom:1px solid #00f2ff11; font-size:0.75rem; color:#fff;">
                <b style="color:#00f2ff">${item.filename}</b> (${item.date})<br>
                Lignes: ${item.rows_in} → ${item.rows_out} | Erreurs: ${item.outliers}
            </div>
        `).join('');
        document.getElementById('historySection').style.display = "block";
    };
});