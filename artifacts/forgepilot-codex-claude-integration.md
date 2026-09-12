# ForgePilot integration brief

Generated from the ForgePilot control room in Codex on 2026-09-12.

## Result

The browser workflow successfully ran two local tools:

1. `forgepilot_search` — returned offline demo evidence because `EXA_API_KEY` is not configured.
2. `forgepilot_chat` — returned an offline demo architecture response because `OPENROUTER_API_KEY` is not configured.

The durable client bundle was then generated with `forgepilot_generate_config`.

## Claude / Codex local MCP command

```json
{
  "command": "C:\\Users\\david\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
  "args": ["-m", "aitherium_pack", "mcp"],
  "cwd": "C:\\Users\\david\\OneDrive\\Documents\\ChatGPT\\ai-tinkerers-hackathon",
  "env": {"PYTHONUNBUFFERED": "1"}
}
```

## To switch from demo mode to live mode

Add these values to `.env` and restart the server:

```env
EXA_API_KEY=...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

The control room will then use Exa’s `auto` search with highlights and send the returned evidence to OpenRouter for the grounded integration response.

## Files

- `integrations/generated/claude.mcp.json`
- `integrations/generated/codex.mcp.json`
- `integrations/generated/remote-mcp.json`
- `integrations/generated/exa.tool.json`
- `integrations/generated/openrouter.tool.json`
