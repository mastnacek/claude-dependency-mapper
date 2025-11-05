# 🛠️ Globální Claude Code Nástroje

Tato složka obsahuje **globální nástroje** dostupné ve všech projektech přes Claude Code slash commands.

## 📁 Struktura:

```
~/.claude/
├── commands/                      # Slash command definice
│   ├── dependencies.md            # /dependencies command (česky)
│   ├── dependencies_en.md         # /dependencies command (English)
│   ├── dependencies-ext.md        # /dependencies-ext command (česky)
│   └── dependencies-ext_en.md     # /dependencies-ext command (English)
└── tools/                         # Python nástroje (implementace)
    ├── dependency_mapper.py       # Základní verze (česky)
    ├── dependency_mapper_en.py    # Základní verze (English)
    ├── dependency_mapper_extended.py      # Rozšířená verze (česky)
    ├── dependency_mapper_extended_en.py   # Rozšířená verze (English)
    ├── README.md (tento soubor - česky)
    └── README_EN.md (English version)
```

## 🔧 Dostupné nástroje:

### `dependency_mapper.py` (Základní)

**Popis:** Mapuje Python závislosti rekurzivně od entry pointu

**Použití:**
```bash
python3 ~/.claude/tools/dependency_mapper.py <entry_file> --output dependencies.md
```

**Slash command:** `/dependencies`

**Výstup:**
- ASCII dependency tree
- Table of Contents s anchor linky s checkboxy
- Bidirectional dependencies (imports + imported by)
- Metadata: docstrings, classes, functions

**Parametry:**
- `<entry_file>` - vstupní soubor (např. main.py)
- `--output <file>` - výstupní soubor (default: dependencies.md)
- `--max-depth N` - max hloubka (default: 999 = unlimited)

**Kdy použít:**
- ✅ Rychlý přehled závislostí
- ✅ Tracking postupu práce s checkboxy
- ✅ Jednoduchý, čistý output

---

### `dependency_mapper_extended.py` (Rozšířená) ⭐

**Popis:** Rozšířená mapa závislostí s AI-friendly metadaty pro lepší kontext

**Použití:**
```bash
python3 ~/.claude/tools/dependency_mapper_extended.py <entry_file> --output dependencies_ext.md
```

**Slash command:** `/dependencies-ext`

**Výstup (vše co má basic verze PLUS):**

**Tier 1 Features (HIGH VALUE):**
- 💡 **Business Purpose** - extrahuje první řádek docstringu (WHY existuje soubor)
- 🏗️ **Architectural Role** - Controller/Model/View/Utility (MVC pattern detection)
- ⚠️ **Risk Level** - HIGH 🔴 / MEDIUM 🟡 / LOW 🟢 (detekce database, eval, error handling)
- 📦 **External Dependencies** - sleduje které knihovny projekt používá
- ✅ **Error Handling Detection** - má soubor try/except bloky?

**Tier 2 Features (NICE TO HAVE):**
- 🚨 **TODO/FIXME/HACK/DEPRECATED extraction** - najde všechny poznámky v kódu
- 🧪 **Test File Detection** - heuristika pro nalezení test_*.py souborů
- 📊 **Summary Statistics** - přehled architektury a risk distribution

**Parametry:**
- `<entry_file>` - vstupní soubor (např. main.py)
- `--output <file>` - výstupní soubor (default: dependencies_ext.md)
- `--max-depth N` - max hloubka (default: 999 = unlimited)

**Kdy použít:**
- ✅ Explorace neznámého codebase (potřebuješ kontext)
- ✅ Plánování refactoringu (musíš znát risk areas)
- ✅ Hledání TODOs a technical debt
- ✅ Porozumění architektuře projektu
- ✅ Identifikace kritických částí kódu

**Příklad výstupu:**
```markdown
### src/controllers/main_controller.py

**Business Purpose:** Hlavní kontroler aplikace Faktura Analyzer.
**Architectural Role:** Controller (MVC)
**Risk Level:** 🔴 HIGH *(Has error handling: try/except blocks)*
**External Dependencies:** `PySide6`, `oracledb`, `logging`

**🚨 TODOs/Issues:**
- Line 542: DEPRECATED: Nahrazeno OracleSearchDialog
- Line 156: PDF Controller odstraněn

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

## ➕ Přidání nového nástroje:

1. **Vytvoř Python skript** v `~/.claude/tools/`
2. **Vytvoř slash command** v `~/.claude/commands/`
3. **Aktualizuj tento README**

## 📝 Poznámky:

- Všechny nástroje jsou globální = dostupné ve všech projektech
- Slash commands automaticky najdou nástroje v `~/.claude/tools/`
- Nástroje používají absolutní cestu `~/.claude/tools/` pro cross-project kompatibilitu

## 🌍 Jazykové verze:

Oba nástroje jsou dostupné v české i anglické verzi:
- **České verze:** `dependency_mapper.py`, `dependency_mapper_extended.py`
- **Anglické verze:** `dependency_mapper_en.py`, `dependency_mapper_extended_en.py`

Vyberte si verzi podle preference - funkcionalita je identická.
