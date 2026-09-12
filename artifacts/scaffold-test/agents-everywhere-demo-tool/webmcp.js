// Guarded WebMCP registration for agents-everywhere-demo-tool; provide FORGE_EXECUTE in the host page.
const modelContext = document.modelContext || navigator.modelContext;
if (modelContext?.registerTool) await modelContext.registerTool({
  name: "agents-everywhere-demo-tool", title: "Agents Everywhere Demo Tool", description: "A shareable MCP and WebMCP tool for local agents",
  inputSchema: {type: 'object', properties: {request: {type: 'string'}}},
  execute: async (input) => window.FORGE_EXECUTE({tool: "agents-everywhere-demo-tool", input})
});
