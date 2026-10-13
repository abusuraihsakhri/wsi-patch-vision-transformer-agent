"""CSV input parsing and spreadsheet export safety helpers."""

def parse_csv_boolean(value):
    """Accept explicit boolean spellings; never treat 'False' as truthy."""
    if isinstance(value, bool):
        return value
    if value is None or str(value).strip() == "":
        return False
    normalized = str(value).strip().casefold()
    if normalized in {"true", "1", "yes", "y", "on"}:
        return True
    if normalized in {"false", "0", "no", "n", "off"}:
        return False
    raise ValueError("Invalid boolean value (expected true/false, yes/no, or 1/0)")


def escape_csv_formula(value):
    """Treat imported cells as data when opened in spreadsheets."""
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value
