import json
import os
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch

from aitherium_pack.server import Handler, mcp_response, call_tool
from aitherium_pack.artifacts import create_run
from aitherium_pack.cli import publish_static


class ForgePilotSmokeTests(unittest.TestCase):
    def test_initialize(self):
        response = mcp_response({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        self.assertEqual(response["result"]["serverInfo"]["name"], "forgepilot")

    def test_tools_are_read_only_demo_surface(self):
        response = mcp_response({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = {tool["name"] for tool in response["result"]["tools"]}
        self.assertEqual(names, {"forgepilot_health", "forgepilot_search", "forgepilot_chat", "forgepilot_generate_config", "forgepilot_create_artifact", "forgepilot_start_device_flow", "forgepilot_local_acceleration_plan", "forgepilot_create_shareable_pack", "forgepilot_create_connector_artifact", "forgepilot_backend_switch_plan", "forgepilot_community_bridge_plan", "forgepilot_create_community_bridge_pack"})
        self.assertNotIn("shell", json.dumps(response).lower())

    def test_offline_health(self):
        self.assertEqual(call_tool("forgepilot_health", {})["status"], "ok")

    def test_device_flow_is_consent_scoped(self):
        from pathlib import Path
        import shutil
        import uuid
        temp = Path.cwd() / ".test-artifacts" / ("device-" + uuid.uuid4().hex)
        try:
            result = call_tool("forgepilot_start_device_flow", {"scopes": ["mcp.tools"]})
            self.assertEqual(result["status"], "awaiting_user_consent")
            self.assertEqual(result["scopes"], ["mcp.tools"])
            self.assertNotIn("token", result)
        finally:
            shutil.rmtree(temp, ignore_errors=True)

    def test_local_acceleration_plan_is_read_only(self):
        plan = call_tool("forgepilot_local_acceleration_plan", {"model": "bonsai-27b"})
        self.assertEqual(plan["model"], "bonsai-27b")
        self.assertIn("awdk", plan["detected_commands"])
        self.assertIn("awnboard", plan["detected_commands"])
        self.assertIn("awbac", " ".join(plan["security_plane"]))
        self.assertIn("workspace.write", plan["capability_policy"])
        self.assertTrue(plan["commands"])

    def test_backend_switch_plan_is_read_only(self):
        plan = call_tool("forgepilot_backend_switch_plan", {"profile": "deepseek-flash"})
        self.assertEqual(plan["profile"], "deepseek-flash")
        self.assertEqual(plan["fast_alias"], "adk claude-model code")
        self.assertIn("adk claude-model check", " ".join(plan["commands"]))
        self.assertIn("awsettings", plan)

    def test_json_rpc_rejects_invalid_and_unknown_calls(self):
        invalid = mcp_response({"jsonrpc": "1.0", "id": 1, "method": "tools/list"})
        self.assertEqual(invalid["error"]["code"], -32600)
        unknown = mcp_response({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "shell"}})
        self.assertEqual(unknown["error"]["code"], -32602)

    def test_device_flow_rejects_privilege_escalation_scopes(self):
        with self.assertRaises(ValueError):
            call_tool("forgepilot_start_device_flow", {"scopes": ["admin", "shell"]})

    def test_text_inputs_are_bounded(self):
        with self.assertRaises(ValueError):
            call_tool("forgepilot_create_shareable_pack", {"name": "x", "description": "x" * 9000})
        with self.assertRaises(ValueError):
            call_tool("forgepilot_backend_switch_plan", {"profile": "../../shell"})

    def test_community_bridge_is_no_secrets_by_default(self):
        plan = call_tool("forgepilot_community_bridge_plan", {})
        self.assertEqual(plan["status"], "ready_to_connect")
        self.assertIn("arc", plan["surfaces"])
        self.assertIn("awrelay", plan["surfaces"])
        self.assertEqual(plan["security"]["default"], "read-only plan; no forum post, relay message, invite, or account mutation")

    def test_community_pack_contains_no_real_credentials(self):
        from pathlib import Path
        import shutil
        import uuid
        from aitherium_pack.community import create_community_bridge_pack
        temp = Path.cwd() / ".test-artifacts" / ("community-" + uuid.uuid4().hex)
        try:
            result = create_community_bridge_pack(output_root=temp)
            pack_dir = Path(result["path"])
            self.assertTrue((pack_dir / "relay-config.example.json").exists())
            self.assertIn("<never-commit>", (pack_dir / "relay-config.example.json").read_text())
            self.assertNotIn("Bearer ", "".join(path.read_text(encoding="utf-8") for path in pack_dir.iterdir() if path.is_file()))
        finally:
            shutil.rmtree(temp, ignore_errors=True)

    def test_http_mcp_requires_token_when_configured(self):
        from http.server import ThreadingHTTPServer
        import threading

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_address[1]}/mcp"
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}).encode()
        try:
            with patch.dict(os.environ, {"FORGEPILOT_MCP_TOKEN": "test-token"}, clear=False):
                request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
                with self.assertRaises(urllib.error.HTTPError) as missing:
                    urllib.request.urlopen(request)
                self.assertEqual(missing.exception.code, 401)
                request.add_header("Authorization", "Bearer test-token")
                with urllib.request.urlopen(request) as response:
                    self.assertEqual(response.status, 200)
        finally:
            server.shutdown()
            server.server_close()

    def test_http_capability_policy_fails_closed(self):
        from http.server import ThreadingHTTPServer
        import threading

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_address[1]}/mcp"
        body = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": "forgepilot_create_artifact", "arguments": {"request": "x"}},
        }).encode()
        try:
            with patch.dict(os.environ, {"FORGEPILOT_MCP_TOKEN": "test-token", "FORGEPILOT_MCP_SCOPES": "mcp.tools"}, clear=False):
                request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer test-token"}, method="POST")
                with urllib.request.urlopen(request) as response:
                    payload = json.loads(response.read())
                self.assertEqual(payload["error"]["code"], -32602)
                self.assertIn("workspace.write", payload["error"]["message"])
        finally:
            server.shutdown()
            server.server_close()

    def test_http_rejects_unlisted_browser_origin(self):
        from http.server import ThreadingHTTPServer
        import threading

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_address[1]}/mcp"
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}).encode()
        try:
            request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "Origin": "https://evil.example"}, method="POST")
            with self.assertRaises(urllib.error.HTTPError) as blocked:
                urllib.request.urlopen(request)
            self.assertEqual(blocked.exception.code, 403)
        finally:
            server.shutdown()
            server.server_close()

    def test_non_loopback_startup_requires_explicit_lan_opt_in(self):
        from aitherium_pack.server import serve
        with patch.dict(os.environ, {"FORGEPILOT_MCP_TOKEN": "", "FORGEPILOT_ALLOW_INSECURE_LAN": "0"}, clear=False):
            with self.assertRaises(RuntimeError):
                serve(host="0.0.0.0", port=0)

    def test_shareable_pack_has_all_surfaces(self):
        from pathlib import Path
        import shutil
        import uuid
        from aitherium_pack.sharing import create_shareable_pack
        temp = Path.cwd() / ".test-artifacts" / ("pack-" + uuid.uuid4().hex)
        try:
            result = create_shareable_pack("Demo Tool", "A tool anyone can apply.", temp)
            pack_dir = Path(result["path"])
            self.assertTrue((pack_dir / "pack.json").exists())
            self.assertTrue((pack_dir / "webmcp.js").exists())
            self.assertIn("awnboard", (pack_dir / "pack.json").read_text())
        finally:
            shutil.rmtree(temp, ignore_errors=True)

    def test_connector_artifact_has_client_installers(self):
        from pathlib import Path
        import shutil
        import uuid
        from aitherium_pack.connectors import create_connector_artifact
        temp = Path.cwd() / ".test-artifacts" / ("connector-" + uuid.uuid4().hex)
        try:
            result = create_connector_artifact(temp)
            connector_dir = Path(result["path"])
            self.assertTrue((connector_dir / "claude.mcp.json").exists())
            self.assertTrue((connector_dir / "codex.mcp.json").exists())
            self.assertTrue((connector_dir / "bootstrap-full.ps1").exists())
            self.assertIn("aitherium_pack", (connector_dir / "install.sh").read_text())
        finally:
            shutil.rmtree(temp, ignore_errors=True)
    def test_artifact_bundle_has_manifest(self):
        from pathlib import Path
        import shutil
        import uuid
        temp = Path.cwd() / ".test-artifacts" / uuid.uuid4().hex
        try:
            result = create_run("Create a safe MCP integration plan", temp)
            run_dir = Path(result["path"])
            self.assertTrue((run_dir / "report.md").exists())
            manifest = json.loads((run_dir / "manifest.json").read_text())
            self.assertIn("report.md", manifest["files"])
        finally:
            shutil.rmtree(temp, ignore_errors=True)

    def test_publish_contains_pwa_shell(self):
        from pathlib import Path
        import shutil
        import uuid
        temp = Path.cwd() / ".test-artifacts" / ("pwa-" + uuid.uuid4().hex)
        temp.mkdir(parents=True)
        try:
            publish_static(temp, "https://example.test/mcp")
            self.assertTrue((temp / "manifest.webmanifest").exists())
            self.assertTrue((temp / "sw.js").exists())
            self.assertIn("https://example.test/mcp", (temp / "config.js").read_text())
            index = (temp / "index.html").read_text()
            self.assertIn('href="./manifest.webmanifest"', index)
            self.assertIn('src="./config.js"', index)
            manifest = json.loads((temp / "manifest.webmanifest").read_text())
            self.assertEqual(manifest["start_url"], "./")
            self.assertIn("new URL('./', self.location)", (temp / "sw.js").read_text())
        finally:
            shutil.rmtree(temp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
