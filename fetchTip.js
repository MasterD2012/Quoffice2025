function fetchTip() {
    const maxTips = 100; // Set this to the number of tip files you have
    const randomIndex = Math.floor(Math.random() * maxTips) + 1;
    const filePath = `totd/t${randomIndex}.txt`;

    fetch(filePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Tip file not found: ${filePath}`);
            }
            return response.text(); // Ensure response is treated as plain text
        })
        .then(text => {
            document.getElementById("tipContent").textContent = text.trim(); // Removes unwanted whitespace
        })
        .catch(error => {
            console.log("Error fetching tip, trying another...", error);
            fetchTip(); // Try again with another file
        });
}

// Auto-refresh functionality
let autoRefresh = true; // Change this based on user settings
if (autoRefresh) {
    setInterval(fetchTip, 10000); // Refreshes every 10 seconds
}

// Fetch a tip on page load
fetchTip();
