#!/usr/bin/env python3
"""Generate comprehensive API documentation for vexy-markliff.

This script extracts docstrings, type annotations, and examples from the codebase
to generate markdown documentation for all public APIs.
"""
# this_file: scripts/generate_api_docs.py

import ast
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Any


def extract_class_info(node: ast.ClassDef) -> dict[str, Any]:
    """Extract information from a class AST node."""
    info = {"name": node.name, "docstring": ast.get_docstring(node), "methods": [], "attributes": []}

    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            if not item.name.startswith("_"):  # Only public methods
                method_info = {
                    "name": item.name,
                    "docstring": ast.get_docstring(item),
                    "args": [arg.arg for arg in item.args.args if arg.arg != "self"],
                    "returns": ast.unparse(item.returns) if item.returns else None,
                }
                info["methods"].append(method_info)

    return info


def extract_function_info(node: ast.FunctionDef) -> dict[str, Any]:
    """Extract information from a function AST node."""
    return {
        "name": node.name,
        "docstring": ast.get_docstring(node),
        "args": [arg.arg for arg in node.args.args],
        "returns": ast.unparse(node.returns) if node.returns else None,
    }


def analyze_module(file_path: Path) -> dict[str, Any]:
    """Analyze a Python module and extract API information."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)

        module_info = {"file": str(file_path), "docstring": ast.get_docstring(tree), "classes": [], "functions": []}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                module_info["classes"].append(extract_class_info(node))
            elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                # Only top-level functions
                if isinstance(node.parent if hasattr(node, "parent") else None, ast.Module):
                    module_info["functions"].append(extract_function_info(node))

        return module_info
    except Exception as e:
        return {"file": str(file_path), "error": str(e)}


def generate_markdown_docs(modules_info: list[dict[str, Any]]) -> str:
    """Generate markdown documentation from module information."""
    markdown = """# Vexy Markliff API Documentation

This document provides comprehensive API documentation for the vexy-markliff package.

## Table of Contents

"""

    # Generate table of contents
    for module in modules_info:
        if "error" in module:
            continue

        module_name = Path(module["file"]).stem
        markdown += f"- [{module_name}](#{module_name.replace('_', '-')})\n"

        for cls in module.get("classes", []):
            markdown += f"  - [{cls['name']}](#{cls['name'].lower()})\n"

        for func in module.get("functions", []):
            markdown += f"  - [{func['name']}](#{func['name'].lower()})\n"

    markdown += "\n---\n\n"

    # Generate detailed documentation
    for module in modules_info:
        if "error" in module:
            continue

        module_name = Path(module["file"]).stem
        markdown += f"## {module_name}\n\n"

        if module.get("docstring"):
            markdown += f"{module['docstring']}\n\n"

        # Classes
        for cls in module.get("classes", []):
            markdown += f"### {cls['name']}\n\n"

            if cls.get("docstring"):
                markdown += f"{cls['docstring']}\n\n"

            # Methods
            for method in cls.get("methods", []):
                markdown += f"#### {cls['name']}.{method['name']}\n\n"

                if method.get("docstring"):
                    markdown += f"```python\n{method['docstring']}\n```\n\n"

                # Method signature
                args_str = ", ".join(method.get("args", []))
                returns_str = f" -> {method['returns']}" if method.get("returns") else ""
                markdown += f"```python\ndef {method['name']}({args_str}){returns_str}\n```\n\n"

        # Functions
        for func in module.get("functions", []):
            markdown += f"### {func['name']}\n\n"

            if func.get("docstring"):
                markdown += f"{func['docstring']}\n\n"

            # Function signature
            args_str = ", ".join(func.get("args", []))
            returns_str = f" -> {func['returns']}" if func.get("returns") else ""
            markdown += f"```python\ndef {func['name']}({args_str}){returns_str}\n```\n\n"

        markdown += "---\n\n"

    return markdown


def main():
    """Generate API documentation for vexy-markliff."""
    src_dir = Path("src/vexy_markliff")

    if not src_dir.exists():
        return

    modules_info = []

    # Analyze all Python files
    for py_file in src_dir.rglob("*.py"):
        if py_file.name.startswith("__"):
            continue

        module_info = analyze_module(py_file)
        modules_info.append(module_info)

    # Generate documentation
    docs = generate_markdown_docs(modules_info)

    # Write to file
    docs_file = Path("docs/api.md")
    docs_file.parent.mkdir(exist_ok=True)

    with open(docs_file, "w", encoding="utf-8") as f:
        f.write(docs)


if __name__ == "__main__":
    main()
