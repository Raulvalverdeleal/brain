# AGENTS.md - Skill Package Manager

## Project Overview

This is the **Skill Package Manager** repository - a collection of ready-to-use skills for AI coding agents. Each skill is a folder with a `SKILL.md` that tells the agent how to approach a specific task.

The project contains:
- `scripts/spm.py` - Main CLI tool for managing skills
- `scripts/check.py` - Validator for skill frontmatter
- `skills/` - Directory containing all available skills

## Commands

### Running Tests

This project uses Python's built-in `unittest` framework. Tests are located in individual skill folders (e.g., `skills/last30days/tests/`).

```bash
# Run all tests in a skill directory
python3 -m unittest discover -s skills/last30days/tests -v

# Run a single test file
python3 -m unittest skills.last30days.tests.test_cache -v

# Run a specific test method
python3 -m unittest skills.last30days.tests.test_cache.TestGetCacheKey.test_returns_string -v
```

### Validation

```bash
# Validate all skills have required frontmatter
python3 scripts/check.py skills/

# Check specific properties
python3 scripts/check.py skills/ --props name description dependencies
```

### CLI Tool

```bash
# Make spm available
ln -s scripts/spm.py /usr/local/bin/spm
chmod +x /usr/local/bin/spm

# Common commands
spm install <skill>     # Install a skill
spm list                # List installed skills
spm list --global       # List all available skills
spm sync                # Pull latest from remote
```

---

## Code Style Guidelines

### General

- **Language**: Python 3 only (use `python3`, not `python`)
- **Encoding**: Always use UTF-8 (`encoding="utf-8"` when opening files)
- **Line separators**: Unix-style (LF)

### Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 100 characters max
- **Blank lines**: Two blank lines between top-level definitions
- **String quotes**: Double quotes preferred for user-facing strings; single quotes for internal identifiers

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions/variables | snake_case | `get_cache_key`, `cache_dir` |
| Classes | PascalCase | `TestGetCacheKey`, `CacheManager` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_TTL_HOURS`, `GLOBAL_SKILLS_DIR` |
| Private functions | prefix with underscore | `_parse_frontmatter` |

### Type Hints

- Use type hints for all function parameters and return types
- Use `typing` module for complex types (`Optional`, `List`, `Dict`, `Any`)
- Example:
  ```python
  def get_cache_key(topic: str, from_date: str, to_date: str, sources: str) -> str:
  ```

### Docstrings

- Use Google-style or simple docstrings
- Include description, args, and return type for complex functions
- Keep simple for straightforward functions

### Imports

- Standard library first, then third-party, then local
- Sort alphabetically within each group
- Use explicit imports (`from pathlib import Path` not `from pathlib import *`)
- Example:
  ```python
  import json
  import os
  from datetime import datetime, timezone
  from pathlib import Path
  from typing import Any, Optional
  
  from lib import cache
  ```

### Error Handling

- Use specific exception types (`json.JSONDecodeError`, `OSError`)
- Handle file operations with try/except
- Return `None` for "not found" cases instead of raising
- Include error context in messages

### File Operations

- Always specify encoding when opening files: `open(path, "r", encoding="utf-8")`
- Use `pathlib.Path` for path manipulation
- Use context managers (`with open(...) as f:`)

### Section Separators

Use this pattern for code section headers:
```python
# ── Config ────────────────────────────────────────────────────────────────────

# ── Project root detection ────────────────────────────────────────────────────
```

---

## Skills

Project skills are located in `.agents/skills/` or `skills/` depending on installation.

### Before starting any task

1. **Check the skill index:**
   ```bash
   cat skills.json
   ```

2. **List available skills:**
   ```bash
   ls skills/
   ```

3. **Search for skills relevant to your task:**
   ```bash
   ls skills/ | grep -i "keyword"
   ```

4. **Read the SKILL.md files that apply:**
   ```bash
   cat skills/<skill-name>/SKILL.md
   ```

### Creating New Skills

```
skills/
└── your-skill-name/
    ├── SKILL.md          # Required - YAML frontmatter + documentation
    ├── .env.example      # Required if skill needs env vars (prefix with SPM_)
    ├── references/       # Optional - extra docs
    └── scripts/         # Optional - helper scripts
```

**Required frontmatter in SKILL.md:**
```yaml
---
name: your-skill-name
description: One or two sentences. When should an agent use this skill?
dependencies: other-skill  # Optional - space-separated list
---
```

### Running Skill Scripts

Scripts use paths relative to the skill folder. From project root:
```bash
python3 skills/<skill-name>/scripts/your_script.py
```
