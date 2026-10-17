#!/usr/bin/env node

const { execSync } = require('child_process');
const os = require('os');

const isWin = os.platform() === 'win32';
const PORTS = [
  { name: 'Backend (FastAPI)', port: 8000 },
  { name: 'Frontend (Vite Primary)', port: 3000 },
  { name: 'Frontend (Vite Fallback)', port: 5173 },
];

console.log('\n\x1b[36m========================================\x1b[0m');
console.log('\x1b[36m🔍  NURTURA PORT SCANNER & CLEANER\x1b[0m');
console.log('\x1b[36m========================================\x1b[0m\n');

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
  } catch {}
  return Array.from(pids);
}

PORTS.forEach(({ name, port }) => {
  process.stdout.write(`Port ${port} (${name}): `);
  const pids = getPidsOnPort(port);
  if (pids.length === 0) {
    console.log('\x1b[32mKOSONG / SIAP DIGUNAKAN\x1b[0m');
    return;
  }

  console.log(`\x1b[33mDigunakan PID: ${pids.join(', ')} -> Membebaskan...\x1b[0m`);
  for (const pid of pids) {
    try {
      if (isWin) execSync(`taskkill /F /T /PID ${pid}`, { stdio: 'ignore' });
      else execSync(`kill -9 ${pid}`, { stdio: 'ignore' });
      console.log(`   \x1b[32m✔ PID ${pid} berhasil dihentikan.\x1b[0m`);
    } catch (err) {
      console.warn(`   \x1b[31m✖ Gagal menghentikan PID ${pid}\x1b[0m`);
    }
  }
});

console.log('\n\x1b[32m✔ Selesai memindai dan membebaskan port.\x1b[0m\n');
