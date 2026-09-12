# 2-minute demo — one take, screen recording (OBS / QuickTime / Loom)

Record the launcher test itself. No slides. Have these open before you hit record:
a browser on https://aitherium.github.io/forgepilot/ , an empty Downloads folder,
Claude Code closed. Total ≈ 2:30. Cut anything that waits.

## 0:00 – 0:20  Hook (browser on the page)
> "Agents shouldn't live in a chatbox. This puts one in the places you already work — your terminal, your IDE, your phone — in one click. Watch a blank Windows machine."

## 0:20 – 0:40  Click
Click **Windows — download & open**. Open the file. SmartScreen → *More info → Run anyway*.
> "That's a 1 KB launcher. It runs AitherZero's playbooks — every step is a numbered script you can read on GitHub."

## 0:40 – 1:20  Install (speed up 4× in editing, or just talk over it)
As the log scrolls:
> "PowerShell 7, Python, Git, Node, gh, then `adk` and `awsh`. Every step verifies for real — it runs the binary, not just checks a file — and every step is idempotent: re-run to repair."
Stop the speed-up on the **verify table** and the **DEV WORKSTATION READY** banner. Hold 3 s.

## 1:20 – 1:50  Connect
`connect` starts: browser tab opens for sign-in → approve.
> "Device-flow sign-in to Aitherium, inference check, and it writes the MCP config for Claude Code and proves the gateway answers."
Hold on **"IDE 'claude-code' wired to the remote MCP gateway"** and the **CONNECTED** banner.

## 1:50 – 2:20  Payoff — the agent where the work is
New terminal, `cd` into a real project, type `awsh`, ask ONE thing that needs local context, e.g.
`what changed in this repo today and is anything running on port 8787`
> "The terminal is the environment: it sees cwd, env, git, running processes. No chatbox has that."
Then open Claude Code in that folder → show the Aitherium MCP server already listed.

## 2:20 – 2:30  Close
Back to the page. Point at macOS / Linux-Termux buttons.
> "Same one click on Mac, Linux, and an Android phone with Termux. Open source: AitherZero, awdk, awsh, ForgePilot. Agents, everywhere."

## Upload
YouTube → Unlisted → title "AI Tinkerers Agents Everywhere — Aitherium demo" → paste URL in the form.

## If something fails on camera
Say "re-run repairs" and re-run the launcher — it's true and it's the pitch. Don't cut it.
