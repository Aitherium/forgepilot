# Agents Everywhere bootstrap

ForgePilot is the first-mile launcher for the Aitherium world: a person starts with one machine and ends with a local agent, an MCP server, local inference or a chosen cloud backend, and connections to the tools where they already work.

## Choose a lane

### Local-first: Bonsai + awdk

```bash
python -m pip install awdk awm awnode
adk setup --tier bonsai
adk bonsai-local
adk start
python -m aitherium_pack serve
```

This is the recommended sovereignty path. The official awdk workflow also exposes `adk quickstart`, `adk doctor`, and `adk --backend bonsai-local`.

### Cloud-first: OpenRouter or another compatible backend

```bash
python -m pip install awdk awm awnode
adk quickstart --cloud
adk start
python -m aitherium_pack serve
```

ForgePilot can still use Exa for evidence and OpenRouter for the reasoning lane while keeping the local MCP surface on the machine.

### Add the terminal and desktop surfaces

```bash
npm i -g @aitherium/awsh
awsh

# Aither World Desk / desktop body
git clone https://github.com/Aitherium/awdesk
cd awdesk
npm install
npx electron .
```

The browser surface is the ForgePilot WebMCP page. AitherConnect is the optional browser bridge for federated search, page context, and the Living OS overlay.

### Switch Claude Code backends

The backend switcher is already in the installed ADK. Surface it as a user-facing
command instead of reimplementing provider configuration:

```bash
adk claude-model code                 # DeepSeek Flash fast coding profile
adk claude-model status               # show the active profile
adk claude-model check --timeout 30   # prove a real turn works
# Or use the shareable wrapper:
bash bootstrap/switch-claude-backend.sh code
```

Other built-in lanes include `plan`, `reason`, `local`, and `fast`. `awsettings` is
the portable settings/approval concept for keeping those choices consistent; it is
not a standalone executable on every install, so do not make the bootstrap depend on
an `awsettings` command being on PATH. Never copy provider API keys into a shareable
pack.

## Connect existing agents

The generated local MCP snippets point Codex and Claude at:

```text
python -m aitherium_pack mcp
```

For AitherOS Online, use the remote MCP configuration after deploying the local node behind an authenticated HTTPS tunnel. Never expose an unauthenticated local agent port.

## Advanced llama.cpp lane

If you already operate a llama.cpp-compatible server, point awdk/awnnode at its OpenAI-compatible base URL. For Bonsai’s ternary weights, prefer the Aitherium-supported `adk bonsai-local` path, which selects the compatible inference runtime for you.

## First success criterion

The bootstrap is complete when the user can ask the same ForgePilot identity from:

1. the local browser control room;
2. Codex or Claude over stdio MCP;
3. awsh or Aither World Desk;
4. AitherOS Online through a secured remote connection.

Each surface should produce the same run artifact and memory scope.
