---
title: What is the /context Command in Claude Code
source: https://claudelog.com/faqs/what-is-context-command-in-claude-code/
author:
published: 2026-03-17
created: 2026-06-25
description: Claude Code /context command provides token usage breakdown across system components. Introduced in v1.0.86 for context engineering and optimization.
tags:
  - clippings
  - Claude
---
The `/context` slash command is a context inspection tool introduced in Claude Code v1.0.86 that shows an approximation of your context usage across different components. It displays token consumption and remaining context window percentage for strategic context optimization.

---

### How to Use It

Simply type `/context` in your Claude Code session to get a detailed breakdown of context usage across all system components.

```bash
/context
```

The command displays token usage for:

- **System Prompt** - Core instructions and behavior definitions
- **System tools** - Built-in Claude Code functionality
- **MCP tools** - Model Context Protocol server integrations
- **Memory files** - `CLAUDE.md` and project context
- **Custom Agents** - Specialized sub-agent definitions
- **Messages** - Current conversation history

### Why Use It

The `/context` command enables data-driven context engineering where you can optimize performance by understanding exactly how your context window is being consumed. This is essential for maintaining peak Claude Code performance throughout long sessions.

**Benefits:**

- **Token Visibility** - Clear breakdown of context consumption across all components
- **Strategic Optimization** - Make informed decisions about MCP tools and Custom Agents
- **Performance Engineering** - Identify context bloat before it impacts response quality
- **Baseline Awareness** - Understand fundamental context overhead for better planning
- **Interactive Analysis** - Ask Claude to review usage and suggest improvements

Use this tool to tactically enable/disable MCP tool functions and optimize Custom Agent efficiency with full knowledge of token consumption.

**MCP Server Management:**

Starting in v2.0.10, combine `/context` with dynamic MCP server control to optimize your context window. After checking token usage:

1. Identify MCP servers consuming tokens but not actively needed
2. Disable them with `@server-name disable` or via `/mcp` command
3. Run `/context` again to verify token savings
4. Re-enable when needed for specific tasks

Disabling unused MCP servers frees up context space for extended conversations and complex reasoning tasks.

### Actionable Suggestions (v2.1.74+)

The `/context` command now provides actionable optimization suggestions:

**What It Identifies:**

- **Context-heavy tools** - MCP tools consuming disproportionate token space
- **Memory bloat** - Overly large CLAUDE.md or memory files
- **Capacity warnings** - When approaching context limits
- **Optimization opportunities** - Specific steps to reclaim context space

**Example Output:**

```markdown
Context Usage: 847,234 / 1,000,000 tokens (84.7%)

⚠️ Suggestions:
• MCP server 'filesystem' uses 12% of context - consider disabling if not needed
• Memory file exceeds 50KB - review for outdated entries
• Consider compacting conversation history
```

These suggestions help maintain peak performance throughout long sessions.

> [!-success] -success
> Context Engineering Workflow
> 
> After running `/context`, ask Claude: "Where is my context potentially inefficient?" to get optimization suggestions and create a feedback loop for continuous improvement.

> [!-success] -success
> Strategic MCP Management
> 
> Use `/context` data to make informed decisions about which MCP tools provide sufficient value for their context overhead, eliminating guesswork from context optimization.

> [!-success] -success
> Context Engineering
> 
> Master context optimization by combining `/context` with [Plan Mode](https://claudelog.com/mechanics/plan-mode/) and [ultrathink](https://claudelog.com/faqs/what-is-ultrathink/) for comprehensive analysis: "Where is my context potentially inefficient and how can I optimize it?"
> 
> ![Custom image](https://cdn.claudelog.com/img/discovery/013_orange-686w.webp)

---

See Also: [Context Inspection](https://claudelog.com/mechanics/context-inspection/) | [Context Window Depletion](https://claudelog.com/mechanics/context-window-depletion/) | [Custom Agents](https://claudelog.com/mechanics/custom-agents/) | [Agent Engineering](https://claudelog.com/mechanics/agent-engineering/) | [MCP Server Setup](https://claudelog.com/faqs/how-to-setup-claude-code-mcp-servers/)