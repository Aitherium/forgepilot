# Agents Everywhere: the hackathon process is the demo

## The pitch

ForgePilot shows how quickly a builder can go from an idea in a Codex conversation to a sharable agent tool. The thing being demonstrated is also how it was built: research, design, bootstrap, authorization, integration, and packaging all become reusable outputs.

## A 90-second run of show

1. **Start with the idea.** Leave the default prompt or replace it with a real project goal.
2. **Research + architect.** ForgePilot uses Exa/OpenRouter when configured and has an explicit offline mode when keys are absent.
3. **Show the one-click bootstrap.** Show the universal `awsh` front door: `curl -fsSL https://aitherium.com/phone.sh | bash` on the Pixel, or `install.sh` on a laptop. Then open `bootstrap/AITHERZERO_FIRST.md` for the inspectable PowerShell orchestration path; the app prints the awdk/awsh/awm/awrepl/awgraph/awgit activation plan.
4. **Show the local lane.** Click **Activate Bonsai-27B stack**. The app distinguishes detected packages from a running, proven local model.
5. **Show the trust boundary.** Click **Secure with awnboard**. The app makes the flow legible: awnboard → awiam → awbac → awdit → awtunnel → approved local tools.
6. **Show the desktop handoff.** Click **Configure Codex + Claude**. This creates runnable MCP JSON and installers for both clients.
7. **Show the shareable surface.** Click **Create shareable pack**. This creates MCP, WebMCP, PWA, and security metadata someone else can apply.
8. **Show the phone lane.** Click **Install on phone** or **Publish your own page**. The same identity becomes a PWA/LAN control surface.
9. **Close with proof.** Click **Package artifact** and open the report. It contains evidence, response, runtime stack, and a SHA-256 manifest.

## What is genuinely live

- The Codex plugin is installed and has called the ForgePilot MCP server.
- The browser UI calls the same MCP tools through JSON-RPC/WebMCP.
- Connector, shareable-pack, PWA, device-flow, and hashed-run artifacts are generated on demand.
- Host detection is honest: if awdk/awsh/Bonsai are not installed, the app says `ready_to_bootstrap` and emits the exact commands. Installed packages are not presented as a live local model until a real request succeeds.

## Why this scales

The author supplies an idea and a description. The pack factory supplies interfaces, client handoff, phone path, and trust metadata. The next builder can run the generated installer, approve the requested capabilities, and use the same tool from Codex, Claude Code, AitherOS, or a WebMCP-capable browser.
