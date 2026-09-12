// Drop this file into a browser tool page. Keep execution behind your own MCP/policy boundary.
const tool = {name:"agents-everywhere-codex-proof", title:"Agents Everywhere Codex Proof", description:"A portable Codex and Claude Code tool pack using local Bonsai inference, awm, awrepl, awgraph, awgit, awnboard, awiam, and awbac.", inputSchema:{type:'object', properties:{request:{type:'string'}}}, execute: async (input) => window.FORGEPILOT_EXECUTE(input)};
const modelContext = document.modelContext || navigator.modelContext;
if (modelContext?.registerTool) await modelContext.registerTool(tool);
