document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const dropZone = document.getElementById("dropZone");
    const fileNameDisplay = document.getElementById("fileName");
    const submitBtn = document.getElementById("submitBtn");
    const statusText = document.getElementById("statusText");
    const statusBar = document.querySelector(".status-bar");
    const btnText = document.querySelector(".btn-text");

    // Click sur la zone déclenche l'input caché
    dropZone.addEventListener("click", () => fileInput.click());

    // Gestion du changement de fichier via input classique
    fileInput.addEventListener("change", function() {
        if (this.files.length) {
            updateFileInfo(this.files[0].name);
        }
    });

    // Gestion du Drag & Drop
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("active");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("active");
    });

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
        statusBar.className = "status-bar"; // Reset status
        statusBar.querySelector(".status-dot").style.background = "#00f2ff"; // Cyan ready
    }

    // Gestion de la soumission
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        if (!fileInput.files.length) {
            statusText.textContent = "Erreur : Aucun fichier sélectionné";
            statusText.style.color = "#ff4444";
            return;
        }

        // Interface en mode chargement
        setLoading(true);

        let formData = new FormData(this);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error("Erreur réseau");
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

            // Succès
            setLoading(false);
            statusText.textContent = "Nettoyage terminé. Téléchargement lancé.";
            statusBar.classList.add("success");
        })
        .catch(error => {
            setLoading(false);
            statusText.textContent = "Erreur lors du traitement.";
            console.error("Error:", error);
        });
    });

    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.textContent = "Traitement en cours...";
            statusText.textContent = "Connexion au noyau de données...";
            statusBar.className = "status-bar processing";
        } else {
            submitBtn.disabled = false;
            btnText.textContent = "Initialiser le Nettoyage";
        }
    }
});