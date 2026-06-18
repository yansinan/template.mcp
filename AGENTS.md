# AGENTS.md — AI Agent 工作指南

本文档是 AI Agent（Hermes、Claude Code 等）在操作此仓库时的行为准则。

---

## 仓库范围

MCP 服务仓库模板。用于快速初始化一个新的 MCP 服务。

**目录结构：**

```
template.mcp/
├── mcp-server.py       # Stdio MCP 服务器（主入口）
├── skills/             # 内容目录（MCP 工具暴露的数据）
├── scripts/            # 辅助脚本
├── configs/            # 参考配置
├── docs/               # 文档与笔记
├── PRINCIPLES.md       # 仓库基本原则
├── AGENTS.md           # 本文件
└── README.md
```

---

## 基本原则

### 1. 官方文档优先

以各功能模块的 **官方文档** 为第一优先依据源。所有文档中的配置参数、命令、路径均应以官方文档为准，不得凭空杜撰。

### 2. 来源必注明

所有操作，**先有具体的来源出处，再执行**。每个配置项、每条命令、每个脚本，都必须在文档中注明来源 URL 或引用出处。

### 3. 来源优先级

```
官方文档（本地/线上） > 开源仓库 > 社区信息 > 技能注明的以往经验 > 其他网络信息
```

### 4. 不确定即查证

**不知道/不确定的马上去查线上/线下资料**，不要盲猜、乱测。

### 5. 定期同步

本地文档信息源安排定期同步线上官方文档来源。

---

## Agent 操作规范

### 定制 mcp-server.py

- 修改 `可定制区域` 内的常量（SERVER_INFO、CONTENT_DIR）
- 保持 MCP 协议主循环（`main()` 函数）不变
- 按需扩展 `load_entries()`、`handle_list_tools()`、`handle_call_tool()`

### 添加内容

- 每个内容条目一个子目录，内含 SKILL.md / index.md / README.md
- 支持分类目录嵌套（如 `back-end/deepseek-cost/`），`load_entries()` 会递归扫描
- 如需更改文件扫描逻辑，修改 `load_entries()`

### 搜索优先级

1. `man <component>` / `<command> --help`
2. 搜索 `<component> official documentation`
3. 搜索 `<component> <error/feature> site:github.com`
4. 本仓库已有内容
5. 其他网络搜索

---

*本文件需与 PRINCIPLES.md 保持一致。*
