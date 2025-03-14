const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.static('public'));

app.get('/list-tips', (req, res) => {
  const tipsDir = path.join(__dirname, 'public', 'totd');
  fs.readdir(tipsDir, (err, files) => {
    if (err) {
      return res.status(500).json({ error: 'Unable to scan directory' });
    }
    const tipFiles = files.filter(file => path.extname(file) === '.txt');
    res.json(tipFiles);
  });
});

app.get('/tip-content/:filename', (req, res) => {
  const tipsDir = path.join(__dirname, 'public', 'totd');
  const filePath = path.join(tipsDir, req.params.filename);
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Unable to read file' });
    }
    res.send(data);
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
