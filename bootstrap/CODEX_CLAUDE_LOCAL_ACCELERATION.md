# Codex + Claude Code on the local Bonsai-27B stack

The target topology is:

```text
Codex / Claude Code
        │ stdio MCP (desktop) or authenticated HTTPS MCP (phone/PWA)
awnboard → awiam → awbac → awdit → awsh connector
        │ approved capability decision
awdk fleet → awm memory · awrepl REPL · awgraph context · awgit project ops
        │
llama.cpp / Bonsai-27B on the user's host
```

ForgePilot's `forgepilot_local_acceleration_plan` is the easy-button planner. It detects whether the local commands are present and emits the activation sequence without installing or changing anything:

```powershell
python -m pip install awdk awm awrepl awgraph awgit
adk setup --tier bonsai --model bonsai-27b
adk bonsai-local --model bonsai-27b
adk start
awsh auth device --client-id forgepilot --scope local.inference mcp.tools workspace.read lan.control
awsh node register --name forgepilot-local --transport mcp --listen 127.0.0.1
python -m aitherium_pack mcp
```

Then connect the stdio MCP config in `integrations/generated/codex.mcp.json` or `integrations/generated/claude.mcp.json`. The agent can use the approved awm/awrepl/awgraph/awgit tools through that one local surface while Bonsai-27B remains local.

The device flow is the identity trust boundary, and `awnboard` is the request trust boundary: a user approves the scopes on Aitherium, awiam resolves the session, awbac evaluates the role/capability, awdit records the decision, and only then does awsh/awdk reach the local stack. The connector receives the short-lived credential; the PWA/phone never receives local API keys. For a LAN phone, keep the MCP host private and use an authenticated HTTPS tunnel when leaving the LAN.
