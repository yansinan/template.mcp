#!/usr/bin/env python3
"""
template.mcp MCP Server — 通用的 Stdio MCP 服务器骨架。

协议：MCP JSON-RPC over stdio（符合 MCP 2025-03-26 规范）
生命周期：
  1. client → initialize → server → InitializeResult
  2. client → initialized (notification, 无需回复)
  3. client → tools/list → server → tools[]
  4. client → tools/call → server → content[]

===== ⚠️ 定制指南 =====
使用此模板创建新 MCP 仓库时：

1. 修改 SERVER_INFO["name"] 和 SERVER_INFO["version"]
2. 修改 CONTENT_DIR 指向你仓库的内容目录
3. 修改 load_entries() 函数扫描你的内容结构
4. 修改 handle_list_tools() 暴露哪些工具
5. 修改 handle_call_tool() 返回什么内容
6. 按需扩展 CAPABILITIES（添加 resources / prompts 支持）
======================
"""

import json
import sys
from pathlib import Path

# ==================== 可定制区域 ====================

# 服务器元信息
SERVER_INFO = {
    "name": "template-mcp",       # ← 改为你的服务名
    "version": "1.0.0",           # ← 改为你的版本号
}

# 服务器能力声明（仅 tools 时保留此结构，如需 resources/prompts 请扩展）
CAPABILITIES = {
    "tools": {},
}

# 内容根目录（脚本所在目录下的 skills/，可按需修改）
HERE = Path(__file__).resolve().parent
CONTENT_DIR = HERE / "skills"

# ==================== 内容加载逻辑 ====================

def load_entries(base: Path) -> list[dict]:
    """
    扫描内容目录，返回条目元信息列表。

    ⚠️ 如需改为其他文件结构（SQLite、API、本地 JSON 等），修改此函数。
    默认实现：扫描 base/ 下的子目录，读取每个子目录的 index.md
    作为条目描述。
    """
    if not base.is_dir():
        return []

    entries = []
    for sub in sorted(base.iterdir()):
        if not sub.is_dir():
            continue
        # 查找 index.md 或 SKILL.md 或 README.md 作为描述源
        desc_file = None
        for name in ("SKILL.md", "index.md", "README.md"):
            if (sub / name).is_file():
                desc_file = sub / name
                break
        if not desc_file:
            continue

        text = desc_file.read_text(encoding="utf-8")
        desc = ""
        tags = []
        for line in text.splitlines():
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
            if line.startswith("tags:"):
                raw = line.split(":", 1)[1].strip()
                if raw.startswith("["):
                    raw = raw.strip("[]")
                tags = [t.strip().strip('"').strip("'") for t in raw.split(",") if t.strip()]
            if line.startswith("---") and desc:
                break

        entries.append({
            "name": sub.name,
            "description": desc or f"条目: {sub.name}",
            "path": str(desc_file),
            "tags": tags,
        })
    return entries


def handle_list_tools() -> dict:
    """返回工具列表（每个目录条目对应一个工具）"""
    entries = load_entries(CONTENT_DIR)
    tools = []
    for e in entries:
        tools.append({
            "name": e["name"],
            "description": e["description"],
            "inputSchema": {
                "type": "object",
                "properties": {
                    # ⚠️ 如需自定义参数，在此扩展
                },
                "required": [],
            },
        })
    return {"tools": tools}


def handle_call_tool(name: str, arguments: dict) -> dict:
    """
    调用指定工具，返回条目内容。

    ⚠️ 如需不同的返回值格式（如 JSON 结构化数据、二进制 base64 等），修改此函数。
    """
    entries = load_entries(CONTENT_DIR)
    matched = None
    for e in entries:
        if e["name"] == name:
            matched = e
            break
    if not matched:
        return {"content": [{"type": "text", "text": f"条目 '{name}' 未找到"}], "isError": True}

    path = Path(matched["path"])
    text = path.read_text(encoding="utf-8")

    # ⚠️ 如需支持子参数（ref、list_refs 等），在此扩展

    return {"content": [{"type": "text", "text": text}]}


# ==================== MCP 协议主循环 ====================
# ⚠️ 除非要修改协议流程，否则以下通常不需要改动

MCP_PROTOCOL_VERSION = "2025-03-26"


def main():
    """MCP stdio 协议主循环：读 stdin JSON-RPC，写 stdout JSON-RPC"""
    initialized = False
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = req.get("method", "")
        req_id = req.get("id")

        # MCP 初始化握手
        if method == "initialize":
            params = req.get("params", {})
            client_version = params.get("protocolVersion", MCP_PROTOCOL_VERSION)
            resp = {
                "jsonrpc": "2.0", "id": req_id,
                "result": {
                    "protocolVersion": client_version,
                    "capabilities": CAPABILITIES,
                    "serverInfo": SERVER_INFO,
                },
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
            continue

        # initialized notification — 无需回复
        if method == "notifications/initialized":
            initialized = True
            continue

        params = req.get("params", {})

        if method == "tools/list":
            result = handle_list_tools()
        elif method == "tools/call":
            name = params.get("name", "")
            arguments = params.get("arguments", {})
            result = handle_call_tool(name, arguments)
        else:
            resp = {
                "jsonrpc": "2.0", "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
            continue

        resp = {"jsonrpc": "2.0", "id": req_id, "result": result}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
