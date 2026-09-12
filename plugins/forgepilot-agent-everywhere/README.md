# ForgePilot Agent Everywhere

This Codex plugin packages the ForgePilot MCP server and bootstrap skill. It is designed to get a builder from a Codex conversation to a local awdk/Bonsai agent, a phone-installable PWA, and back to a reviewable artifact.

The same MCP identity can be used from desktop Codex/Claude, a trusted LAN phone, or an HTTPS PWA. The package deliberately keeps keys on the MCP host and treats the browser as a thin control surface.

Install from the repo-local marketplace after adding the marketplace directory to Codex. Start a new Codex task after installation so the MCP tool surface is discovered.
