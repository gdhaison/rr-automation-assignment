"""Helpers for parsing pytest-bdd/cucumber style tables used in step definitions."""
from typing import Dict


def parse_cucumber_table(table: str) -> Dict[str, str]:
    if not table:
        return {}
    lines = [l.strip() for l in table.strip().splitlines() if l.strip()]
    result: Dict[str, str] = {}
    for row in lines:
        parts = [p.strip() for p in row.split('|') if p.strip()]
        if len(parts) >= 2:
            key = parts[0]
            value = parts[1]
            result[key] = value
    return result
