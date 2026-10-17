#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

const isWin = os.platform() === 'win32';
const rootDir = path.resolve(__dirname, '..');
const backendDir = path.join(rootDir, 'backend');
const frontendDir = path.join(rootDir, 'frontend');

// Ports used by Nurtura
const PORTS = [
  { name: 'Backend (FastAPI)', port: 8000 },
  { name: 'Frontend (Vite Primary)', port: 3000 },
  { name: 'Frontend (Vite Fallback)', port: 5173 },
];

console.log('\n\x1b[36m========================================================\x1b[0m');
console.log('\x1b[36m🌱  NURTURA FULLSTACK RUNNER (PORT GUARD & DEV)\x1b[0m');
console.log('\x1b[36m========================================================\x1b[0m\n');

/**
 * Scan and return array of PIDs listening on a given TCP port
 */
function getPidsOnPort(port) {
  const pids = new Set();
  try {
    if (isWin) {
      const output = execSync('netstat -ano -p tcp', {
        encoding: 'utf-8',
        stdio: ['ignore', 'pipe', 'ignore'],
      });
      const lines = output.split(/\r?\n/);
      for (const line of lines) {
        if (line.includes(`:${port}`) && line.includes('LISTENING')) {
          const parts = line.trim().split(/\s+/);
          const pid = parts[parts.length - 1];
          if (pid && pid !== '0' && !isNaN(Number(pid))) {
            pids.add(Number(pid));
          }
        }
      }
    } else {
      const output = execSync(`lsof -ti tcp:${port}`, {
        encoding: 'utf-8',
        stdio: ['ignore', 'pipe', 'ignore'],
      });
      output
        .split(/\r?\n/)
        .map((p) => p.trim())
        .filter(Boolean)
        .forEach((pid) => pids.add(Number(pid)));
    }
  } catch {
    // Port is free or utility returned no matching records
  }
  return Array.from(pids);
}

/**
 * Scan and terminate processes occupying target ports
 */
function freePort(serviceName, port) {
  process.stdout.write(`🔍 Memindai port ${port} (${serviceName})... `);
  const pids = getPidsOnPort(port);
  if (pids.length === 0) {
    console.log('\x1b[32m[BEBAS]\x1b[0m');
    return;
  }

  console.log(`\x1b[33m[TERPAKAI oleh PID: ${pids.join(', ')}]\x1b[0m`);
  for (const pid of pids) {
    try {
      console.log(`   ⚡ Membebaskan port ${port}: menghentikan PID ${pid}...`);
      if (isWin) {
        execSync(`taskkill /F /T /PID ${pid}`, { stdio: 'ignore' });
      } else {
        execSync(`kill -9 ${pid}`, { stdio: 'ignore' });
      }
      console.log(`   \x1b[32m✔ PID ${pid} berhasil dihentikan.\x1b[0m`);
    } catch (err) {
      console.warn(`   \x1b[31m✖ Gagal menghentikan PID ${pid}: ${err.message}\x1b[0m`);
    }
  }

  // Double check port status
  const remaining = getPidsOnPort(port);
  if (remaining.length === 0) {
    console.log(`   \x1b[32m✔ Port ${port} sekarang sudah siap digunakan.\x1b[0m`);
  } else {
    console.warn(`   \x1b[31m⚠ Peringatan: Port ${port} masih digunakan PID: ${remaining.join(', ')}\x1b[0m`);
  }
}

// 1. Scan and free ports
console.log('\x1b[1mTahap 1: Memindai & Membebaskan Port (8000, 3000, 5173)\x1b[0m');
PORTS.forEach(({ name, port }) => freePort(name, port));

// 2. Resolve Python environment for backend
let pythonExe = 'python';
const venvPythonWin = path.join(backendDir, '.venv', 'Scripts', 'python.exe');
const venvPythonUnix = path.join(backendDir, '.venv', 'bin', 'python');

if (isWin && fs.existsSync(venvPythonWin)) {
  pythonExe = venvPythonWin;
} else if (!isWin && fs.existsSync(venvPythonUnix)) {
  pythonExe = venvPythonUnix;
}

console.log('\n\x1b[1mTahap 2: Menjalankan Backend & Frontend Bersamaan\x1b[0m');
console.log(`\x1b[35m[Backend]\x1b[0m  FastAPI : ${pythonExe}`);
console.log(`\x1b[34m[Frontend]\x1b[0m Vite    : npm run dev di folder /frontend\n`);

// 3. Spawn child processes
const children = [];

function spawnService(prefix, color, commandLine, cwd) {
  const child = spawn(commandLine, {
    cwd,
    stdio: 'inherit',
    shell: true,
  });

  child.on('error', (err) => {
    console.error(`${color}[${prefix}]\x1b[0m Gagal memulai proses:`, err);
  });

  child.on('exit', (code, signal) => {
    if (signal !== 'SIGINT' && signal !== 'SIGTERM') {
      console.log(`${color}[${prefix}]\x1b[0m Proses selesai (kode: ${code})`);
    }
  });

  children.push(child);
  return child;
}

// Launch Backend (FastAPI on Port 8000)
const backendCmd = `"${pythonExe}" -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0`;
spawnService('BACKEND', '\x1b[35m', backendCmd, backendDir);

// Launch Frontend (Vite on Port 3000)
const frontendCmd = isWin ? 'npm.cmd run dev' : 'npm run dev';
spawnService('FRONTEND', '\x1b[34m', frontendCmd, frontendDir);

// 4. Graceful Cleanup Handler
let cleaningUp = false;
function cleanup() {
  if (cleaningUp) return;
  cleaningUp = true;
  console.log('\n\x1b[33m🛑 Menghentikan proses Backend dan Frontend...\x1b[0m');

  for (const child of children) {
    if (child && child.pid) {
      try {
        if (isWin) {
          execSync(`taskkill /F /T /PID ${child.pid}`, { stdio: 'ignore' });
        } else {
          process.kill(-child.pid, 'SIGTERM');
        }
      } catch {
        // Process might already be exited
      }
    }
  }

  // Ensure target ports are completely free
  PORTS.forEach(({ port }) => {
    const pids = getPidsOnPort(port);
    pids.forEach((pid) => {
      try {
        if (isWin) execSync(`taskkill /F /T /PID ${pid}`, { stdio: 'ignore' });
        else execSync(`kill -9 ${pid}`, { stdio: 'ignore' });
      } catch {}
    });
  });

  console.log('\x1b[32m✔ Seluruh layanan dihentikan. Port telah dibebaskan.\x1b[0m\n');
  process.exit(0);
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
