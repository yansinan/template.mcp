# template.mcp

MCP 服务仓库模板。作为子模块或独立仓库的上游模板，用于快速创建新的 MCP 服务。

## 目录结构

```
template.mcp/
├── mcp-server.py      # Stdio MCP 服务器骨架
├── PRINCIPLES.md      # 仓库基本原则（可覆盖）
├── AGENTS.md          # AI Agent 工作指南（可覆盖）
├── skills/            # MCP 工具暴露的内容目录
├── scripts/           # 辅助脚本
├── configs/           # 参考配置
├── docs/              # 文档与笔记
└── README.md
```

## 快速开始

### 1. fork / 复制此模板

```bash
# 作为新仓库
cp -r /path/to/template.mcp /path/to/new-repo
cd /path/to/new-repo

# 或作为子模块
cd ~/workspace/litellm.docker/mcps
git submodule add https://github.com/your/new-repo.git
```

### 2. 定制 mcp-server.py

编辑 `mcp-server.py` 中的 `可定制区域`：

```python
SERVER_INFO = {
    "name": "your-service-name",   # ← 改
    "version": "1.0.0",
}
CONTENT_DIR = HERE / "skills"       # ← 改为你实际的内容目录
```

然后按需求修改 `load_entries()`、`handle_list_tools()`、`handle_call_tool()`。

### 3. 填入内容

在 `skills/` 下创建你的内容目录。默认的文件扫描逻辑会读取子目录中的 `SKILL.md` / `index.md` / `README.md`。

### 4. 注册到 LiteLLM

```yaml
mcp_servers:
  your-service:
    transport: stdio
    command: python3
    args: [/mcps/your-service/mcp-server.py]
    allow_all_keys: true
```

如需 Docker 卷挂载：

```yaml
volumes:
  - ./mcps:/mcps
```

### 5. 验证

```bash
printf '{}' | python3 mcp-server.py   # 简单的连通性测试
# 完整 MCP 协议测试
echo '...' | python3 mcp-server.py
```

## 参考

- [MCP 协议规范](https://spec.modelcontextprotocol.io/)
- [LiteLLM MCP Gateway 文档](https://docs.litellm.ai/docs/mcp)
