# Agents Everywhere: phone, LAN, and self-service publishing

ForgePilot has one MCP tool surface and three ways to reach it:

1. **Phone PWA:** deploy the static bundle to an HTTPS host (AitherOS Online, GitHub Pages, Netlify, or Cloudflare Pages), open it on the phone, and choose **Add to Home Screen / Install app**. The browser UI is a thin client; API keys stay on the MCP host.
2. **Trusted LAN:** set a random `FORGEPILOT_MCP_TOKEN`, set `FORGEPILOT_ALLOW_INSECURE_LAN=1`, run `python -m aitherium_pack serve` on a host PC, and open `http://<host-name>.local:8787/` from a phone on the same Wi-Fi. Prefer HTTPS/private tunneling before exposing anything beyond the LAN.
3. **Desktop home:** choose AitherOS Online, [Aither World Desk](https://github.com/Aitherium/awdesk), or [GobboNet](https://github.com/ElodineOfficial/gobbonet) depending on whether the user wants a hosted living desktop, Aitherium desktop, or local-private LAN GUI.

## Publish a page yourself

```powershell
python -m aitherium_pack publish --output dist/agent-everywhere --mcp-endpoint https://YOUR-MCP-HOST.example/mcp
```

Commit `dist/agent-everywhere` to a GitHub repository and enable GitHub Pages for that folder, or upload the folder to any static host. The endpoint must be authenticated HTTPS for internet use. Do not place provider API keys in `config.js` or browser code.

## Connect from Codex or Claude on a phone

Codex/Claude can use the same remote MCP endpoint when their mobile/client surface supports remote MCP. Complete the connection in that client, then use the installed ForgePilot PWA for the visual setup checklist. For desktop Codex/Claude, use the included stdio config or the ForgePilot Codex plugin; for a phone, prefer the HTTPS endpoint and the PWA.

## Local-first inference

```powershell
python -m pip install awdk awm awnode
adk setup --tier bonsai
adk bonsai-local
adk start
python -m aitherium_pack serve
```

Keep the local model and MCP server on the host PC. The phone is the control surface.

The raw server is intentionally not internet-safe. Non-loopback mode requires a
bearer token and an explicit trusted-LAN flag; use HTTPS or a private tunnel for
remote access.
