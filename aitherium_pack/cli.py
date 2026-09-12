from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from .config import write_configs
from .server import serve, stdio_mcp


def _load_env() -> None:
    env_file = Path.cwd() / ".env"
    if not env_file.exists():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"'))


def publish_static(output: Path, mcp_endpoint: str = "/mcp") -> Path:
    """Build a host-agnostic PWA bundle for GitHub Pages or any static host."""
    web_root = Path(__file__).resolve().parent / "web"
    output.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "manifest.webmanifest", "sw.js", "icon.svg"):
        (output / name).write_bytes((web_root / name).read_bytes())
    (output / "config.js").write_text(
        f"window.FORGEPILOT_MCP_ENDPOINT = {json.dumps(mcp_endpoint)};\n",
        encoding="utf-8",
    )
    (output / "README.md").write_text(
        "# ForgePilot PWA\n\n"
        "This is the static phone/desktop UI. Open the page and set its MCP endpoint to an authenticated HTTPS MCP server. The endpoint is remembered in browser local storage; bearer tokens are kept in memory only.\n\n"
        "Deploy this folder with GitHub Pages, Netlify, Cloudflare Pages, or any static host. Configure the MCP server's CORS allowlist for the published page origin, and never expose an unauthenticated MCP server to the public internet.\n",
        encoding="utf-8",
    )
    return output


def main() -> None:
    _load_env()
    parser = argparse.ArgumentParser(prog="forgepilot")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("serve")
    sub.add_parser("mcp")
    sub.add_parser("config")
    run = sub.add_parser("run")
    run.add_argument("request")
    awdk = sub.add_parser("install-awdk")
    awdk.add_argument("--cloud", action="store_true")
    publish = sub.add_parser("publish", help="Build the installable PWA for a static host")
    publish.add_argument("--output", default="dist/agent-everywhere")
    publish.add_argument("--mcp-endpoint", default="/mcp")
    pack = sub.add_parser("pack", help="Scaffold a shareable MCP + WebMCP agent pack")
    pack.add_argument("name")
    pack.add_argument("description")
    connector = sub.add_parser("connector", help="Generate Claude Code and Codex connector scripts")
    args = parser.parse_args()
    if args.command == "serve":
        serve()
    elif args.command == "mcp":
        stdio_mcp()
    elif args.command == "config":
        print(json.dumps({str(path): "written" for path in write_configs()}, indent=2))
    elif args.command == "run":
        from .artifacts import create_run
        print(json.dumps(create_run(args.request), indent=2))
    elif args.command == "install-awdk":
        command = [sys.executable, "-m", "pip", "install", "awdk"]
        subprocess.run(command, check=True)
        quickstart = ["adk", "quickstart"] + (["--cloud"] if args.cloud else [])
        print(f"awdk installed. Continue with: {' '.join(quickstart)}")
    elif args.command == "publish":
        output = publish_static(Path(args.output), args.mcp_endpoint)
        print(json.dumps({"published": str(output.resolve()), "mcp_endpoint": args.mcp_endpoint}, indent=2))
    elif args.command == "pack":
        from .sharing import create_shareable_pack
        print(json.dumps(create_shareable_pack(args.name, args.description), indent=2))
    elif args.command == "connector":
        from .connectors import create_connector_artifact
        print(json.dumps(create_connector_artifact(), indent=2))


if __name__ == "__main__":
    main()
