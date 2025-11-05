#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dependency Mapper - Mapuje závislosti Python projektu od vstupního souboru.
Generuje interaktivní Markdown mapu s linky na skutečné soubory.

Usage:
    python3 dependency_mapper.py main.py [--max-depth 3] [--output dependencies.md]
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field


@dataclass
class FileNode:
    """Reprezentace souboru v dependency grafu."""
    path: Path
    relative_path: str
    imports: List[str] = field(default_factory=list)
    imported_by: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)


class DependencyMapper:
    """Mapuje závislosti Python projektu rekurzivně."""

    def __init__(self, root_dir: Path, max_depth: int = 999):
        self.root_dir = root_dir
        self.max_depth = max_depth
        self.visited: Set[str] = set()
        self.nodes: Dict[str, FileNode] = {}
        self.import_errors: List[str] = []

    def resolve_import_path(self, import_name: str, from_file: Path) -> Optional[Path]:
        """
        Převede import na absolutní cestu k souboru.

        Examples:
            'src.controllers.main_controller' -> src/controllers/main_controller.py
            'config' -> config.py
            '.preview_controller' -> src/controllers/preview_controller.py (relativní)
        """
        # Relativní import (začíná tečkou)
        if import_name.startswith('.'):
            parent_dir = from_file.parent
            relative_parts = import_name.lstrip('.').split('.')
            resolved_path = parent_dir / '/'.join(relative_parts)
        else:
            # Absolutní import
            parts = import_name.split('.')
            resolved_path = self.root_dir / '/'.join(parts)

        # Zkusíme různé varianty
        candidates = [
            resolved_path.with_suffix('.py'),
            resolved_path / '__init__.py',
        ]

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate

        return None

    def extract_imports(self, file_path: Path) -> List[str]:
        """Extrahuje všechny importy ze souboru pomocí AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
        except (SyntaxError, FileNotFoundError, UnicodeDecodeError) as e:
            self.import_errors.append(f"{file_path}: {e}")
            return []

        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # from module import x
                    imports.append(node.module)
                elif node.level > 0:
                    # from . import x (relativní)
                    imports.append('.' * node.level)

        return imports

    def extract_metadata(self, file_path: Path) -> tuple:
        """Extrahuje docstring, classes a functions ze souboru."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
        except (SyntaxError, FileNotFoundError, UnicodeDecodeError):
            return None, [], []

        docstring = ast.get_docstring(tree)
        classes = []
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                # Pouze top-level funkce (ne metody)
                functions.append(node.name)

        return docstring, classes, functions

    def map_dependencies(self, entry_file: Path, depth: int = 0) -> FileNode:
        """Rekurzivně mapuje závislosti od vstupního souboru."""
        # Relativní cesta pro klíč
        try:
            relative_path = str(entry_file.relative_to(self.root_dir))
        except ValueError:
            # Soubor je mimo root_dir
            relative_path = str(entry_file)

        # Kontrola zda jsme soubor už nenavštívili
        if relative_path in self.visited or depth > self.max_depth:
            return self.nodes.get(relative_path)

        self.visited.add(relative_path)
        print(f"{'  ' * depth}📄 Mapuji: {relative_path}", file=sys.stderr)

        # Extrakce importů a metadat
        imports = self.extract_imports(entry_file)
        docstring, classes, functions = self.extract_metadata(entry_file)

        # Vytvoření nodu
        node = FileNode(
            path=entry_file,
            relative_path=relative_path,
            docstring=docstring,
            classes=classes,
            functions=functions
        )
        self.nodes[relative_path] = node

        # Rekurzivní zpracování importů
        for import_name in imports:
            resolved_path = self.resolve_import_path(import_name, entry_file)

            if resolved_path and resolved_path.exists():
                try:
                    import_relative = str(resolved_path.relative_to(self.root_dir))
                except ValueError:
                    import_relative = str(resolved_path)

                node.imports.append(import_relative)

                # Rekurzivně mapujeme importovaný soubor
                child_node = self.map_dependencies(resolved_path, depth + 1)

                if child_node and import_relative in self.nodes:
                    self.nodes[import_relative].imported_by.append(relative_path)

        return node

    def generate_markdown(self, entry_file: str, output_file: Path):
        """Generuje Markdown dokumentaci dependency grafu."""
        lines = [
            f"# 📊 Dependency Map",
            "",
            f"**Entry point:** [{entry_file}]({entry_file})",
            f"**Root directory:** `{self.root_dir}`",
            f"**Max depth:** {self.max_depth}",
            f"**Files analyzed:** {len(self.nodes)}",
            "",
            "---",
            "",
        ]

        # Table of Contents
        lines.extend([
            "## 📑 Table of Contents",
            "",
        ])

        for relative_path in sorted(self.nodes.keys()):
            anchor = relative_path.replace('/', '-').replace('.', '-').replace('_', '-')
            lines.append(f"- [ ] [{relative_path}](#{anchor})")

        lines.extend(["", "---", ""])

        # Dependency Tree (od entry point)
        lines.extend([
            "## 🌲 Dependency Tree",
            "",
            "```",
        ])

        entry_relative = str(Path(entry_file).relative_to(self.root_dir)) if Path(entry_file).is_absolute() else entry_file
        self._generate_tree(entry_relative, lines, visited=set(), prefix="", is_last=True)

        lines.extend([
            "```",
            "",
            "---",
            "",
        ])

        # Detailní informace o každém souboru
        lines.extend([
            "## 📄 File Details",
            "",
        ])

        for relative_path in sorted(self.nodes.keys()):
            node = self.nodes[relative_path]
            anchor = relative_path.replace('/', '-').replace('.', '-').replace('_', '-')

            lines.extend([
                f"### {relative_path} {{#{anchor}}}",
                "",
                f"**Path:** [{relative_path}]({relative_path})",
                "",
            ])

            # Docstring
            if node.docstring:
                first_line = node.docstring.split('\n')[0].strip()
                lines.append(f"**Description:** {first_line}")
                lines.append("")

            # Classes
            if node.classes:
                class_list = ", ".join(f"`{c}`" for c in node.classes[:5])
                if len(node.classes) > 5:
                    class_list += f" ... +{len(node.classes) - 5} more"
                lines.append(f"**Classes:** {class_list}")
                lines.append("")

            # Functions
            if node.functions:
                func_list = ", ".join(f"`{f}()`" for f in node.functions[:5])
                if len(node.functions) > 5:
                    func_list += f" ... +{len(node.functions) - 5} more"
                lines.append(f"**Functions:** {func_list}")
                lines.append("")

            # Imports (tento soubor importuje)
            if node.imports:
                lines.append("**Imports:**")
                for imp in sorted(node.imports):
                    imp_anchor = imp.replace('/', '-').replace('.', '-').replace('_', '-')
                    lines.append(f"- [ ] [{imp}](#{imp_anchor})")
                lines.append("")

            # Imported by (kdo importuje tento soubor)
            if node.imported_by:
                lines.append("**Imported by:**")
                for imp_by in sorted(node.imported_by):
                    imp_by_anchor = imp_by.replace('/', '-').replace('.', '-').replace('_', '-')
                    lines.append(f"- [ ] [{imp_by}](#{imp_by_anchor})")
                lines.append("")

            lines.extend(["---", ""])

        # Chyby při importu
        if self.import_errors:
            lines.extend([
                "## ⚠️ Import Errors",
                "",
            ])
            for error in self.import_errors:
                lines.append(f"- {error}")
            lines.append("")

        # Zápis do souboru
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"✅ Dependency map vygenerována: {output_file}", file=sys.stderr)

    def _generate_tree(self, file_path: str, lines: List[str], visited: Set[str], prefix: str, is_last: bool):
        """Rekurzivně generuje ASCII tree."""
        if file_path in visited or file_path not in self.nodes:
            return

        visited.add(file_path)
        node = self.nodes[file_path]

        # Symbol pro větev
        branch = "└── " if is_last else "├── "
        lines.append(f"{prefix}{branch}{file_path}")

        # Prefix pro děti
        child_prefix = prefix + ("    " if is_last else "│   ")

        # Rekurzivně projdeme importy
        imports = [imp for imp in node.imports if imp not in visited]
        for i, imp in enumerate(imports):
            is_last_child = (i == len(imports) - 1)
            self._generate_tree(imp, lines, visited, child_prefix, is_last_child)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 dependency_mapper.py <entry_file> [--max-depth N] [--output file.md]")
        print("Example: python3 dependency_mapper.py main.py --output dependencies.md")
        print("Note: Default max-depth is 999 (unlimited)")
        sys.exit(1)

    entry_file = Path(sys.argv[1])
    max_depth = 999  # Neomezená hloubka (zastaví se pouze na circular imports nebo visited files)
    output_file = Path("dependencies.md")

    # Parsování argumentů
    if "--max-depth" in sys.argv:
        idx = sys.argv.index("--max-depth")
        max_depth = int(sys.argv[idx + 1])

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_file = Path(sys.argv[idx + 1])

    if not entry_file.exists():
        print(f"❌ Soubor neexistuje: {entry_file}", file=sys.stderr)
        sys.exit(1)

    # Detekce root directory (hledáme .git nebo pyproject.toml)
    root_dir = entry_file.parent
    for parent in entry_file.parents:
        if (parent / '.git').exists() or (parent / 'pyproject.toml').exists():
            root_dir = parent
            break

    print(f"🔍 Mapuji závislosti od: {entry_file}", file=sys.stderr)
    print(f"📁 Root directory: {root_dir}", file=sys.stderr)
    print(f"⚙️  Max depth: {max_depth}", file=sys.stderr)
    print("", file=sys.stderr)

    # Mapování
    mapper = DependencyMapper(root_dir, max_depth)
    mapper.map_dependencies(entry_file)

    # Generování Markdown
    mapper.generate_markdown(str(entry_file.relative_to(root_dir)), output_file)

    print("", file=sys.stderr)
    print(f"📊 Statistiky:", file=sys.stderr)
    print(f"  - Soubory: {len(mapper.nodes)}", file=sys.stderr)
    print(f"  - Chyby: {len(mapper.import_errors)}", file=sys.stderr)


if __name__ == "__main__":
    main()
