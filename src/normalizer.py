from datetime import datetime
from unidecode import unidecode


def normalize_name(name):
    if not isinstance(name, str):
        return ""

    name = unidecode(name).upper().strip()

    if "," in name:
        parts = [part.strip() for part in name.split(",")]
        if len(parts) == 2:
            name = f"{parts[1]} {parts[0]}"

    return " ".join(name.split())


def normalize_currency(value):
    if value is None:
        return 0.0

    if isinstance(value, str):
        value = value.strip().replace(".", "").replace(",", ".")

    try:
        return float(value)
    except ValueError:
        return 0.0


def normalize_date(value):
    if value is None:
        return None

    try:
        return datetime.strptime(str(value), "%d/%m/%Y").date()
    except ValueError:
        try:
            return datetime.strptime(str(value), "%Y-%m-%d").date()
        except ValueError:
            return None
        
def normalize_ans(value):
    if value is None:
        return ""

    try:
        return str(int(float(value)))
    except (ValueError, TypeError):
        return str(value).strip()