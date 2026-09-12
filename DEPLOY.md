# Ship the Agents Everywhere demo

## One-click local demo

```powershell
.\setup.ps1
python -m aitherium_pack serve
```

Open `http://127.0.0.1:8787/` on the desktop, or use the LAN hostname from a phone on the same Wi-Fi.

## Build a phone PWA

```powershell
python -m aitherium_pack publish --output dist/agent-everywhere --mcp-endpoint https://YOUR-MCP-HOST.example/mcp
```

The generated folder is static and can be published from a GitHub Pages branch, a `/docs` folder, or any static host. Replace the placeholder endpoint with a real authenticated HTTPS MCP URL.

## GitHub Pages, automatically

This repository includes two GitHub Actions workflows:

- `Verify ForgePilot` runs the Python tests and builds/checks the static bundle on pull requests and pushes to `main`.
- `Deploy ForgePilot to GitHub Pages` publishes the PWA after every push to `main`.

One-time setup:

1. In the repository, open **Settings → Pages** and choose **GitHub Actions** as the source.
2. Optionally create a repository variable named `FORGEPILOT_MCP_ENDPOINT` containing an authenticated HTTPS endpoint such as `https://agent.example.com/mcp`. If it is unset, the page opens with `/mcp` and asks each user to configure their own endpoint.
3. Push to `main`; the Pages workflow exposes the deployed URL in its environment summary.

The page is only the client. Each user can run `python -m aitherium_pack serve` locally, host an MCP server on a trusted LAN, or publish an authenticated HTTPS endpoint. For a cross-origin Pages connection, add the exact Pages origin to `FORGEPILOT_ALLOWED_ORIGINS` on the MCP host and use `FORGEPILOT_MCP_TOKEN`; do not put a bearer token in the Pages repository or static bundle.

The endpoint field is remembered in the browser. A bearer token, when needed, is held in memory only and is cleared by refresh or the **Clear** button.

## Demo story

1. Open the PWA on a phone and choose **Local LAN**, **Install on phone**, or **Publish your own page**.
2. Click **Package artifact**. ForgePilot writes a report, evidence bundle, runtime stack, and SHA-256 manifest.
3. In Codex, install the local `forgepilot-agent-everywhere` plugin. Its MCP server exposes the same five tools over stdio.
4. Show the same identity from Codex, the browser page, and a phone-sized PWA.
