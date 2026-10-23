
const signatureInput = document.getElementById("signature");
const fileLabel = document.getElementById("file-label");
const uploadForm = document.querySelector("form");
const submitButton = document.querySelector(".primary-button");

signatureInput.addEventListener("change", function () {
    if (this.files.length > 0) {
        fileLabel.textContent = this.files[0].name;
    } else {
        fileLabel.textContent = "Choose a signature image";
    }
});

uploadForm.addEventListener("submit", function () {
    submitButton.textContent = "Comparing signatures...";
    submitButton.disabled = true;
});
