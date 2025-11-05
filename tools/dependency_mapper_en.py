#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dependency Mapper - Maps Python project dependencies from an entry file.
Generates an interactive Markdown map with links to actual files.

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
    """Representation of a file in the dependency graph."""
    path: Path
    relative_path: str
    imports: List[str] = field(default_factory=list)
    imported_by: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)


class DependencyMapper:
    """Maps Python project dependencies recursively."""

    def __init__(self, root_dir: Path, max_depth: int = 999):
        self.root_dir = root_dir
        self.max_depth = max_depth
        self.visited: Set[str] = set()
        self.nodes: Dict[str, FileNode] = {}
        self.import_errors: List[str] = []

    def resolve_import_path(self, import_name: str, from_file: Path) -> Optional[Path]:
        """
        Converts an import to an absolute file path.

        Examples:
            'src.controllers.main_controller' -> src/controllers/main_controller.py
            'config' -> config.py
            '.preview_controller' -> src/controllers/preview_controller.py (relative)
        """
        # Relative import (starts with dot)
        if import_name.startswith('.'):
            parent_dir = from_file.parent
            relative_parts = import_name.lstrip('.').split('.')
            resolved_path = parent_dir / '/'.join(relative_parts)
        else:
            # Absolute import
            parts = import_name.split('.')
            resolved_path = self.root_dir / '/'.join(parts)

        # Try various candidates
        candidates = [
            resolved_path.with_suffix('.py'),
            resolved_path / '__init__.py',
        ]

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate

        return None

    def extract_imports(self, file_path: Path) -> List[str]:
        """Extracts all imports from a file using AST."""
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
                    # from . import x (relative)
                    imports.append('.' * node.level)

        return imports

    def extract_metadata(self, file_path: Path) -> tuple:
        """Extracts docstring, classes, and functions from a file."""
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
                # Only top-level functions (not methods)
                functions.append(node.name)

        return docstring, classes, functions

    def map_dependencies(self, entry_file: Path, depth: int = 0) -> FileNode:
        """Recursively maps dependencies from the entry file."""
        # Relative path for key
        try:
            relative_path = str(entry_file.relative_to(self.root_dir))
        except ValueError:
            # File is outside root_dir
            relative_path = str(entry_file)

        # Check if we've already visited this file
        if relative_path in self.visited or depth > self.max_depth:
            return self.nodes.get(relative_path)

        self.visited.add(relative_path)
        print(f"{'  ' * depth}📄 Mapping: {relative_path}", file=sys.stderr)

        # Extract imports and metadata
        imports = self.extract_imports(entry_file)
        docstring, classes, functions = self.extract_metadata(entry_file)

        # Create node
        node = FileNode(
            path=entry_file,
            relative_path=relative_path,
            docstring=docstring,
            classes=classes,
            functions=functions
        )
        self.nodes[relative_path] = node

        # Recursively process imports
        for import_name in imports:
            resolved_path = self.resolve_import_path(import_name, entry_file)

            if resolved_path and resolved_path.exists():
                try:
                    import_relative = str(resolved_path.relative_to(self.root_dir))
                except ValueError:
                    import_relative = str(resolved_path)

                node.imports.append(import_relative)

                # Recursively map the imported file
                child_node = self.map_dependencies(resolved_path, depth + 1)

                if child_node and import_relative in self.nodes:
                    self.nodes[import_relative].imported_by.append(relative_path)

        return node

    def generate_markdown(self, entry_file: str, output_file: Path):
        """Generates Markdown documentation of the dependency graph."""
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

        # Dependency Tree (from entry point)
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

        # Detailed information for each file
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

            # Imports (what this file imports)
            if node.imports:
                lines.append("**Imports:**")
                for imp in sorted(node.imports):
                    imp_anchor = imp.replace('/', '-').replace('.', '-').replace('_', '-')
                    lines.append(f"- [ ] [{imp}](#{imp_anchor})")
                lines.append("")

            # Imported by (who imports this file)
            if node.imported_by:
                lines.append("**Imported by:**")
                for imp_by in sorted(node.imported_by):
                    imp_by_anchor = imp_by.replace('/', '-').replace('.', '-').replace('_', '-')
                    lines.append(f"- [ ] [{imp_by}](#{imp_by_anchor})")
                lines.append("")

            lines.extend(["---", ""])

        # Import errors
        if self.import_errors:
            lines.extend([
                "## ⚠️ Import Errors",
                "",
            ])
            for error in self.import_errors:
                lines.append(f"- {error}")
            lines.append("")

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"✅ Dependency map generated: {output_file}", file=sys.stderr)

    def _generate_tree(self, file_path: str, lines: List[str], visited: Set[str], prefix: str, is_last: bool):
        """Recursively generates ASCII tree."""
        if file_path in visited or file_path not in self.nodes:
            return

        visited.add(file_path)
        node = self.nodes[file_path]

        # Branch symbol
        branch = "└── " if is_last else "├── "
        lines.append(f"{prefix}{branch}{file_path}")

        # Prefix for children
        child_prefix = prefix + ("    " if is_last else "│   ")

        # Recursively process imports
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
    max_depth = 999  # Unlimited depth (stops only on circular imports or visited files)
    output_file = Path("dependencies.md")

    # Parse arguments
    if "--max-depth" in sys.argv:
        idx = sys.argv.index("--max-depth")
        max_depth = int(sys.argv[idx + 1])

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_file = Path(sys.argv[idx + 1])

    if not entry_file.exists():
        print(f"❌ File does not exist: {entry_file}", file=sys.stderr)
        sys.exit(1)

    # Detect root directory (look for .git or pyproject.toml)
    root_dir = entry_file.parent
    for parent in entry_file.parents:
        if (parent / '.git').exists() or (parent / 'pyproject.toml').exists():
            root_dir = parent
            break

    print(f"🔍 Mapping dependencies from: {entry_file}", file=sys.stderr)
    print(f"📁 Root directory: {root_dir}", file=sys.stderr)
    print(f"⚙️  Max depth: {max_depth}", file=sys.stderr)
    print("", file=sys.stderr)

    # Mapping
    mapper = DependencyMapper(root_dir, max_depth)
    mapper.map_dependencies(entry_file)

    # Generate Markdown
    mapper.generate_markdown(str(entry_file.relative_to(root_dir)), output_file)

    print("", file=sys.stderr)
    print(f"📊 Statistics:", file=sys.stderr)
    print(f"  - Files: {len(mapper.nodes)}", file=sys.stderr)
    print(f"  - Errors: {len(mapper.import_errors)}", file=sys.stderr)


if __name__ == "__main__":
    main()
