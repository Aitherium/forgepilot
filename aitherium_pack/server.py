from __future__ import annotations

import json
import hmac
import os
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .config import configs
from .artifacts import create_run
from .auth import start_device_flow
from .local_stack import acceleration_plan
from .sharing import create_shareable_pack
from .connectors import create_connector_artifact
from .backend_profiles import switch_plan
from .community import community_bridge_plan, create_community_bridge_pack
from .providers import exa_search, openrouter_chat
from .security import MAX_HTTP_BODY, allowed_origins, bearer_token, is_loopback, validated_scopes


ROOT = Path(__file__).resolve().parent
TOOLS = [
    {
        "name": "forgepilot_health",
        "description": "Return the local ForgePilot runtime status. Read-only.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "forgepilot_search",
        "description": "Search the web with Exa and return compact, untrusted highlights with source URLs.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string", "minLength": 3}, "num_results": {"type": "integer", "minimum": 1, "maximum": 10}},
            "required": ["query"],
        },
    },
    {
        "name": "forgepilot_chat",
        "description": "Answer an integration question using optional Exa evidence through OpenRouter. Read-only.",
        "inputSchema": {"type": "object", "properties": {"message": {"type": "string", "minLength": 1}, "evidence": {"type": "array"}}, "required": ["message"]},
    },
    {
        "name": "forgepilot_generate_config",
        "description": "Generate portable MCP client configuration snippets. Read-only.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "forgepilot_create_artifact",
        "description": "Create a timestamped, read-only integration run bundle with evidence, response, report, and SHA-256 manifest.",
        "inputSchema": {"type": "object", "properties": {"request": {"type": "string", "minLength": 1}}, "required": ["request"]},
    },
    {
        "name": "forgepilot_start_device_flow",
        "description": "Create a consent-scoped Aitherium device-flow handoff for local inference, MCP, workspace, and LAN capabilities. No token is returned.",
        "inputSchema": {"type": "object", "properties": {"scopes": {"type": "array", "items": {"type": "string"}}}},
    },
    {
        "name": "forgepilot_local_acceleration_plan",
        "description": "Inspect local aw* command/package presence and return the Bonsai model activation plan for Codex and Claude Code. Read-only.",
        "inputSchema": {"type": "object", "properties": {"model": {"type": "string"}}},
    },
    {
        "name": "forgepilot_create_shareable_pack",
        "description": "Scaffold a portable MCP + WebMCP + PWA agent tool pack with awnboard/awiam/awbac/awdit metadata.",
        "inputSchema": {"type": "object", "properties": {"name": {"type": "string", "minLength": 1}, "description": {"type": "string", "minLength": 1}}, "required": ["name", "description"]},
    },
    {
        "name": "forgepilot_create_connector_artifact",
        "description": "Generate runnable Claude Code and Codex MCP configs plus bootstrap scripts for the current local checkout.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "forgepilot_backend_switch_plan",
        "description": "Show the safe adk/awsettings plan for switching Claude Code to a provider such as DeepSeek Flash. Read-only.",
        "inputSchema": {"type": "object", "properties": {"profile": {"type": "string"}}},
    },
    {
        "name": "forgepilot_community_bridge_plan",
        "description": "Show the safe ARC, awgym, awrelay, Relay, Forums, Spaces, and AwDesk connection plan. Read-only.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "forgepilot_create_community_bridge_pack",
        "description": "Create a no-secrets community bridge artifact for ARC, awgym, awrelay, Relay, Spaces, and AwDesk.",
        "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}},
    },
]

TOOL_SCOPES = {
    "forgepilot_health": {"mcp.tools"},
    "forgepilot_search": {"mcp.tools"},
    "forgepilot_chat": {"mcp.tools"},
    "forgepilot_generate_config": {"mcp.tools", "workspace.read"},
    "forgepilot_create_artifact": {"mcp.tools", "workspace.write"},
    "forgepilot_start_device_flow": {"mcp.tools", "lan.control"},
    "forgepilot_local_acceleration_plan": {"mcp.tools", "workspace.read"},
    "forgepilot_create_shareable_pack": {"mcp.tools", "workspace.write"},
    "forgepilot_create_connector_artifact": {"mcp.tools", "workspace.write"},
    "forgepilot_backend_switch_plan": {"mcp.tools"},
    "forgepilot_community_bridge_plan": {"mcp.tools"},
    "forgepilot_create_community_bridge_pack": {"mcp.tools", "workspace.write"},
}


