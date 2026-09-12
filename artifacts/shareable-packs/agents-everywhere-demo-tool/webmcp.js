// Drop this file into a browser tool page. Keep execution behind your own MCP/policy boundary.
const tool = {name:"agents-everywhere-demo-tool", title:"Agents Everywhere Demo Tool", description:"Find the official MCP setup for this project and give me a safe Codex + Claude integration plan.", inputSchema:{type:'object', properties:{request:{type:'string'}}}, execute: async (input) => window.FORGEPILOT_EXECUTE(input)};
const modelContext = document.modelContext || navigator.modelContext;
if (modelContext?.registerTool) await modelContext.registerTool(tool);
