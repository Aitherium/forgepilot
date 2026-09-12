# Agents Everywhere (Aitherium) — submission text

Paste-ready for the AI Tinkerers "Agents, Everywhere" portal (2026-09-12). Canonical app link: https://aitherium.github.io/forgepilot/

## Project name
Agents Everywhere (Aitherium)

## Project description
Agents shouldn't live in a chatbox. Agents Everywhere puts one in the places developers already work — the **terminal**, the **IDE**, and the **phone** — and makes getting there a single click.

Open the page, click your OS. The launcher runs AitherZero's `dev-workstation` playbook (PowerShell 7, Python, Git, Node, gh, `adk`, `awsh`) and then `connect` (browser device-flow sign-in, inference check, and MCP wiring for Claude Code / Cursor / Windsurf / VS Code to the Aitherium gateway). Every step is *proven*, not assumed — real `--version` calls, a real gateway handshake — and every step is idempotent, so re-running repairs. Then `awsh` answers questions typed where a command would go, using the machine's real context (cwd, env, files, running containers), which no standalone chatbot has. Same one line on macOS/Linux; on an Android phone via Termux the bootstrap runs natively.

Environment shapes the workflow: the terminal gives the agent context; the IDE gets the gateway's tools through MCP; the phone makes the agent portable. ForgePilot (the published PWA) exposes the same capabilities over MCP and WebMCP (`navigator.modelContext`) and packages every run as a hashed, shareable artifact.

Tech: AitherZero (PowerShell 7 playbook engine — during the hackathon we fixed 8 bugs that made no public-repo script runnable, added the bootstrap door and 4 playbooks), awdk (`adk` — device-flow auth, `adk mcp setup`, `adk setup` for vLLM/Ollama/llama.cpp), awsh, aither-kvcache, awnix (bootc image), MCP JSON-RPC, WebMCP, a static PWA on GitHub Pages, Exa + OpenRouter adapters in the ForgePilot pack. All open source: Aitherium/AitherZero #4 #5, Aitherium/awskills #32, Aitherium/forgepilot.

## Products & tools used
AI Tinkerers. Exa / OpenRouter **only if keys are in `.env` and one live `forgepilot_search` / `forgepilot_chat` ran before submitting** (adapters: `aitherium_pack/providers.py`). Other: Aitherium aw* stack, Claude Code, Codex, GitHub Pages, Cloudflare.

## Team contributions — David Parkhurst (Lead)
Built the AitherZero one-paste bootstrap (`bootstrap.ps1`/`.sh`, 5.1→pwsh re-exec, Termux lane), the `dev-workstation` / `connect` / `local-inference` / `awnix` playbooks and 9 onboarding scripts, engine fixes (script `_init` resolution, exit/throw contract, headless prompts, log levels, banners, idempotent package install, PATH refresh), CI fixes; the ForgePilot agent pack (MCP server, WebMCP page tools, PWA, artifact/manifest generation, connector generators, one-click launchers); the `agents-everywhere` awskill + tool scaffold; publishing to GitHub Pages and the Demo Hall. Used Claude Code and Codex as the coding agents; Exa/OpenRouter adapters in the pack.

## Additional links
1. https://aitherium.github.io/forgepilot/ — the app (click your OS)
2. https://github.com/Aitherium/AitherZero — playbooks + bootstrap (PRs #4, #5)
3. https://github.com/Aitherium/forgepilot — ForgePilot pack source
(also: https://github.com/Aitherium/awskills/pull/32)

## Prior work
AitherZero, awdk, awsh, aither-kvcache, awnix, the Aitherium gateway/portal and Demo Hall pre-existed. Created today: the bootstrap door and every playbook/script named above, the engine and CI fixes, the ForgePilot pack, PWA, launchers, connector artifacts, the awskill and scaffold, and the publishing.

## Social post
Agents shouldn't live in a chatbox. One click puts one in your terminal, your IDE, and your phone — installed, signed in, wired to MCP, and *proven* at every step. https://aitherium.github.io/forgepilot/  Built on the open aw* stack. @AITinkerers @OpenAI @CopilotKit @openrouter @exaailabs @auth0 @ambiguousio @triggerdotdev @mozillaAI @googlecloud #AgentsEverywhere

## Before the demo (do not skip)
- Run `agents-everywhere-windows.cmd` once on a second Windows box (SmartScreen → More info → Run anyway). Must end with "DONE. Open a new terminal and type: awsh".
- Pixel/Termux: `curl -fsSL https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.sh | sh` — only show live if it passed.
- One scripted `awsh` question that needs local context.
- demo.aitherium.com is served by a Cloudflare Worker, not the demo-aitherium gh-pages branch; `/forgepilot/` needs a Worker route or use the github.io link.