def _enforce_tool_scope(name: str) -> None:
    if bearer_token() is None:
        return
    raw = os.getenv("FORGEPILOT_MCP_SCOPES", "mcp.tools")
    granted = set(validated_scopes([item.strip() for item in raw.split(",") if item.strip()], ["mcp.tools"]))
    required = TOOL_SCOPES.get(name, {"mcp.tools"})
    if not required.issubset(granted):
        missing = ", ".join(sorted(required - granted))
        raise ValueError(f"capability scope required: {missing}")


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "forgepilot_health":
        return {"status": "ok", "pack": "forgepilot", "version": "0.1.0", "providers": {"exa": bool(os.getenv("EXA_API_KEY")), "openrouter": bool(os.getenv("OPENROUTER_API_KEY"))}}
    if name == "forgepilot_search":
        return exa_search(str(arguments.get("query", "")), int(arguments.get("num_results", 5)))
    if name == "forgepilot_chat":
        return openrouter_chat(str(arguments.get("message", "")), arguments.get("evidence", []))
    if name == "forgepilot_generate_config":
        return {"configs": configs(), "note": "Review the target client's current config path before installing."}
    if name == "forgepilot_create_artifact":
        return create_run(str(arguments.get("request", "")))
    if name == "forgepilot_start_device_flow":
        scopes = arguments.get("scopes")
        return start_device_flow(scopes if isinstance(scopes, list) else None)
    if name == "forgepilot_local_acceleration_plan":
        return acceleration_plan(str(arguments.get("model", "bonsai-27b")))
    if name == "forgepilot_create_shareable_pack":
        return create_shareable_pack(str(arguments.get("name", "Agent Tool")), str(arguments.get("description", "A shareable agent tool.")))
    if name == "forgepilot_create_connector_artifact":
        return create_connector_artifact()
    if name == "forgepilot_backend_switch_plan":
        return switch_plan(str(arguments.get("profile", "deepseek-flash")))
    if name == "forgepilot_community_bridge_plan":
        return community_bridge_plan()
    if name == "forgepilot_create_community_bridge_pack":
        return create_community_bridge_pack(str(arguments.get("name", "Aitherium Community Bridge")))
    raise ValueError(f"unknown tool: {name}")


def mcp_response(request: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(request, dict) or request.get("jsonrpc") != "2.0":
        return {"jsonrpc": "2.0", "id": request.get("id") if isinstance(request, dict) else None, "error": {"code": -32600, "message": "invalid JSON-RPC request"}}
    method = request.get("method")
    request_id = request.get("id")
    if method == "notifications/initialized":
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"protocolVersion": "2025-06-18", "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": "forgepilot", "version": "0.1.0"}}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = request.get("params") or {}
        try:
            if not isinstance(params, dict) or not isinstance(params.get("name"), str):
                raise ValueError("tools/call requires a tool name")
            if params["name"] not in {tool["name"] for tool in TOOLS}:
                raise ValueError("unknown tool")
            arguments = params.get("arguments") or {}
            if not isinstance(arguments, dict):
                raise ValueError("tool arguments must be an object")
            _enforce_tool_scope(params["name"])
            result = call_tool(params["name"], arguments)
            content = [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]
            return {"jsonrpc": "2.0", "id": request_id, "result": {"content": content, "structuredContent": result}}
        except ValueError as exc:
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": str(exc)}}
        except Exception:
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32000, "message": "tool execution failed"}}
    if request_id is not None:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"method not found: {method}"}}
    return None


