# Agent Skills

A collection of specialized skill files designed to enhance AI coding assistants with domain-specific knowledge and capabilities.

## What Are Skills?

Skills are structured instruction sets that give AI agents (like Claude Code and OpenAI Codex) specialized knowledge for specific domains. They address gaps in LLM training data by providing:

- Current API references and usage patterns
- Working code examples and best practices
- Domain-specific workflows and techniques
- Quality guidelines and error handling strategies

## Available Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [interview](interview/) | In-depth interviewing to create detailed specs. Use when defining requirements, speccing out features, or articulating product details. Asks probing questions about technical implementation, UI/UX, concerns, and tradeoffs. | `npx skills add EnzeD/skills --skill interview` |
| [nano-banana-pro](nano-banana-pro/) | Image generation and editing using Google Gemini's Nano Banana Pro model. Supports text-to-image, image editing, multi-turn conversations, and transparency extraction via difference matting. | `npx skills add EnzeD/skills --skill nano-banana-pro` |
| [spec-reviewer](spec-reviewer/) | Review and challenge spec documents against your project's codebase, best practices, and guidelines. Spawns a team of parallel agents to analyze consistency, code reuse, performance, scope, and testability. | `npx skills add EnzeD/skills --skill spec-reviewer` |

## Installation

Install a specific skill:

```bash
npx skills add EnzeD/skills --skill <skill-name>
```

### Manual Installation

Copy the skill folder to your project's skill directory:

**Claude Code:**
```bash
cp -r nano-banana-pro .claude/skills/
```

**OpenAI Codex:**
```bash
cp -r nano-banana-pro .codex/skills/
```

## Skill Structure

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md           # Main skill instructions (required)
├── references/        # Additional documentation
│   └── *.md
└── scripts/           # Helper scripts and utilities
    └── *.py
```

## Contributing

Contributions are welcome! When editing a skill:

1. Update the `SKILL.md` with improved instructions or new capabilities
2. Add or modify supporting files in `references/` and `scripts/` as needed
3. Test your changes to ensure the skill works correctly

## License

MIT License - feel free to use these skills in your projects.
