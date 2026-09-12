# Aitherium device-flow contract

ForgePilot exposes `forgepilot_start_device_flow` to Codex, Claude, and the PWA. It creates a short-lived user code and a local pending session, then waits for the user to approve the requested scopes at the Aitherium verification URL.

The demo is deliberately honest: without `AITHERIUM_DEVICE_URL`, it runs in `demo-device-flow` mode and never issues or stores a token. In the real Aitherium deployment, configure:

```powershell
$env:AITHERIUM_DEVICE_URL = "https://aitherium.com/device"
```

The eventual awsh adapter should implement the same handoff with the scopes:

- `local.inference` — route to the user's local llama.cpp/Bonsai backend;
- `mcp.tools` — connect the approved MCP server;
- `workspace.read` — inspect the selected workspace;
- `lan.control` — reach the selected private-LAN node.

The user must approve the scopes. The device flow should return a short-lived access token only to the local awsh/awdk connector, store it in the platform credential store, and never put it in the browser, PWA bundle, artifact report, or Codex transcript.

Suggested awsh CLI contract:

```text
awsh auth device --client-id forgepilot --scope local.inference mcp.tools workspace.read lan.control
awsh node register --name <device-name> --transport mcp --listen 127.0.0.1
```

After registration, Codex/Claude can use the stdio MCP connection on desktop or the authenticated HTTPS endpoint from the phone PWA. Do not expose unauthenticated MCP directly to the public internet.
