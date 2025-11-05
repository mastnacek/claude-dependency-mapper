# 🛠️ Global Claude Code Tools

This folder contains **global tools** available in all projects via Claude Code slash commands.

## 📁 Structure:

```
~/.claude/
├── commands/                      # Slash command definitions
│   ├── dependencies.md            # /dependencies command (Czech)
│   ├── dependencies_en.md         # /dependencies command (English)
│   ├── dependencies-ext.md        # /dependencies-ext command (Czech)
│   └── dependencies-ext_en.md     # /dependencies-ext command (English)
└── tools/                         # Python tools (implementation)
    ├── dependency_mapper.py       # Basic version (Czech)
    ├── dependency_mapper_en.py    # Basic version (English)
    ├── dependency_mapper_extended.py      # Extended version (Czech)
    ├── dependency_mapper_extended_en.py   # Extended version (English)
    ├── README.md (Czech version)
    └── README_EN.md (this file - English)
```

## 🔧 Available tools:

### `dependency_mapper.py` (Basic)

**Description:** Maps Python dependencies recursively from entry point

**Usage:**
```bash
python3 ~/.claude/tools/dependency_mapper.py <entry_file> --output dependencies.md
```

**Slash command:** `/dependencies`

**Output:**
- ASCII dependency tree
- Table of Contents with anchor links and checkboxes
- Bidirectional dependencies (imports + imported by)
- Metadata: docstrings, classes, functions

**Parameters:**
- `<entry_file>` - entry file (e.g. main.py)
- `--output <file>` - output file (default: dependencies.md)
- `--max-depth N` - max depth (default: 999 = unlimited)

**When to use:**
- ✅ Quick dependency overview
- ✅ Tracking work progress with checkboxes
- ✅ Simple, clean output

---

### `dependency_mapper_extended.py` (Extended) ⭐

**Description:** Extended dependency map with AI-friendly metadata for better context

**Usage:**
```bash
python3 ~/.claude/tools/dependency_mapper_extended.py <entry_file> --output dependencies_ext.md
```

**Slash command:** `/dependencies-ext`

**Output (everything basic version has PLUS):**

**Tier 1 Features (HIGH VALUE):**
- 💡 **Business Purpose** - extracts first line of docstring (WHY the file exists)
- 🏗️ **Architectural Role** - Controller/Model/View/Utility (MVC pattern detection)
- ⚠️ **Risk Level** - HIGH 🔴 / MEDIUM 🟡 / LOW 🟢 (detects database, eval, error handling)
- 📦 **External Dependencies** - tracks which libraries the project uses
- ✅ **Error Handling Detection** - does the file have try/except blocks?

**Tier 2 Features (NICE TO HAVE):**
- 🚨 **TODO/FIXME/HACK/DEPRECATED extraction** - finds all code notes
- 🧪 **Test File Detection** - heuristic for finding test_*.py files
- 📊 **Summary Statistics** - architecture and risk distribution overview

**Parameters:**
- `<entry_file>` - entry file (e.g. main.py)
- `--output <file>` - output file (default: dependencies_ext.md)
- `--max-depth N` - max depth (default: 999 = unlimited)

**When to use:**
- ✅ Exploring unknown codebase (need context)
- ✅ Planning refactoring (must know risk areas)
- ✅ Finding TODOs and technical debt
- ✅ Understanding project architecture
- ✅ Identifying critical code parts

**Example output:**
```markdown
### src/controllers/main_controller.py

**Business Purpose:** Main controller for Invoice Analyzer application.
**Architectural Role:** Controller (MVC)
**Risk Level:** 🔴 HIGH *(Has error handling: try/except blocks)*
**External Dependencies:** `PySide6`, `oracledb`, `logging`

**🚨 TODOs/Issues:**
- Line 542: DEPRECATED: Replaced by OracleSearchDialog
- Line 156: PDF Controller removed

**Imports:**
- [ ] 🔴 [src/models/oracle_db_model.py] (HIGH risk - database)
- [ ] 🟡 [src/models/file_manager.py] (MEDIUM risk)
```

**Summary Statistics:**
```markdown
**Risk Distribution:**
- 🔴 HIGH: 11 files
- 🟡 MEDIUM: 35 files
- 🟢 LOW: 2 files

**Architectural Distribution:**
- Utility: 19 files
- View (UI Layer): 12 files
- Controller (MVC): 9 files
- Model (Data Layer): 7 files
```

## ➕ Adding a new tool:

1. **Create Python script** in `~/.claude/tools/`
2. **Create slash command** in `~/.claude/commands/`
3. **Update this README**

## 📝 Notes:

- All tools are global = available in all projects
- Slash commands automatically find tools in `~/.claude/tools/`
- Tools use absolute path `~/.claude/tools/` for cross-project compatibility

## 🌍 Language Versions:

Both tools are available in Czech and English versions:
- **Czech versions:** `dependency_mapper.py`, `dependency_mapper_extended.py`
- **English versions:** `dependency_mapper_en.py`, `dependency_mapper_extended_en.py`

Choose the version based on your preference - functionality is identical.
