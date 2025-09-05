
const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');
const fs = require('fs');

let pyProc = null;
let mainWindow = null;

function createPy () {
  const base = path.join(__dirname, '..');
  const pyBin = path.join(base, 'python-dist', process.platform === 'win32' ? 'app.exe' : 'app');
  if (fs.existsSync(pyBin)) {
    // run the bundled binary
    pyProc = spawn(pyBin, [], { cwd: base });
  } else {
    // fallback to streamlit (development)
    pyProc = spawn('streamlit', ['run', 'app.py'], { cwd: base });
  }
  pyProc.stdout.on('data', (data) => {
    console.log(`PY: ${data.toString()}`);
  });
  pyProc.stderr.on('data', (data) => {
    console.error(`PY ERR: ${data.toString()}`);
  });
  pyProc.on('close', (code) => {
    console.log('Python process exited with ' + code);
  });
}

function waitForServer(url, timeoutMs=120000, intervalMs=1000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const check = () => {
      http.get(url, (res) => {
        resolve(true);
      }).on('error', () => {
        if (Date.now() - start > timeoutMs) {
          reject(new Error('Timeout waiting for server'));
        } else {
          setTimeout(check, intervalMs);
        }
      });
    };
    check();
  });
}

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 900,
    icon: path.join(__dirname, '..', 'assets', 'icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });
  mainWindow.loadURL('http://localhost:8501');
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(async () => {
  createPy();
  try {
    await waitForServer('http://localhost:8501', 120000, 1000);
    createWindow();
  } catch (err) {
    console.error('Server did not start in time:', err);
    createWindow();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
  if (pyProc) {
    try { pyProc.kill(); } catch(e) {}
  }
});
