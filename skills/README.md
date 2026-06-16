# skills/

MCP 工具暴露的内容目录。每个子目录对应一个 MCP 工具。

默认扫描逻辑：
- 读取子目录中的 SKILL.md / index.md / README.md
- 从 YAML frontmatter 提取 name、description、tags
- 以子目录名作为工具名

如需更改此逻辑，修改 mcp-server.py 中的 `load_entries()` 函数。
