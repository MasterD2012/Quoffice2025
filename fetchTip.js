function fetchTip() {
    const maxTips = 100; // Adjust this number based on how many tips you have
    const randomIndex = Math.floor(Math.random() * maxTips) + 1;
    const filePath = `totd/t${randomIndex}.txt`;

    fetch(filePath)
        .then(response => {
            if (!response.ok) {
                throw new Error("Tip file not found");
            }
            return response.text();
        })
        .then(text => {
            document.getElementById("tipContent").innerText = text;
        })
        .catch(error => {
            console.log("Error fetching tip, trying another...", error);
            fetchTip(); // Try again with another file
        });
}

// Auto-refresh functionality
let autoRefresh = true; // Set to false if disabled in settings
if (autoRefresh) {
    setInterval(fetchTip, 10000); // Refreshes every 10 seconds
}

// Fetch a tip on page load
fetchTip();
