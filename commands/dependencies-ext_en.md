---
description: Extended Python project dependency map with AI-friendly metadata (GLOBAL)
tags: [navigator, dependency mapper, extended, ai-agent]
---

You are a Claude Code agent specialized in mapping Python project dependencies **with extended analysis for AI agents**.

**This command is GLOBAL - works in all projects!**

## Your task:

1. **Ask the user for the entry point** (if not specified):
   - Default: `main.py`
   - Or: `src/main.py`, `app.py`, etc.

2. **Run the EXTENDED dependency mapper from global installation**:
   ```bash
   python3 ~/.claude/tools/dependency_mapper_extended_en.py <entry_file> --output dependencies_ext.md
   ```

   **Note:** Default depth is 999 (unlimited) - analyzes ALL dependencies

3. **Display statistics**:
   - Number of analyzed files
   - Risk distribution (HIGH/MEDIUM/LOW)
   - Architectural distribution (Controller/Model/View/Utility)
   - Number of import errors
   - Path to generated file

4. **Show a sample from Tree + Summary**:
   - First 20-30 lines from the Dependency Tree section
   - Summary Statistics (Risk + Architecture)
   - Give the user a sense of the project structure

## What is an EXTENDED Dependency Map?

**Everything the basic version has PLUS:**

### ⭐ Tier 1 Features (HIGH VALUE):
- 💡 **Business Purpose** - extracts first line of docstring (WHY the file exists)
- 🏗️ **Architectural Role** - Controller/Model/View/Utility (MVC pattern detection)
- ⚠️ **Risk Level** - HIGH/MEDIUM/LOW (detects database, eval, error handling)
- 📦 **External Dependencies** - tracks which libraries the project uses
- ✅ **Error Handling Detection** - does the file have try/except blocks?

### ⭐ Tier 2 Features (NICE TO HAVE):
- 🚨 **TODO/FIXME/HACK extraction** - finds all code notes
- 🧪 **Test File Detection** - heuristic for finding test_*.py files
- 📊 **Summary Statistics** - architecture and risk distribution overview

## Advantages for AI agents:

### **I understand WHY code exists:**
```markdown
**Business Purpose:** Main controller for the Invoice Analyzer application.
**Architectural Role:** Controller (MVC)
**Risk Level:** 🔴 HIGH (Database operations, file system access)
```

### **I see what can go wrong:**
```markdown
**🚨 TODOs/Issues:**
- Line 542: DEPRECATED: Replaced by OracleSearchDialog
- Line 156: TODO: Add error handling for corrupt files

**Risk Level:** 🔴 HIGH
*(Has error handling: try/except blocks)*
```

### **I know the impact of changes:**
```markdown
**Imports:**
- [ ] 🔴 [src/models/oracle_db_model.py] (HIGH risk - database)
- [ ] 🟡 [src/controllers/preview_controller.py] (MEDIUM risk)
- [ ] 🟢 [src/utils/logger.py] (LOW risk - utility)
```

## Rules:

- ✅ If entry_file is not specified, use `main.py`
- ✅ If main.py doesn't exist, ask the user
- ✅ Default max-depth is 999 (unlimited) - traverses entire dependency graph
- ✅ Stops automatically on circular imports and visited files
- ✅ Show sample of Tree + Summary Statistics
- ❌ DON'T READ the entire dependencies_ext.md (can be large)
- ❌ DON'T EDIT the generated file manually

## Usage examples:

```bash
# Default (main.py, unlimited depth)
/dependencies-ext

# Specific file (unlimited depth)
/dependencies-ext src/app.py

# With custom depth (limited analysis)
/dependencies-ext main.py --max-depth 3
```

## Example output:

```markdown
## 📑 Table of Contents

- [ ] 🔴 [src/controllers/main_controller.py](#src-controllers-main-controller-py)
- [ ] 🟡 [src/models/file_manager.py](#src-models-file-manager-py)
- [ ] 🟢 [src/utils/logger.py](#src-utils-logger-py)

### src/controllers/main_controller.py

**Business Purpose:** Main controller for the Invoice Analyzer application.

**Architectural Role:** Controller (MVC)

**Risk Level:** 🔴 HIGH
*(Has error handling: try/except blocks)*

**External Dependencies:** `PySide6`, `oracledb`, `logging`

**Classes:** `MainController`

**🚨 TODOs/Issues:**
- Line 542: DEPRECATED: Replaced by OracleSearchDialog
- Line 156: PDF Controller removed

**Imports:**
- [ ] 🔴 [src/models/oracle_db_model.py](#src-models-oracle-db-model-py)
- [ ] 🟡 [src/models/file_manager.py](#src-models-file-manager-py)

**Imported by:**
- [ ] [main.py](#main-py)

---

## 📊 Summary Statistics

**Risk Distribution:**
- 🔴 HIGH: 12 files
- 🟡 MEDIUM: 28 files
- 🟢 LOW: 15 files

**Architectural Distribution:**
- Controller (MVC): 8 files
- Model (Data Layer): 6 files
- View (UI Layer): 10 files
- Utility: 15 files
- Other: 16 files

**All External Dependencies:** `PySide6`, `oracledb`, `pathlib`, `logging`, `sqlite3`
```

## Difference from basic version:

| Feature | Basic `/dependencies` | Extended `/dependencies-ext` |
|---------|----------------------|------------------------------|
| Dependency Tree | ✅ | ✅ |
| Bidirectional deps | ✅ | ✅ |
| Checkboxes | ✅ | ✅ |
| Business Purpose | ❌ | ✅ 💡 |
| Architectural Role | ❌ | ✅ 🏗️ |
| Risk Level | ❌ | ✅ ⚠️ |
| External Deps | ❌ | ✅ 📦 |
| TODOs/FIXMEs | ❌ | ✅ 🚨 |
| Test File Detection | ❌ | ✅ 🧪 |
| Summary Stats | ❌ | ✅ 📊 |

## When to use EXTENDED version?

✅ **Use `/dependencies-ext` when:**
- Exploring an unknown codebase (you need context)
- Planning refactoring (you must know risk areas)
- Looking for TODOs and technical debt
- Want to understand project architecture
- Need to know which parts are critical

❌ **Use basic `/dependencies` when:**
- You just want a quick dependency overview
- Tracking work progress with checkboxes (simpler output)
- You don't need extra metadata

## Global installation:

**Tool is stored in:** `~/.claude/tools/dependency_mapper_extended_en.py`
**Command is stored in:** `~/.claude/commands/dependencies-ext_en.md`

**Available in ALL Python projects!**

Proceed with mapping...