class Handler(BaseHTTPRequestHandler):
    server_version = "ForgePilot/0.1"

    def _origin_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        return not origin or origin in allowed_origins(self.server.server_address[1])

    def _authorized(self) -> bool:
        expected = bearer_token()
        if expected is None:
            return True
        supplied = self.headers.get("Authorization", "")
        if not supplied.startswith("Bearer "):
            return False
        return hmac.compare_digest(supplied[7:].strip(), expected)

    def _security_headers(self) -> dict[str, str]:
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Cache-Control": "no-store",
        }
        origin = self.headers.get("Origin")
        if origin and origin in allowed_origins(self.server.server_address[1]):
            headers["Access-Control-Allow-Origin"] = origin
            headers["Vary"] = "Origin"
        return headers

    def _reject(self, status: int, message: str) -> None:
        self._write(status, {"error": message})

    def _write(self, status: int, payload: object, content_type: str = "application/json") -> None:
        body = json.dumps(payload).encode("utf-8") if content_type == "application/json" else payload
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for name, value in self._security_headers().items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        if not self._origin_allowed():
            self._reject(403, "origin not allowed")
            return
        self.send_response(204)
        for name, value in self._security_headers().items():
            self.send_header(name, value)
        self.send_header("Access-Control-Allow-Headers", "authorization, content-type, mcp-session-id")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._write(200, call_tool("forgepilot_health", {}))
            return
        if path in {"/", "/index.html"}:
            self._write(200, (ROOT / "web" / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        static_types = {
            "/manifest.webmanifest": ("manifest.webmanifest", "application/manifest+json"),
            "/sw.js": ("sw.js", "application/javascript"),
            "/icon.svg": ("icon.svg", "image/svg+xml"),
            "/config.js": ("config.js", "application/javascript"),
        }
        if path in static_types:
            filename, content_type = static_types[path]
            file_path = ROOT / "web" / filename
            if file_path.exists():
                self._write(200, file_path.read_bytes(), content_type)
                return
        if path == "/api/tools":
            if not self._origin_allowed():
                self._reject(403, "origin not allowed")
                return
            if not self._authorized():
                self._reject(401, "MCP authorization required")
                return
            self._write(200, {"tools": TOOLS})
            return
        self._write(404, {"error": "not found"})

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/mcp":
            self._reject(404, "not found")
            return
        if not self._origin_allowed():
            self._reject(403, "origin not allowed")
            return
        if not self._authorized():
            self.send_response(401)
            self.send_header("WWW-Authenticate", "Bearer")
            for name, value in self._security_headers().items():
                self.send_header(name, value)
            self.end_headers()
            return
        try:
            raw_length = self.headers.get("Content-Length", "0")
            length = int(raw_length)
            if length < 0 or length > MAX_HTTP_BODY:
                self._reject(413, "request body too large")
                return
            request = json.loads(self.rfile.read(length) or b"{}")
            response = mcp_response(request)
            if response is None:
                self.send_response(202)
                self.end_headers()
            else:
                self._write(200, response)
        except (ValueError, json.JSONDecodeError):
            self._reject(400, "invalid request")
        except Exception:
            self._reject(500, "request failed")

    def log_message(self, format: str, *args: object) -> None:
        print(f"[forgepilot] {format % args}")


def serve(host: str | None = None, port: int | None = None) -> None:
    bind = host or os.getenv("FORGEPILOT_HOST", "127.0.0.1")
    listen_port = port or int(os.getenv("FORGEPILOT_PORT", "8787"))
    if not is_loopback(bind):
        if bearer_token() is None:
            raise RuntimeError("non-loopback MCP requires FORGEPILOT_MCP_TOKEN")
        if os.getenv("FORGEPILOT_ALLOW_INSECURE_LAN") != "1":
            raise RuntimeError("non-loopback HTTP is disabled; set FORGEPILOT_ALLOW_INSECURE_LAN=1 only on a trusted LAN or use HTTPS")
    print(f"ForgePilot control room: http://{bind}:{listen_port}")
    print("MCP endpoint: /mcp (JSON-RPC over HTTP) | stdio: python -m aitherium_pack mcp")
    ThreadingHTTPServer((bind, listen_port), Handler).serve_forever()


def stdio_mcp() -> None:
    import sys
    for line in sys.stdin:
        if not line.strip():
            continue
        response = mcp_response(json.loads(line))
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
