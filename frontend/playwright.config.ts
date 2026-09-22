import { defineConfig, devices } from '@playwright/test';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const frontend = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(frontend, '..');
const python = path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const localBrowsers = path.join(root, '.cache', 'ms-playwright');
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync(localBrowsers)) process.env.PLAYWRIGHT_BROWSERS_PATH = localBrowsers;

export default defineConfig({
  testDir: './e2e', fullyParallel: false, workers: 1, timeout: 30000,
  use: { baseURL: 'http://127.0.0.1:5174', trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 1000 } } }],
  webServer: [
    { command: `"${python}" -m uvicorn app.main:app --host 127.0.0.1 --port 8001`, cwd: root, url: 'http://127.0.0.1:8001/api/health', timeout: 30000,
      env: { CHAINLENS_DATABASE_URL: `sqlite:///${path.join(root, '.runtime', 'e2e-v3.sqlite3').replaceAll('\\', '/')}`, CHAINLENS_SNAPSHOT: path.join(root, 'data/snapshots/2026-09-16.v3.json') } },
    { command: `"${process.execPath}" node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5174 --strictPort`, cwd: frontend, url: 'http://127.0.0.1:5174', timeout: 30000, env: { VITE_API_TARGET: 'http://127.0.0.1:8001' } },
  ],
});
