document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const dropZone = document.getElementById("dropZone");
    const fileNameDisplay = document.getElementById("fileName");
    const submitBtn = document.getElementById("submitBtn");
    const statusText = document.getElementById("statusText");
    const statusBar = document.querySelector(".status-bar");
    const btnText = document.querySelector(".btn-text");

    let isProcessing = false;

    dropZone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", function() {
        if (this.files.length) updateFileInfo(this.files[0].name);
    });

    dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("active"); });
    dropZone.addEventListener("dragleave", () => dropZone.classList.remove("active"));
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("active");
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            updateFileInfo(e.dataTransfer.files[0].name);
        }
    });

    function updateFileInfo(name) {
        fileNameDisplay.textContent = `Fichier détecté : ${name}`;
        statusText.textContent = "Fichier prêt pour l'analyse";
        statusBar.classList.remove("processing", "success", "ready");
        statusBar.classList.add("ready");
    }

    form.addEventListener("submit", function(e) {
        e.preventDefault();
        if (isProcessing) return;
        if (!fileInput.files.length) {
            statusText.textContent = "Erreur : Aucun fichier sélectionné";
            statusText.style.color = "#ff4444";
            return;
        }

        isProcessing = true;
        setLoading(true);

        let formData = new FormData(this);

        fetch("/upload", { method: "POST", body: formData })
            .then(async response => {
                if (!response.ok) {
                    const err = await response.text();
                    throw new Error(err);
                }
                return response.blob();
            })
            .then(blob => {
                let url = window.URL.createObjectURL(blob);
                let a = document.createElement("a");
                a.href = url;
                a.download = "cleaned_data.csv";
                document.body.appendChild(a);
                a.click();
                a.remove();

                setLoading(false);
                statusText.textContent = "Nettoyage terminé. Téléchargement lancé.";
                statusBar.classList.add("success");
                fileInput.value = "";
                fileNameDisplay.textContent = "";
            })
            .catch(error => {
                setLoading(false);
                statusText.textContent = error.message || "Erreur lors du traitement.";
                console.error("Error:", error);
            })
            .finally(() => { isProcessing = false; });
    });

    function setLoading(isLoading) {
        statusBar.classList.remove("processing", "success", "ready");
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.textContent = "Traitement en cours...";
            statusText.textContent = "Connexion au noyau de données...";
            statusBar.classList.add("processing");
        } else {
            submitBtn.disabled = false;
            btnText.textContent = "Initialiser le Nettoyage";
            statusBar.classList.add("ready");
        }
    }
});
