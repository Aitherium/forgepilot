# Hackathon submission: ForgePilot

## One-line pitch

ForgePilot is a portable Aitherium agent pack that follows builders from browser research to the desktop coding agent they already use.

## Why this belongs somewhere new

Most agents live in a chat tab and make people copy context across tools. ForgePilot makes the integration surface itself agent-ready: the same pack appears as an awdk identity, an MCP server, and a WebMCP tool surface inside the control room.

## Two-minute demo

1. Run `./setup.ps1` on Windows or `./setup.sh` on macOS/Linux.
2. Open `http://127.0.0.1:8787`.
3. Submit: “Find the official MCP setup for this project and give me a safe Codex + Claude integration plan.”
4. Show the grounded response and source URLs. With no keys, the offline demo path still renders; with `EXA_API_KEY` and `OPENROUTER_API_KEY`, it becomes live.
5. Click “Show configs” and show that the same pack emits Claude, Codex, remote MCP, Exa, and OpenRouter connection artifacts.
6. Open the page in a WebMCP-capable browser agent and point out that the tools are registered on the page, not simulated through clicks.
7. Finish by showing `fleet.yaml`: the browser experience, desktop MCP experience, and awdk fleet all resolve to the same ForgePilot identity.

## Architecture

```text
                 ┌──────────────────────────┐
                 │ ForgePilot / pack.yaml   │
                 │ identity + skills        │
                 └────────────┬─────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    awdk fleet           MCP /mcp             WebMCP page
    fleet.yaml       Codex / Claude /        browser-native
                    ChatGPT-compatible       tools + context
                              │
                    Exa evidence + OpenRouter
```

## Safety choice

The public demo exposes only read-only health, search, grounded chat, and config generation. That makes the cross-surface story easy to inspect and keeps consequential actions behind a future approval layer.
