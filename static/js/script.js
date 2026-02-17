document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const dropZone = document.getElementById("dropZone");

    dropZone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length) {
            document.getElementById("fileNameDisplay").textContent = fileInput.files[0].name.toUpperCase();
            document.getElementById("fileNameDisplay").style.color = "var(--neon)";
        }
    });

    form.addEventListener("submit", function(e) {
        e.preventDefault();
        const btn = document.getElementById("submitBtn");
        btn.textContent = "PROCESSING CORE...";

        fetch("/upload", { method: "POST", body: new FormData(this) })
            .then(res => res.json())
            .then(data => {
                if(data.status === "success") {
                    document.getElementById("uploadSection").style.display = "none";
                    document.getElementById("resultsArea").style.display = "block";
                    document.getElementById("mainCard").style.maxWidth = "650px";

                    document.getElementById("res-rows").textContent = data.stats.rows_after;
                    document.getElementById("res-dups").textContent = `-${data.stats.duplicates_removed}`;
                    document.getElementById("res-outliers").textContent = data.stats.outliers_found;
                    document.getElementById("res-cols").textContent = data.stats.cols_after;

                    document.getElementById("t-rows-prev").textContent = data.stats.rows_before;
                    document.getElementById("t-nulls-prev").textContent = data.stats.nulls_before;
                    document.getElementById("downloadLink").href = `/download/${data.filename}`;
                }
            });
    });
});