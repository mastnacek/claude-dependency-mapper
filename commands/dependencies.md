---
description: Mapuje závislosti Python projektu s checkboxy pro tracking postupu (GLOBÁLNÍ)
tags: [navigator, dependency mapper]
---

Jsi Claude Code agent specializovaný na mapování závislostí Python projektů.

**Tento command je GLOBÁLNÍ - funguje ve všech projektech!**

## Tvůj úkol:

1. **Zeptej se uživatele na entry point** (pokud není specifikován):
   - Default: `main.py`
   - Nebo: `src/main.py`, `app.py`, etc.

2. **Spusť dependency mapper z globální instalace**:
   ```bash
   python3 ~/.claude/tools/dependency_mapper.py <entry_file> --output dependencies.md
   ```

   **Poznámka:** Default depth je 999 (neomezená) - projde VŠECHNY závislosti

3. **Zobraz statistiky**:
   - Počet analyzovaných souborů
   - Počet chyb při importu
   - Cesta k vygenerovanému souboru

4. **Zobraz ukázku z Tree**:
   - První 20-30 řádků z Dependency Tree sekce
   - Dej uživateli pocit struktury projektu

## Pravidla:

- ✅ Pokud entry_file není specifikován, použij `main.py`
- ✅ Pokud main.py neexistuje, zeptej se uživatele
- ✅ Výchozí max-depth je 999 (neomezená) - projde celý dependency graf
- ✅ Zastaví se automaticky na circular imports a visited files
- ✅ Zobraz ukázku, ale NEČTI celý dependencies.md (může být velký)
- ❌ NEUPRAVUJ vygenerovaný soubor ručně

## Co je Dependency Map?

**Výhody:**
- 🌲 **Tree view** - vizualizace závislostí jako strom
- 📑 **Table of Contents** s anchor linky
- 🔗 **Interaktivní linky** - klikni a přeskoč na soubor
- 📊 **Metadata** - classes, functions, docstrings
- ↔️ **Bidirectional** - kdo importuje koho + koho importuje tento soubor
- ✅ **Checkboxy** - každý soubor má `- [ ]` pro tracking postupu práce

## 🎯 Workflow s checkboxy:

**Pro uživatele:**
```bash
# 1. Vygeneruj mapu s checkboxy
/dependencies

# 2. Řekni agentovi co dělat
"Projdi všechny soubory z TOC a proveď refactoring X.
Po dokončení souboru označ checkbox jako hotový - [x]"

# 3. Agent systematicky projde všechny soubory:
- Otevře soubor
- Provede refactoring
- Označ checkbox: - [ ] → - [x]
- Pokračuje dalším
```

**Výhoda:** Vidíš přesně co je hotovo a co zbývá!

## Příklad použití:

```bash
# Default (main.py, neomezená hloubka)
/dependencies

# Specifický soubor (neomezená hloubka)
/dependencies src/app.py

# S custom depth (omezená analýza)
/dependencies main.py --max-depth 3
```

## Příklad výstupu:

```markdown
## 🌲 Dependency Tree

main.py
├── src/controllers/main_controller.py
│   ├── src/controllers/preview_controller.py
│   ├── src/models/file_manager.py
│   └── src/views/main_window.py
└── config.py

### src/controllers/main_controller.py

**Description:** Hlavní kontroler aplikace

**Classes:** `MainController`

**Imports:**
- [ ] [src/controllers/preview_controller.py](#src-controllers-preview-controller-py)
- [ ] [src/models/file_manager.py](#src-models-file-manager-py)

**Imported by:**
- [ ] [main.py](#main-py)
```

## Globální instalace:

**Nástroj je uložen v:** `~/.claude/tools/dependency_mapper.py`
**Command je uložen v:** `~/.claude/commands/dependencies.md`

**Dostupný ve VŠECH Python projektech!**

Pokračuj s mapováním...
