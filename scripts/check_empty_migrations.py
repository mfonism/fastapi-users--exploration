import ast
import sys
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parents[1] / "alembic" / "versions"


def main() -> int:
    failures = [
        failure
        for migration_path in sorted(MIGRATIONS_DIR.glob("*.py"))
        for failure in _migration_failures(migration_path)
    ]

    if failures:
        sys.stderr.write("Empty Alembic migration check failed:\n")
        for failure in failures:
            sys.stderr.write(f"- {failure}\n")
        return 1

    return 0


def _migration_failures(migration_path: Path) -> list[str]:
    module = ast.parse(migration_path.read_text())
    failures: list[str] = []

    if not _has_alembic_operation(module, "upgrade"):
        failures.append(f"{migration_path.name} has no Alembic operation in upgrade()")

    if not _has_alembic_operation(module, "downgrade"):
        failures.append(
            f"{migration_path.name} has no Alembic operation in downgrade()"
        )

    return failures


def _has_alembic_operation(module: ast.Module, function_name: str) -> bool:
    function = _find_function(module, function_name)
    return function is not None and any(
        _is_alembic_operation(node) for node in ast.walk(function)
    )


def _find_function(module: ast.Module, function_name: str) -> ast.FunctionDef | None:
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return node

    return None


def _is_alembic_operation(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "op"
    )


if __name__ == "__main__":
    sys.exit(main())
