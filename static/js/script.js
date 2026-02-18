document.addEventListener("DOMContentLoaded", () => {
    // Sélection des nouveaux IDs du HTML
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const processBtn = document.getElementById("process-btn");
    const uploadArea = document.getElementById("uploadArea");
    const resultsArea = document.getElementById("resultsArea");

    // Déclenche l'explorateur de fichiers au clic sur la zone
    dropZone.addEventListener("click", () => fileInput.click());

    // Affichage du nom du fichier sélectionné
    fileInput.addEventListener("change", () => {
        if (fileInput.files.length) {
            const fileName = fileInput.files[0].name.toUpperCase();
            // On met à jour le texte dans la zone d'upload pour confirmer la sélection
            dropZone.querySelector("p").textContent = `FICHIER PRÊT : ${fileName}`;
            dropZone.querySelector("p").style.color = "var(--neon)";
            dropZone.style.borderColor = "var(--neon)";
        }
    });

    // Gestion de l'envoi du fichier (Action du bouton PROCESS START)
    processBtn.addEventListener("click", function(e) {
        if (!fileInput.files.length) {
            alert("Veuillez d'abord sélectionner un fichier.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        // Changement d'état du bouton
        processBtn.textContent = "PROCESSING CORE...";
        processBtn.classList.add("loading");

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === "success") {
                // Bascule de l'interface : Accueil -> Dashboard
                uploadArea.style.display = "none";
                resultsArea.style.display = "block";

                // Mise à jour des statistiques du moteur Pandas
                document.getElementById("res-rows").textContent = data.stats.rows_after;
                document.getElementById("res-dups").textContent = `-${data.stats.duplicates_removed}`;
                document.getElementById("res-outliers").textContent = data.stats.outliers_found;
                document.getElementById("res-cols").textContent = data.stats.cols_after;

                document.getElementById("t-rows-prev").textContent = data.stats.rows_before;
                document.getElementById("t-nulls-prev").textContent = data.stats.nulls_before;

                // Configuration du lien de téléchargement
                document.getElementById("downloadLink").href = `/download/${data.filename}`;
            } else {
                alert("Erreur lors du traitement : " + (data.message || "Fichier invalide"));
                processBtn.textContent = "PROCESS START";
                processBtn.classList.remove("loading");
            }
        })
        .catch(err => {
            console.error("Erreur Fetch:", err);
            alert("Erreur de connexion au serveur.");
            processBtn.textContent = "PROCESS START";
        });
    });
});