import datetime
import secrets
import string

def generate_random_string(length=8):
	# Generate a secure random string of the specified length
	alphabet = string.ascii_letters + string.digits
	return "".join(secrets.choice(alphabet) for _ in range(length))

def generate_file_name(prefix: str = "", suffix: str = "", extension: str = "txt") -> str:
	# Get the current date and time
	now = datetime.datetime.now()
	year_str = now.strftime("%Y")

	# Generate a random string
	random_str = generate_random_string()

	# Construct the file name
	file_name = f"{prefix}{year_str}_{random_str}{suffix}.{extension}"
	return file_name

def main() -> None:
	prefix = "report_"
	suffix = "_v1"
	extension = "txt"
	print(generate_file_name(prefix=prefix, suffix=suffix, extension=extension))


if __name__ == "__main__":
	main()
