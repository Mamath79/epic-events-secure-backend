import re


def validate_email(email: str) -> bool:
    """Vérifie si une adresse email est valide."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_regex, email))


def validate_siret(siret: str) -> bool:
    """Vérifie si un SIRET est valide (14 chiffres)."""
    return bool(re.match(r"^\d{14}$", siret))


def validate_date(date: str) -> bool:
    """Vérifie si une date est au format YYYY-MM-DD."""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date))


def validate_numeric(value: str) -> bool:
    """Vérifie si une valeur ne contient que des chiffres."""
    return bool(re.match(r"^\d+(\.\d+)?$", value))


def clean_text(text: str) -> str:
    """Supprime les espaces inutiles et les caractères spéciaux interdits."""
    text = text.strip()
    text = re.sub(
        r"[^\w\s-]", "", text
    )  # Supprime caractères spéciaux sauf lettres, chiffres, espaces et "-"
    return text


def validate_mandatory_field(value: str, field_name: str):
    """Vérifie si un champ obligatoire est renseigné."""
    if not value or not value.strip():
        raise ValueError(f"Le champ '{field_name}' est obligatoire.")


def validate_date_order(start_date: str, end_date: str, allow_same=False) -> bool:
    """Vérifie que la date de début est antérieure à la date de fin."""
    if not validate_date(start_date) or not validate_date(end_date):
        return False
    return start_date < end_date or (allow_same and start_date == end_date)
