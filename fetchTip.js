function fetchTip() {
  const maxTips = 3; // Adjust this number to match the number of tip files you have.
  const randomIndex = Math.floor(Math.random() * maxTips) + 1; // generates 1, 2, or 3
  const filePath = `totd/t${randomIndex}.txt`;

  fetch(filePath)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Tip file not found: ${filePath}`);
      }
      return response.text();
    })
    .then(text => {
      document.getElementById('tipContent').innerText = text.trim();
    })
    .catch(err => {
      console.error('Error fetching tip:', err);
      document.getElementById('tipContent').innerText = 'Failed to load tip.';
    });
}
