import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel

TODO_FILE = "todo_items.json"

# HTML without line-through options, with proper WebChannel initialization
html_code = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ToDo</title>
<style>
body { margin:0; font-family:'Segoe UI',sans-serif; background-color:#fff8b5; color:#333; }
header { background-color:#ffeb3b; color:#000; padding:1rem; text-align:center; font-size:2rem; font-weight:bold; box-shadow:0 2px 4px rgba(0,0,0,0.2); }
.container { max-width:600px; margin:2rem auto; background:#fffde7; padding:2rem; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1); }
input[type="text"] { width:60%; padding:10px; font-size:1rem; border:2px solid #fbc02d; border-radius:5px; outline:none; }
button { padding:10px 15px; background-color:#fdd835; border:none; border-radius:5px; font-size:1rem; cursor:pointer; margin-left:10px; }
button:hover { background-color:#fbc02d; }
ul { list-style:none; padding:0; margin-top:1rem; }
li { background:#fffde7; padding:10px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; border-left:5px solid #fdd835; border-radius:5px; cursor:pointer; }
.delete-btn { background:#ff7043; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer; }
.delete-btn:hover { background-color:#f4511e; }
</style>
</head>
<body>
<header>ToDo</header>
<div class="container">
<input type="text" id="taskInput" placeholder="Enter a new task...">
<button onclick="addTask()">Add</button>
<ul id="taskList"></ul>
</div>

<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<script>
var pyjs;

new QWebChannel(qt.webChannelTransport, function(channel){
    pyjs = channel.objects.pyjs;
    loadTasks();
});

function loadTasks(){
    pyjs.loadTasks(function(js_code){
        eval(js_code);
    });
}

function saveTasks(){
    const items = [];
    document.querySelectorAll("#taskList li").forEach(li => {
        items.push(li.querySelector(".task-text").textContent);
    });
    pyjs.saveTasks(JSON.stringify(items));
}

function addTask(){
    const taskInput = document.getElementById("taskInput");
    const taskText = taskInput.value.trim();
    if(taskText==="") return;
    const li = document.createElement("li");
    li.innerHTML = '<span class="task-text">'+taskText+'</span><button class="delete-btn" onclick="removeTask(this)">Delete</button>';
    document.getElementById("taskList").appendChild(li);
    taskInput.value = "";
    saveTasks();
}

function removeTask(button){
    button.parentElement.remove();
    saveTasks();
}
</script>
</body>
</html>
"""

class Bridge(QObject):
    @pyqtSlot(result=str)
    def loadTasks(self):
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
        else:
            items = []

        js = """
function addTaskFromPython(text){
    const li = document.createElement("li");
    li.innerHTML = '<span class="task-text">'+text+'</span><button class="delete-btn" onclick="removeTask(this)">Delete</button>';
    document.getElementById("taskList").appendChild(li);
}
"""
        for task in items:
            js += f'addTaskFromPython("{task}");\n'
        return js

    @pyqtSlot(str)
    def saveTasks(self, tasks_json):
        items = json.loads(tasks_json)
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDo App")
        self.resize(700, 600)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Setup WebChannel
        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject("pyjs", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        # Load HTML from string
        self.browser.setHtml(html_code, QUrl(""))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
