document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const fileInput = document.getElementById("fileInput").files[0];

    if (!fileInput) {
        alert("Please upload an audio file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput);

    try {
        const response = await fetch("http://127.0.0.1:8000/predict/", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        document.getElementById("result").innerHTML = 
            `<p>Transcript: ${result.transcript}</p>
             <p>Prediction: ${result.prediction}</p>`;
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to get prediction. Make sure the backend is running.");
    }
});
