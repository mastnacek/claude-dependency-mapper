#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dependency Mapper Extended - Rozšířená verze s analýzou pro AI agenty.
Mapuje závislosti Python projektu a extrahuje metadata pro lepší kontext.

Nové features:
- Business Purpose (z docstringů)
- Architectural Role (Controller/Model/View/Utility)
- Risk Level (HIGH/MEDIUM/LOW)
- External Dependencies tracking
- TODO/FIXME/HACK/DEPRECATED extraction
- Test file detection

Usage:
    python3 dependency_mapper_extended.py main.py [--max-depth 3] [--output dependencies_ext.md]
"""

import ast
import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field


@dataclass
class FileNode:
    """Reprezentace souboru v dependency grafu s rozšířenými metadaty."""
    path: Path
    relative_path: str
    imports: List[str] = field(default_factory=list)
    imported_by: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)

    # ⭐ NOVÉ FIELDS pro AI agenty:
    business_purpose: Optional[str] = None        # První řádek docstringu
    architectural_role: Optional[str] = None      # Controller/Model/View/Utility
    risk_level: Optional[str] = None              # HIGH/MEDIUM/LOW
    external_deps: List[str] = field(default_factory=list)  # Externí knihovny
    todos: List[str] = field(default_factory=list)          # TODO/FIXME komentáře
    test_file: Optional[str] = None               # Cesta k test souboru
    has_error_handling: bool = False              # Obsahuje try/except


class DependencyMapperExtended:
    """Mapuje závislosti Python projektu rekurzivně s rozšířenou analýzou."""

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

    # ⭐ NOVÉ METODY pro rozšířenou analýzu:

    def extract_business_purpose(self, file_path: Path) -> Optional[str]:
        """
        Extrahuje business purpose z prvního řádku module docstringu.

        Args:
            file_path: Cesta k Python souboru

        Returns:
            První řádek docstringu nebo None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            docstring = ast.get_docstring(tree)
            if docstring:
                # První řádek = business purpose
                first_line = docstring.split('\n')[0].strip()
                # Odstraníme prázdné řádky na začátku
                for line in docstring.split('\n'):
                    line = line.strip()
                    if line:
                        return line
                return first_line if first_line else None
        except:
            pass
        return None

    def detect_architectural_role(self, file_path: Path) -> str:
        """
        Detekuje architekturu podle cesty a naming conventions.

        Args:
            file_path: Cesta k souboru

        Returns:
            String s rolí: "Controller", "Model", "View", "Utility", atd.
        """
        path_str = str(file_path).lower().replace('\\', '/')
        filename = file_path.name.lower()

        # MVC Pattern detection
        if 'controller' in path_str or filename.endswith('_controller.py'):
            return "Controller (MVC)"
        elif 'model' in path_str or filename.endswith('_model.py'):
            return "Model (Data Layer)"
        elif 'view' in path_str or filename.endswith('_view.py'):
            return "View (UI Layer)"
        elif 'util' in path_str or 'helper' in path_str:
            return "Utility (Helper Functions)"
        elif 'config' in filename:
            return "Configuration"
        elif 'test' in path_str or filename.startswith('test_'):
            return "Test"
        elif '__init__.py' in filename:
            return "Package Initializer"
        else:
            return "Other"

    def analyze_risk_level(self, file_path: Path) -> str:
        """
        Automatická detekce risk level na základě obsahu souboru.

        Args:
            file_path: Cesta k souboru

        Returns:
            "HIGH", "MEDIUM", nebo "LOW"
        """
        try:
            content = file_path.read_text(encoding='utf-8').lower()
        except:
            return "UNKNOWN"

        # HIGH risk indicators:
        high_risk_keywords = [
            'eval(', 'exec(', '__import__', 'subprocess',
            'oracledb', 'psycopg', 'pymongo',  # Database drivers
            'sqlalchemy', 'database', 'db_connection',
            'password', 'secret', 'token', 'api_key',
            'os.remove', 'shutil.rmtree', 'os.system',
        ]
        if any(keyword in content for keyword in high_risk_keywords):
            return "HIGH"

        # MEDIUM risk indicators:
        medium_risk_keywords = [
            'try:', 'except', 'raise', 'error',
            'config', 'settings', 'environment',
            'file.write', 'file.delete', 'makedirs',
            'requests.', 'http', 'api',
        ]
        if any(keyword in content for keyword in medium_risk_keywords):
            return "MEDIUM"

        return "LOW"

    def extract_external_dependencies(self, file_path: Path) -> List[str]:
        """
        Extrahuje externí knihovny (ne projektové moduly).

        Args:
            file_path: Cesta k souboru

        Returns:
            Seznam názvů externích knihoven
        """
        external_libs = set()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        # Filtruj pouze non-project imports
                        if not self._is_project_module(module_name):
                            external_libs.add(module_name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_name = node.module.split('.')[0]
                        if not self._is_project_module(module_name):
                            external_libs.add(module_name)
        except:
            pass

        return sorted(external_libs)

    def _is_project_module(self, module_name: str) -> bool:
        """Kontrola zda je modul součástí projektu."""
        # Společné názvy projektových modulů
        project_indicators = ['src', 'app', 'lib', 'core', 'config']

        # Pokud začíná tečkou, je to relativní import
        if module_name.startswith('.'):
            return True

        # Pokud odpovídá známým projektovým modulům
        if module_name in project_indicators:
            return True

        # Pokud existuje jako složka v root_dir
        if (self.root_dir / module_name).exists():
            return True

        return False

    def extract_todos(self, file_path: Path) -> List[str]:
        """
        Extrahuje TODO/FIXME/HACK/DEPRECATED komentáře.

        Args:
            file_path: Cesta k souboru

        Returns:
            Seznam nalezených TODO komentářů s čísly řádků
        """
        todos = []
        markers = ['TODO:', 'FIXME:', 'HACK:', 'XXX:', 'DEPRECATED:', 'ODSTRANĚNO:', 'WARNING:', 'CRITICAL:']

        try:
            content = file_path.read_text(encoding='utf-8')
            for line_num, line in enumerate(content.split('\n'), 1):
                for marker in markers:
                    if marker in line:
                        # Extrahuj komentář (odstraň leading whitespace a #)
                        comment = line.strip().lstrip('#').strip()
                        todos.append(f"Line {line_num}: {comment}")
                        break  # Jeden TODO per line
        except:
            pass

        return todos

    def find_test_file(self, file_path: Path) -> Optional[str]:
        """
        Heuristika pro nalezení odpovídajícího test souboru.

        Args:
            file_path: Cesta k souboru

        Returns:
            Relativní cesta k test souboru nebo None
        """
        stem = file_path.stem

        # Typické test file patterns
        test_candidates = [
            # test_module.py
            self.root_dir / "tests" / f"test_{stem}.py",
            self.root_dir / "test" / f"test_{stem}.py",
            file_path.parent / f"test_{stem}.py",

            # module_test.py
            self.root_dir / "tests" / f"{stem}_test.py",
            self.root_dir / "test" / f"{stem}_test.py",
            file_path.parent / f"{stem}_test.py",
        ]

        for candidate in test_candidates:
            if candidate.exists():
                try:
                    return str(candidate.relative_to(self.root_dir))
                except ValueError:
                    return str(candidate)

        return None

    def check_error_handling(self, file_path: Path) -> bool:
        """
        Kontrola zda soubor obsahuje error handling (try/except).

        Args:
            file_path: Cesta k souboru

        Returns:
            True pokud obsahuje try/except bloky
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    return True
        except:
            pass

        return False

    def map_dependencies(self, entry_file: Path, depth: int = 0) -> FileNode:
        """Rekurzivně mapuje závislosti od vstupního souboru s rozšířenou analýzou."""
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

        # Extrakce základních metadat
        imports = self.extract_imports(entry_file)
        docstring, classes, functions = self.extract_metadata(entry_file)

        # ⭐ Extrakce rozšířených metadat:
        business_purpose = self.extract_business_purpose(entry_file)
        architectural_role = self.detect_architectural_role(entry_file)
        risk_level = self.analyze_risk_level(entry_file)
        external_deps = self.extract_external_dependencies(entry_file)
        todos = self.extract_todos(entry_file)
        test_file = self.find_test_file(entry_file)
        has_error_handling = self.check_error_handling(entry_file)

        # Vytvoření nodu s rozšířenými metadaty
        node = FileNode(
            path=entry_file,
            relative_path=relative_path,
            docstring=docstring,
            classes=classes,
            functions=functions,
            business_purpose=business_purpose,
            architectural_role=architectural_role,
            risk_level=risk_level,
            external_deps=external_deps,
            todos=todos,
            test_file=test_file,
            has_error_handling=has_error_handling
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
        """Generuje Markdown dokumentaci dependency grafu s rozšířenými metadaty."""
        lines = [
            f"# 📊 Dependency Map (Extended)",
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
            node = self.nodes[relative_path]
            anchor = relative_path.replace('/', '-').replace('.', '-').replace('_', '-')

            # Risk level emoji
            risk_emoji = {
                'HIGH': '🔴',
                'MEDIUM': '🟡',
                'LOW': '🟢',
                'UNKNOWN': '⚪'
            }.get(node.risk_level, '⚪')

            lines.append(f"- [ ] {risk_emoji} [{relative_path}](#{anchor})")

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

            # Risk level emoji a popis
            risk_emoji = {
                'HIGH': '🔴',
                'MEDIUM': '🟡',
                'LOW': '🟢',
                'UNKNOWN': '⚪'
            }.get(node.risk_level, '⚪')

            lines.extend([
                f"### {relative_path} {{#{anchor}}}",
                "",
                f"**Path:** [{relative_path}]({relative_path})",
                "",
            ])

            # ⭐ Business Purpose
            if node.business_purpose:
                lines.append(f"**Business Purpose:** {node.business_purpose}")
                lines.append("")

            # ⭐ Architectural Role
            if node.architectural_role:
                lines.append(f"**Architectural Role:** {node.architectural_role}")
                lines.append("")

            # ⭐ Risk Level
            lines.append(f"**Risk Level:** {risk_emoji} {node.risk_level}")
            if node.has_error_handling:
                lines.append("*(Has error handling: try/except blocks)*")
            lines.append("")

            # Docstring (pokud není stejný jako business purpose)
            if node.docstring and node.docstring.strip() != (node.business_purpose or ""):
                first_line = node.docstring.split('\n')[0].strip()
                if first_line != node.business_purpose:
                    lines.append(f"**Description:** {first_line}")
                    lines.append("")

            # ⭐ External Dependencies
            if node.external_deps:
                deps_list = ", ".join(f"`{dep}`" for dep in node.external_deps[:10])
                if len(node.external_deps) > 10:
                    deps_list += f" ... +{len(node.external_deps) - 10} more"
                lines.append(f"**External Dependencies:** {deps_list}")
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

            # ⭐ TODOs/Issues
            if node.todos:
                lines.append("**🚨 TODOs/Issues:**")
                for todo in node.todos[:10]:  # Max 10 TODOs
                    lines.append(f"- {todo}")
                if len(node.todos) > 10:
                    lines.append(f"- ... +{len(node.todos) - 10} more")
                lines.append("")

            # ⭐ Test File
            if node.test_file:
                test_anchor = node.test_file.replace('/', '-').replace('.', '-').replace('_', '-')
                lines.append(f"**Test File:** ✅ [{node.test_file}](#{test_anchor})")
                lines.append("")

            # Imports (tento soubor importuje)
            if node.imports:
                lines.append("**Imports:**")
                for imp in sorted(node.imports):
                    imp_node = self.nodes.get(imp)
                    imp_anchor = imp.replace('/', '-').replace('.', '-').replace('_', '-')

                    # Risk level emoji pro import
                    if imp_node:
                        imp_risk_emoji = {
                            'HIGH': '🔴',
                            'MEDIUM': '🟡',
                            'LOW': '🟢',
                            'UNKNOWN': '⚪'
                        }.get(imp_node.risk_level, '⚪')
                        lines.append(f"- [ ] {imp_risk_emoji} [{imp}](#{imp_anchor})")
                    else:
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

        # ⭐ Summary Statistics
        lines.extend([
            "## 📊 Summary Statistics",
            "",
        ])

        # Risk distribution
        risk_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'UNKNOWN': 0}
        for node in self.nodes.values():
            risk_counts[node.risk_level] = risk_counts.get(node.risk_level, 0) + 1

        lines.append(f"**Risk Distribution:**")
        lines.append(f"- 🔴 HIGH: {risk_counts['HIGH']} files")
        lines.append(f"- 🟡 MEDIUM: {risk_counts['MEDIUM']} files")
        lines.append(f"- 🟢 LOW: {risk_counts['LOW']} files")
        lines.append("")

        # Architectural distribution
        arch_counts = {}
        for node in self.nodes.values():
            role = node.architectural_role or "Other"
            arch_counts[role] = arch_counts.get(role, 0) + 1

        lines.append(f"**Architectural Distribution:**")
        for role, count in sorted(arch_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {role}: {count} files")
        lines.append("")

        # External dependencies summary
        all_external_deps = set()
        for node in self.nodes.values():
            all_external_deps.update(node.external_deps)

        if all_external_deps:
            lines.append(f"**All External Dependencies:** {', '.join(f'`{dep}`' for dep in sorted(all_external_deps))}")
            lines.append("")

        # Zápis do souboru
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"✅ Extended dependency map vygenerována: {output_file}", file=sys.stderr)

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
        print("Usage: python3 dependency_mapper_extended.py <entry_file> [--max-depth N] [--output file.md]")
        print("Example: python3 dependency_mapper_extended.py main.py --output dependencies_ext.md")
        print("Note: Default max-depth is 999 (unlimited)")
        sys.exit(1)

    entry_file = Path(sys.argv[1])
    max_depth = 999  # Neomezená hloubka (zastaví se pouze na circular imports nebo visited files)
    output_file = Path("dependencies_ext.md")

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

    print(f"🔍 Mapuji závislosti (EXTENDED) od: {entry_file}", file=sys.stderr)
    print(f"📁 Root directory: {root_dir}", file=sys.stderr)
    print(f"⚙️  Max depth: {max_depth}", file=sys.stderr)
    print("", file=sys.stderr)

    # Mapování
    mapper = DependencyMapperExtended(root_dir, max_depth)
    mapper.map_dependencies(entry_file)

    # Generování Markdown
    mapper.generate_markdown(str(entry_file.relative_to(root_dir)), output_file)

    print("", file=sys.stderr)
    print(f"📊 Statistiky:", file=sys.stderr)
    print(f"  - Soubory: {len(mapper.nodes)}", file=sys.stderr)
    print(f"  - Chyby: {len(mapper.import_errors)}", file=sys.stderr)


if __name__ == "__main__":
    main()
