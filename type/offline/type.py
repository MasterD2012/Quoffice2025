import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot

# Python class exposed to JavaScript
class Backend(QObject):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor

    @pyqtSlot(result=str)
    def loadFile(self):
        path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Type 2025 (*.TYP2)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to load file:\n{e}")
        return ""

    @pyqtSlot(str)
    def saveFile(self, content):
        path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Type 2025 (*.TYP2)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to save file:\n{e}")

# Your HTML code embedded
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Type 2025</title>
<style>
body { margin:0; font-family: "Segoe UI", sans-serif; background:#f4f4f4; }
body.dark { background:#2e2e2e; color:white; }
.ribbon { display:flex; flex-direction:column; background:#e7e7e7; border-bottom:1px solid #ccc; }
.ribbon-tabs { display:flex; background:#f2f2f2; }
.ribbon-tab { padding:10px 15px; cursor:pointer; border-bottom:3px solid transparent; }
.ribbon-tab.active { border-bottom:3px solid dodgerblue; background:#fff; }
.ribbon-content { display:none; padding:10px; background:#fff; }
.ribbon-content.active { display:flex; gap:20px; flex-wrap:wrap; }
.ribbon-group { border:1px solid #ccc; padding:10px; min-width:120px; background:#f9f9f9; }
#editor { padding:20px; margin:10px; min-height:500px; background:white; border:1px solid #ccc; outline:none; }
body.dark #editor { background:#444; color:white; }
#context-menu { position:absolute; display:none; background:white; border:1px solid #ccc; z-index:1000; box-shadow:0 0 10px rgba(0,0,0,0.2); }
#context-menu ul { list-style:none; margin:0; padding:5px 0; }
#context-menu li { padding:8px 20px; cursor:pointer; }
#context-menu li:hover { background:#eee; }
.bottom-bar { display:flex; justify-content:space-between; align-items:center; padding:5px 15px; background:#ddd; border-top:1px solid #aaa; position:fixed; bottom:0; width:100%; }
.zoom-slider { width:200px; }
</style>
</head>
<body>
<div class="ribbon">
<div class="ribbon-tabs">
<div class="ribbon-tab" data-tab="file">File</div>
<div class="ribbon-tab active" data-tab="home">Home</div>
<div class="ribbon-tab" data-tab="insert">Insert</div>
<div class="ribbon-tab" data-tab="layout">Layout</div>
<div class="ribbon-tab" data-tab="review">Review</div>
</div>
<div class="ribbon-content" id="file">
<div class="ribbon-group">
<button onclick="newDocument()">New</button>
<button onclick="saveDocument()">Save</button>
<button onclick="loadDocument()">Open</button>
</div>
</div>
<div class="ribbon-content active" id="home">
<div class="ribbon-group">
<select onchange="document.execCommand('fontName', false, this.value)">
<option value="Segoe UI">Segoe UI</option>
<option value="Arial">Arial</option>
<option value="Georgia">Georgia</option>
</select>
<select onchange="document.execCommand('fontSize', false, this.value)">
<option value="1">8pt</option>
<option value="2">10pt</option>
<option value="3">12pt</option>
<option value="4">14pt</option>
<option value="5">18pt</option>
</select>
</div>
<div class="ribbon-group">
<button onclick="document.execCommand('bold')"><b>B</b></button>
<button onclick="document.execCommand('italic')"><i>I</i></button>
<button onclick="document.execCommand('underline')"><u>U</u></button>
</div>
<div class="ribbon-group">
<button onclick="document.execCommand('justifyLeft')">Left</button>
<button onclick="document.execCommand('justifyCenter')">Center</button>
<button onclick="document.execCommand('justifyRight')">Right</button>
</div>
</div>
<div class="ribbon-content" id="insert">
<div class="ribbon-group">
<button onclick="document.execCommand('insertImage', false, prompt('Image URL:'))">Insert Image</button>
<button onclick="insertTable()">Insert Table</button>
</div>
</div>
<div class="ribbon-content" id="layout">
<div class="ribbon-group"><button onclick="toggleDarkMode()">Toggle Dark Mode</button></div>
</div>
<div class="ribbon-content" id="review"><div class="ribbon-group"><p>No review tools available</p></div></div>
</div>
<div id="editor" contenteditable="true">Type here...</div>
<div id="context-menu">
<ul>
<li onclick="document.execCommand('cut')">Cut</li>
<li onclick="document.execCommand('copy')">Copy</li>
<li onclick="document.execCommand('paste')">Paste</li>
<li onclick="document.execCommand('undo')">Undo</li>
<li onclick="document.execCommand('redo')">Redo</li>
<li onclick="document.execCommand('selectAll')">Select All</li>
</ul>
</div>
<div class="bottom-bar">
<input type="range" min="50" max="200" value="100" class="zoom-slider" onchange="zoomEditor(this.value)">
</div>

<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<script>
let backend;
new QWebChannel(qt.webChannelTransport, function(channel) {
    backend = channel.objects.backend;
});

document.querySelectorAll('.ribbon-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.ribbon-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.ribbon-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

const contextMenu = document.getElementById("context-menu");
const editor = document.getElementById("editor");

editor.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    contextMenu.style.top = e.pageY + "px";
    contextMenu.style.left = e.pageX + "px";
    contextMenu.style.display = "block";
});

document.addEventListener("click", () => { contextMenu.style.display = "none"; });

function insertTable() {
    const table = document.createElement('table'); table.border = "1";
    for (let i=0;i<3;i++){ const row = table.insertRow();
        for(let j=0;j<3;j++){ const cell = row.insertCell(); cell.textContent="Cell"; } }
    editor.appendChild(table);
}
function toggleDarkMode(){ document.body.classList.toggle('dark'); }
function zoomEditor(val){ editor.style.zoom = val + '%'; }
function newDocument(){ editor.innerHTML=""; }
function saveDocument(){ backend.saveFile(editor.innerHTML); }
function loadDocument(){ 
    backend.loadFile().then(content => { if(content) editor.innerHTML = content; }); 
}
</script>
</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Type 2025")
        self.resize(1000, 700)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Setup web channel for JS-Python communication
        self.channel = QWebChannel()
        self.backend = Backend(self.browser)
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)

        self.browser.setHtml(html_code)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
