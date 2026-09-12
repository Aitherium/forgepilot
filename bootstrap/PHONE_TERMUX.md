# Phone-terminal demo: Agents Everywhere

The universal entry point is **AitherShell / `awsh`**, not a desktop GUI. Aitherium's
official laptop path is:

```bash
curl -fsSL https://aitherium.com/install.sh | sh
```

On Android Termux or the Pixel Linux Terminal, use:

```bash
curl -fsSL https://aitherium.com/phone.sh | bash
```

Verify the universal terminal, then add this pack:

```bash
git clone https://github.com/YOUR-ORG/agents-everywhere.git
cd agents-everywhere
bash bootstrap/agents-everywhere.sh
```

For a phone that already has Termux, the recovery script installs the user-space Python,
Git, and Node prerequisites, creates an isolated environment, installs awdk plus the
optional aw* bricks, installs awsh when npm is available, attempts the AitherZero
`node-onboard` playbook when PowerShell is available, and starts the local MCP/WebMCP
control surface. It writes a status record under
`~/.aitherium/agents-everywhere/status.txt` and never writes credentials there.

## Choose the local or remote lane

The default tries the local `bonsai-27b` path:

```bash
AITHERIUM_MODEL=bonsai-27b bash bootstrap/agents-everywhere.sh
```

If the device cannot hold the selected model, keep the agent on the phone and route
inference through an authenticated awnode or other MCP endpoint:

```bash
AITHERIUM_RUN_LOCAL_MODEL=0 bash bootstrap/agents-everywhere.sh
```

That is still “Agents Everywhere”: the control plane, identity, WebMCP/PWA, and tool
surface travel with the person; the model can be local, LAN-local, or a user-chosen
remote backend. Do not promise that every phone can run a 27B model just because it
can run a Linux kernel—RAM, storage, thermals, quantization, and backend support are
the real gate.

## Connect the phone

1. Keep the server on loopback for a single-device demo. For LAN mode, set a random
   `FORGEPILOT_MCP_TOKEN` and `FORGEPILOT_ALLOW_INSECURE_LAN=1` only on a trusted LAN.
2. Put awnboard in front of any LAN or internet exposure; let awiam identify the
   device, awbac make the capability decision, and awdit record it.
3. Publish the static PWA over HTTPS and point it at an authenticated MCP endpoint.
4. Install it with **Add to Home Screen**. Awconnect can provide the browser/desktop
   bridge, while awnode keeps the selected backend behind the same capability surface.

## Switch the coding backend from the phone terminal

Once `awsh`/`adk` is installed, the same pack can switch Claude Code without editing
provider environment variables by hand:

```bash
bash bootstrap/switch-claude-backend.sh code
```

That runs `adk claude-model code`, shows the active profile, and performs a real
`adk claude-model check`. Use `plan`, `reason`, `local`, `fast`, or a named profile as
the argument. Keys remain in the local credential/settings plane.

## Demo proof

```bash
curl http://127.0.0.1:8787/health
adk status
awsh --version
```

“Detected” means the executable exists. “Proven” means a real request completed using
the intended local model or the explicitly selected remote endpoint. Show that
distinction on stage.
