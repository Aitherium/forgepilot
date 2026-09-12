# Security posture

ForgePilot is a hackathon artifact, not a finished internet-facing control plane.
This file states the boundary clearly.

## Default-safe behavior

- HTTP binds to `127.0.0.1` by default.
- Non-loopback HTTP refuses to start without `FORGEPILOT_MCP_TOKEN` and
  `FORGEPILOT_ALLOW_INSECURE_LAN=1`.
- `/mcp` is the only POST route. Requests are JSON-RPC 2.0, bounded to 1 MiB, and
  unknown tools/arguments fail closed.
- When a bearer token is configured, each tool also requires the scopes in
  `FORGEPILOT_MCP_SCOPES`; write-producing tools require `workspace.write`.
- Browser origins are allowlisted; wildcard CORS is not used.
- Device-flow state stores only a hash of the short-lived user code. It never stores
  an access token, and requested scopes are restricted to the known capability set.
- User input is length-bounded and model/profile names reject shell-control characters.
- Provider responses are size-bounded and provider keys are never written to generated
  packs or browser code.

## What this does not provide

- The stdio MCP server assumes the local client/process is trusted. Do not run it from
  an untrusted directory or hand its command to an unknown agent.
- The bearer token is not OAuth/OIDC and is not a replacement for awnboard/awiam.
  Use an HTTPS reverse proxy, private tunnel, or real Aitherium device-flow gateway for
  remote access.
- `FORGEPILOT_ALLOW_INSECURE_LAN=1` is for a trusted demo network only. It does not
  encrypt traffic.
- Generated connector artifacts contain local executable paths and are local handoff
  files. Review them before sharing; do not commit them with credentials or tokens.
- Hash manifests provide integrity evidence, not a cryptographic publisher signature.

## Release checklist

1. Run the test suite and inspect the generated artifact.
2. Use a fresh random token and explicit least-privilege scopes.
3. Put HTTPS and identity in front of remote MCP.
4. Review the exact client config before installing it into Codex or Claude.
5. Prove a real local/remote model round-trip; package detection is not runtime proof.
