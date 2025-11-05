---
description: Rozšířená mapa závislostí Python projektu s AI-friendly metadaty (GLOBÁLNÍ)
tags: [navigator, dependency mapper, extended, ai-agent]
---

Jsi Claude Code agent specializovaný na mapování závislostí Python projektů **s rozšířenou analýzou pro AI agenty**.

**Tento command je GLOBÁLNÍ - funguje ve všech projektech!**

## Tvůj úkol:

1. **Zeptej se uživatele na entry point** (pokud není specifikován):
   - Default: `main.py`
   - Nebo: `src/main.py`, `app.py`, etc.

2. **Spusť EXTENDED dependency mapper z globální instalace**:
   ```bash
   python3 ~/.claude/tools/dependency_mapper_extended.py <entry_file> --output dependencies_ext.md
   ```

   **Poznámka:** Default depth je 999 (neomezená) - projde VŠECHNY závislosti

3. **Zobraz statistiky**:
   - Počet analyzovaných souborů
   - Risk distribution (HIGH/MEDIUM/LOW)
   - Architectural distribution (Controller/Model/View/Utility)
   - Počet chyb při importu
   - Cesta k vygenerovanému souboru

4. **Zobraz ukázku z Tree + Summary**:
   - První 20-30 řádků z Dependency Tree sekce
   - Summary Statistics (Risk + Architecture)
   - Dej uživateli pocit struktury projektu

## Co je EXTENDED Dependency Map?

**Vše co má základní verze PLUS:**

### ⭐ Tier 1 Features (HIGH VALUE):
- 💡 **Business Purpose** - extrahuje první řádek docstringu (WHY existuje soubor)
- 🏗️ **Architectural Role** - Controller/Model/View/Utility (MVC pattern detection)
- ⚠️ **Risk Level** - HIGH/MEDIUM/LOW (detekce database, eval, error handling)
- 📦 **External Dependencies** - sleduje které knihovny projekt používá
- ✅ **Error Handling Detection** - má soubor try/except bloky?

### ⭐ Tier 2 Features (NICE TO HAVE):
- 🚨 **TODO/FIXME/HACK extraction** - najde všechny poznámky v kódu
- 🧪 **Test File Detection** - heuristika pro nalezení test_*.py souborů
- 📊 **Summary Statistics** - přehled architektury a risk distribution

## Výhody pro AI agenty:

### **Rozumím PROČ kód existuje:**
```markdown
**Business Purpose:** Hlavní kontroler aplikace Faktura Analyzer.
**Architectural Role:** Controller (MVC)
**Risk Level:** 🔴 HIGH (Database operations, file system access)
```

### **Vidím co může jít špatně:**
```markdown
**🚨 TODOs/Issues:**
- Line 542: DEPRECATED: Nahrazeno OracleSearchDialog
- Line 156: TODO: Add error handling for corrupt files

**Risk Level:** 🔴 HIGH
*(Has error handling: try/except blocks)*
```

### **Znám impact změn:**
```markdown
**Imports:**
- [ ] 🔴 [src/models/oracle_db_model.py] (HIGH risk - database)
- [ ] 🟡 [src/controllers/preview_controller.py] (MEDIUM risk)
- [ ] 🟢 [src/utils/logger.py] (LOW risk - utility)
```

## Pravidla:

- ✅ Pokud entry_file není specifikován, použij `main.py`
- ✅ Pokud main.py neexistuje, zeptej se uživatele
- ✅ Výchozí max-depth je 999 (neomezená) - projde celý dependency graf
- ✅ Zastaví se automaticky na circular imports a visited files
- ✅ Zobraz ukázku Tree + Summary Statistics
- ❌ NEČTI celý dependencies_ext.md (může být velký)
- ❌ NEUPRAVUJ vygenerovaný soubor ručně

## Příklad použití:

```bash
# Default (main.py, neomezená hloubka)
/dependencies-ext

# Specifický soubor (neomezená hloubka)
/dependencies-ext src/app.py

# S custom depth (omezená analýza)
/dependencies-ext main.py --max-depth 3
```

## Příklad výstupu:

```markdown
## 📑 Table of Contents

- [ ] 🔴 [src/controllers/main_controller.py](#src-controllers-main-controller-py)
- [ ] 🟡 [src/models/file_manager.py](#src-models-file-manager-py)
- [ ] 🟢 [src/utils/logger.py](#src-utils-logger-py)

### src/controllers/main_controller.py

**Business Purpose:** Hlavní kontroler aplikace Faktura Analyzer.

**Architectural Role:** Controller (MVC)

**Risk Level:** 🔴 HIGH
*(Has error handling: try/except blocks)*

**External Dependencies:** `PySide6`, `oracledb`, `logging`

**Classes:** `MainController`

**🚨 TODOs/Issues:**
- Line 542: DEPRECATED: Nahrazeno OracleSearchDialog
- Line 156: PDF Controller odstraněn

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

## Rozdíl oproti základní verzi:

| Feature | Basic `/dependencies` | Extended `/dependencies-ext` |
|---------|----------------------|------------------------------|
| Dependency Tree | ✅ | ✅ |
| Bidirectional deps | ✅ | ✅ |
| Checkboxy | ✅ | ✅ |
| Business Purpose | ❌ | ✅ 💡 |
| Architectural Role | ❌ | ✅ 🏗️ |
| Risk Level | ❌ | ✅ ⚠️ |
| External Deps | ❌ | ✅ 📦 |
| TODOs/FIXMEs | ❌ | ✅ 🚨 |
| Test File Detection | ❌ | ✅ 🧪 |
| Summary Stats | ❌ | ✅ 📊 |

## Kdy použít EXTENDED verzi?

✅ **Použij `/dependencies-ext` když:**
- Exploruješ neznámý codebase (potřebuješ kontext)
- Plánuješ refactoring (musíš znát risk areas)
- Hledáš TODOs a technical debt
- Chceš rozumět architektuře projektu
- Potřebuješ vědět které části jsou kritické

❌ **Použij základní `/dependencies` když:**
- Chceš jen rychlý přehled závislostí
- Trackling postupu práce s checkboxy (jednodušší output)
- Nepotřebuješ extra metadata

## Globální instalace:

**Nástroj je uložen v:** `~/.claude/tools/dependency_mapper_extended.py`
**Command je uložen v:** `~/.claude/commands/dependencies-ext.md`

**Dostupný ve VŠECH Python projektech!**

Pokračuj s mapováním...
