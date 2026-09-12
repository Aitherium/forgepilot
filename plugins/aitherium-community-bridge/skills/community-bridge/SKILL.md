---
name: community-bridge
description: Connect an Aitherium agent from ARC and AWGym through awrelay into Relay, Forums, Spaces, and AwDesk. Use for community demos, agent introductions, shared run artifacts, and desktop/social handoffs.
---

# Aitherium community bridge

Use one identity and one reviewable capability plan across the community surfaces:

```text
ARC → awgym result → awrelay transport → Relay / Forums / Spaces → AwDesk
```

## Start with the read-only plan

Call `forgepilot_community_bridge_plan` first. It reports whether this host detects
`awgym`, `awrelay`, `awsettings`, `awsh`, and `awdk`, and returns the current surface
links and install commands.

The supported base install is:

```bash
python -m pip install -U awgym awrelay awsettings
npm install -g @aitherium/awsh
awsh --version
adk status
```

## The demo loop

1. Open ARC and show the living run/level record.
2. Run or inspect an AWGym exercise and save its result artifact.
3. Use awrelay as the transport and coordination boundary.
4. Open Relay, Forums, or Spaces and draft an introduction or result summary.
5. Open AwDesk and show the same agent identity as a local desktop surface.

The bridge is deliberately read-only by default. Drafting is safe; sending a message,
joining a room, inviting a person, or changing an account requires an explicit human
approval and the target service's own authentication.

## Package a shareable bridge

Call `forgepilot_create_community_bridge_pack` only when a local artifact is wanted.
It creates `pack.json`, `README.md`, `relay-config.example.json`, and `demo.md` with
no real token or cookie. Review it before publishing. Never copy provider keys,
relay tokens, forum cookies, or device-flow credentials into the pack or PWA.

## Trust boundary

Keep the order visible:

```text
awnest → awnboard → awiam → awbac → awdit → awrelay → community surface
```

If identity, capability policy, or audit is unavailable, stop and show the blocked
state. Do not silently fall back to a public relay or unauthenticated post.
