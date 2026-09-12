# Aitherium Agent Pack — ForgePilot

ForgePilot is a hackathon-ready agent pack for building and shipping agent integrations from wherever the work already happens.

The hackathon demo is deliberately self-referential: it shows the process used to build this pack. A plain-language request becomes research, a local aw* bootstrap plan, a scoped identity/policy boundary, desktop connectors, a phone PWA, and a shareable artifact.

It gives you one local runtime with four surfaces:

- an Aitherium/awdk pack and fleet definition;
- a small MCP server for Codex, Claude Desktop/Code, ChatGPT-compatible MCP clients, and any MCP host;
- a WebMCP-enabled control room for browser agents;
- generated OpenRouter and Exa adapter configs.

The demo story is simple: ask ForgePilot to research an API or integration, get grounded Exa sources, then produce a portable setup bundle for the coding client you are using.

The larger hackathon story is Agents Everywhere: [bootstrap/AGENT_EVERYWHERE.md](bootstrap/AGENT_EVERYWHERE.md) walks a new builder from zero to awdk, Bonsai/local inference, MCP, awsh, desktop, and secured remote connections.

Backend switching is a first-class path too: run `bash bootstrap/switch-claude-backend.sh code` (or the PowerShell equivalent) to use `adk claude-model code` for the DeepSeek Flash coding profile, then verify with `adk claude-model check`. The pack exposes the same plan through `forgepilot_backend_switch_plan`.

The pack is also designed to be opened alongside [Aitherium Studio](https://studio.aitherium.com/): use `pack.yaml` as the identity/tool contract, `fleet.yaml` as the orchestration view, and the control room as the browser-native demo surface. Use `SHAREABLE_PACKS.md` when you want to turn a new idea into a portable MCP + WebMCP + PWA tool that other builders can apply.

## Quick start

### Windows

```powershell
Set-ExecutionPolicy -Scope Process Bypass
./setup.ps1
```

### macOS/Linux

```bash
chmod +x setup.sh
./setup.sh
```

The setup script creates `.venv`, installs this project plus the aw* acceleration and authorization bricks, writes `.env`, and emits client config snippets under `integrations/generated/`. For an offline demo-only install, set `SKIP_AWSDK=1`.

Add `EXA_API_KEY` for live research and `OPENROUTER_API_KEY` for model-backed chat. The app still starts without either key in demo mode, so the control room and MCP handshake can be shown offline.

Start the control room:

```bash
python -m aitherium_pack serve
```

Open http://127.0.0.1:8787.

### GitHub Pages

The repository ships an automated static deployment. Enable **Settings → Pages → GitHub Actions**, then push `main`. The `pages.yml` workflow builds the PWA and deploys it to the repository's Pages URL; `verify.yml` tests every pull request and checks the Pages bundle. The hosted page is a client only: configure its MCP endpoint to your own authenticated HTTPS ForgePilot/Aitherium node. See [DEPLOY.md](DEPLOY.md) for CORS, token, and repository-variable setup.

Or create a durable run artifact directly:

```bash
python -m aitherium_pack run "Design a safe Codex and Claude MCP integration for this project"
```

That writes `artifacts/runs/<run-id>/` with `research.json`, `response.json`, `report.md`, `stack.json`, and a SHA-256 `manifest.json`.

If you want the native Aitherium fleet server after setup:

```bash
adk-serve --fleet fleet.yaml --port 8080
```

## What is included

```text
pack.yaml                         awdk-style pack metadata
fleet.yaml                        awdk fleet definition
aitherium_pack/
  cli.py                          one-command setup/serve/config generation
  server.py                       stdlib HTTP + MCP JSON-RPC server
  providers.py                    Exa and OpenRouter adapters
  config.py                       generated client config helpers
  web/index.html                  ForgePilot control room + WebMCP tools
skills/                           portable pack skills
integrations/                     checked-in examples and generated snippets
```

## Desktop integrations

The generated files are intentionally plain JSON snippets so they can be copied into the client of choice:

- Claude Desktop / Claude Code: `integrations/generated/claude.mcp.json`
- Codex-style MCP clients: `integrations/generated/codex.mcp.json`
- ChatGPT or any remote MCP client: `integrations/generated/remote-mcp.json`

For a local stdio client, the server command is `python -m aitherium_pack mcp`. For a remote client, expose the HTTP server through a trusted tunnel and use `/mcp`. The HTTP server binds to loopback by default; non-loopback mode requires `FORGEPILOT_MCP_TOKEN` plus an explicit trusted-LAN flag. CORS is origin-allowlisted and request bodies are bounded.

## awdk connection

The pack is shaped for the current awdk workflow: `pip install awdk`, `adk install pack:...`, a named identity, and a fleet YAML. When awdk is installed, `python -m aitherium_pack install-awdk --cloud` runs the native cloud quickstart path and leaves this pack as the project-owned integration layer. The local MCP server remains dependency-light so the hackathon demo can run even before a full model backend is configured.

## Identity and capability boundary

The device-flow and local-stack plans are designed around the Aitherium front door: `awnboard` receives the request, `awiam` identifies the caller/session, `awbac` makes a fail-closed capability decision, `awdit` records it, and `awtunnel` handles private reachability. Only after approval does awsh/awdk reach Bonsai-27B, awm, awrepl, awgraph, awgit, or ForgePilot MCP.

## Safety boundary

ForgePilot’s first-party tools are read-only: health, web research, grounded chat, and config generation. Research results are marked untrusted before entering the model prompt. No email, purchase, file mutation, shell, or browser-navigation tool is exposed by default.

## Sources

- [Aitherium awdk](https://github.com/Aitherium/awdk)
- [Aitherium setup](https://aitherium.com/get/)
- [Exa coding-agent search guide](https://docs.exa.ai/reference/search-api-guide-for-coding-agents)
- [WebMCP draft specification](https://webmachinelearning.github.io/webmcp/)
