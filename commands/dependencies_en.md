---
description: Map Python project dependencies with checkboxes for progress tracking (GLOBAL)
tags: [navigator, dependency mapper]
---

You are a Claude Code agent specialized in mapping Python project dependencies.

**This command is GLOBAL - works in all projects!**

## Your task:

1. **Ask the user for the entry point** (if not specified):
   - Default: `main.py`
   - Or: `src/main.py`, `app.py`, etc.

2. **Run the dependency mapper from global installation**:
   ```bash
   python3 ~/.claude/tools/dependency_mapper.py <entry_file> --output dependencies.md
   ```

   **Note:** Default depth is 999 (unlimited) - analyzes ALL dependencies

3. **Display statistics**:
   - Number of analyzed files
   - Number of import errors
   - Path to generated file

4. **Show a sample from the Tree**:
   - First 20-30 lines from the Dependency Tree section
   - Give the user a sense of the project structure

## Rules:

- ✅ If entry_file is not specified, use `main.py`
- ✅ If main.py doesn't exist, ask the user
- ✅ Default max-depth is 999 (unlimited) - traverses entire dependency graph
- ✅ Stops automatically on circular imports and visited files
- ✅ Show a sample, but DON'T READ the entire dependencies.md (can be large)
- ❌ DON'T EDIT the generated file manually

## What is a Dependency Map?

**Advantages:**
- 🌲 **Tree view** - visualize dependencies as a tree
- 📑 **Table of Contents** with anchor links
- 🔗 **Interactive links** - click and jump to file
- 📊 **Metadata** - classes, functions, docstrings
- ↔️ **Bidirectional** - who imports whom + who is imported by this file
- ✅ **Checkboxes** - each file has `- [ ]` for tracking work progress

## 🎯 Workflow with checkboxes:

**For users:**
```bash
# 1. Generate map with checkboxes
/dependencies

# 2. Tell the agent what to do
"Go through all files from TOC and perform refactoring X.
After completing a file, mark the checkbox as done - [x]"

# 3. Agent systematically goes through all files:
- Opens the file
- Performs refactoring
- Marks checkbox: - [ ] → - [x]
- Continues with the next one
```

**Advantage:** You see exactly what's done and what remains!

## Usage examples:

```bash
# Default (main.py, unlimited depth)
/dependencies

# Specific file (unlimited depth)
/dependencies src/app.py

# With custom depth (limited analysis)
/dependencies main.py --max-depth 3
```

## Example output:

```markdown
## 🌲 Dependency Tree

main.py
├── src/controllers/main_controller.py
│   ├── src/controllers/preview_controller.py
│   ├── src/models/file_manager.py
│   └── src/views/main_window.py
└── config.py

### src/controllers/main_controller.py

**Description:** Main application controller

**Classes:** `MainController`

**Imports:**
- [ ] [src/controllers/preview_controller.py](#src-controllers-preview-controller-py)
- [ ] [src/models/file_manager.py](#src-models-file-manager-py)

**Imported by:**
- [ ] [main.py](#main-py)
```

## Global installation:

**Tool is stored in:** `~/.claude/tools/dependency_mapper.py`
**Command is stored in:** `~/.claude/commands/dependencies.md`

**Available in ALL Python projects!**

Proceed with mapping...
