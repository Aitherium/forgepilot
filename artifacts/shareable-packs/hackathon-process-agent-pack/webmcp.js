// Drop this file into a browser tool page. Keep execution behind your own MCP/policy boundary.
const tool = {name:"hackathon-process-agent-pack", title:"Hackathon Process Agent Pack", description:"Turn this hackathon workflow into a shareable Codex + Claude + WebMCP pack with a local Bonsai path, awnboard authorization, and a phone-ready PWA.", inputSchema:{type:'object', properties:{request:{type:'string'}}}, execute: async (input) => window.FORGEPILOT_EXECUTE(input)};
const modelContext = document.modelContext || navigator.modelContext;
if (modelContext?.registerTool) await modelContext.registerTool(tool);
