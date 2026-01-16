def generate_random_string(length=8):
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def generate_file_name(prefix: str = "", suffix: str = "", extension: str = "txt") -> str:
    import datetime

    now = datetime.datetime.now()
    year_str = now.strftime("%Y")
    random_str = generate_random_string()
    file_name = f"{prefix}{year_str}_{random_str}{suffix}.{extension}"
    return file_name

def create_file_name(prefix: str, suffix: str, extension: str) -> str:
    return generate_file_name(prefix, suffix, extension)