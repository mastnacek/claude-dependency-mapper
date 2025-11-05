# 🛠️ Claude Dependency Mapper

**Bilingual Python dependency mapping tools for Claude Code with AI-friendly metadata analysis**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.com/claude-code)

> Systematically map and analyze Python project dependencies with interactive Markdown documentation, checkboxes for progress tracking, and AI-friendly metadata extraction.

## 🌍 Available in Two Languages

All tools and documentation are available in both **Czech** (Čeština) and **English**:
- 🇨🇿 Czech versions for Czech-speaking developers
- 🇬🇧 English versions for international use

Choose your preferred language - functionality is identical!

---

## 📚 Available Commands

| Command | Description | Czech | English |
|---------|-------------|-------|---------|
| `/dependencies` | Basic dependency mapper with checkboxes | [📖 CZ Docs](commands/dependencies.md) | [📖 EN Docs](commands/dependencies_en.md) |
| `/dependencies-ext` | Extended mapper with AI metadata analysis | [📖 CZ Docs](commands/dependencies-ext.md) | [📖 EN Docs](commands/dependencies-ext_en.md) |

### Quick Feature Comparison

| Feature | Basic | Extended |
|---------|-------|----------|
| ASCII Dependency Tree | ✅ | ✅ |
| Table of Contents with Links | ✅ | ✅ |
| Bidirectional Dependencies | ✅ | ✅ |
| Progress Checkboxes | ✅ | ✅ |
| **Business Purpose** | ❌ | ✅ 💡 |
| **Architectural Role Detection** | ❌ | ✅ 🏗️ |
| **Risk Level Analysis** | ❌ | ✅ ⚠️ |
| **External Dependencies** | ❌ | ✅ 📦 |
| **TODO/FIXME Extraction** | ❌ | ✅ 🚨 |
| **Test File Detection** | ❌ | ✅ 🧪 |
| **Summary Statistics** | ❌ | ✅ 📊 |

---

## 🚀 Quick Start

### 1. Installation

Copy tools to your global Claude Code directory:

```bash
# Linux/Mac
cp -r commands/* ~/.claude/commands/
cp -r tools/* ~/.claude/tools/

# Windows
copy commands\* %USERPROFILE%\.claude\commands\
copy tools\* %USERPROFILE%\.claude\tools\
```

### 2. Usage in Claude Code

**Basic mapping:**
```bash
/dependencies
# or with specific file:
/dependencies src/main.py
```

**Extended mapping with AI metadata:**
```bash
/dependencies-ext
# or with specific file:
/dependencies-ext src/main.py
```

### 3. Direct CLI Usage

You can also run the tools directly:

```bash
# Basic version
python3 ~/.claude/tools/dependency_mapper.py main.py --output dependencies.md

# Extended version
python3 ~/.claude/tools/dependency_mapper_extended.py main.py --output dependencies_ext.md
```

---

## 📖 Documentation

### For Users
- **[Tools README (CZ)](tools/README.md)** - Detailed tool documentation in Czech
- **[Tools README (EN)](tools/README_EN.md)** - Detailed tool documentation in English

### For Contributors
- See [Contributing](#-contributing) section below

---

## ✨ Key Features

### 🌲 Visual Dependency Tree
```
main.py
├── src/controllers/main_controller.py
│   ├── src/controllers/preview_controller.py
│   ├── src/models/file_manager.py
│   └── src/views/main_window.py
└── config.py
```

### ✅ Progress Tracking with Checkboxes
```markdown
## Table of Contents
- [ ] [main.py](#main-py)
- [ ] [src/controllers/main_controller.py](#src-controllers-main-controller-py)
- [x] [config.py](#config-py)  ← Mark as done!
```

### 🎯 AI-Friendly Metadata (Extended Version)
```markdown
**Business Purpose:** Main controller for Invoice Analyzer application.
**Architectural Role:** Controller (MVC)
**Risk Level:** 🔴 HIGH (Database operations, file system access)
**External Dependencies:** `PySide6`, `oracledb`, `logging`

**🚨 TODOs/Issues:**
- Line 542: DEPRECATED: Replaced by OracleSearchDialog
- Line 156: TODO: Add error handling for corrupt files
```

---

## 🎯 Use Cases

### 📋 Basic Version (`/dependencies`)
- ✅ Quick dependency overview
- ✅ Tracking refactoring progress with checkboxes
- ✅ Understanding project structure
- ✅ Simple, clean output

### ⭐ Extended Version (`/dependencies-ext`)
- ✅ Exploring unknown codebases (need context)
- ✅ Planning refactoring (must know risk areas)
- ✅ Finding TODOs and technical debt
- ✅ Understanding project architecture
- ✅ Identifying critical code sections

---

## 🛠️ Technical Details

### Requirements
- Python 3.7+
- No external dependencies (uses stdlib only)
- Works on Linux, macOS, and Windows

### Supported Features
- ✅ Recursive dependency analysis
- ✅ Circular import detection
- ✅ Relative and absolute imports
- ✅ AST-based code parsing
- ✅ Markdown output with anchor links
- ✅ Configurable depth limiting
- ✅ Error handling and reporting

---

## 📂 Repository Structure

```
claude-dependency-mapper/
├── README.md (this file)
│
├── commands/                          # Claude Code slash commands
│   ├── dependencies.md                # Basic command (CZ)
│   ├── dependencies_en.md             # Basic command (EN)
│   ├── dependencies-ext.md            # Extended command (CZ)
│   └── dependencies-ext_en.md         # Extended command (EN)
│
└── tools/                             # Python implementation
    ├── README.md                      # Tool documentation (CZ)
    ├── README_EN.md                   # Tool documentation (EN)
    ├── dependency_mapper.py           # Basic tool (CZ)
    ├── dependency_mapper_en.py        # Basic tool (EN)
    ├── dependency_mapper_extended.py  # Extended tool (CZ)
    └── dependency_mapper_extended_en.py # Extended tool (EN)
```

---

## 🤝 Contributing

Contributions are welcome! When adding new commands:

1. **Create the tool** in `tools/` directory
2. **Create slash command** in `commands/` directory
3. **Add both Czech and English versions**
4. **Update this README** with new command in the table
5. **Update tools/README.md** with documentation
6. **Submit a Pull Request**

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built for [Claude Code](https://claude.com/claude-code)
- Inspired by the need for better Python dependency visualization
- Made with ❤️ by [@mastnacek](https://github.com/mastnacek)

---

## 📮 Support

- **Issues:** [GitHub Issues](https://github.com/mastnacek/claude-dependency-mapper/issues)
- **Discussions:** [GitHub Discussions](https://github.com/mastnacek/claude-dependency-mapper/discussions)

---

**🤖 Generated with [Claude Code](https://claude.com/claude-code)**
