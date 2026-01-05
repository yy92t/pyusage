from __future__ import annotations

import re


_RE_IF = re.compile(r"^if\s+(.*):\s*$")
_RE_ELIF = re.compile(r"^elif\s+(.*):\s*$")
_RE_ELSE = re.compile(r"^else:\s*$")
_RE_WHILE = re.compile(r"^while\s+(.*):\s*$")
_RE_FOR_RANGE = re.compile(
	r"^for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+range\(([^)]*)\):\s*$"
)


def _indent_width(line: str) -> int:
	return len(line) - len(line.lstrip(" \t"))


def translate_python_to_javascript(python_code: str) -> str:
	out: list[str] = []
	block_indents: list[int] = []

	for raw_line in python_code.splitlines():
		if not raw_line.strip():
			out.append("")
			continue

		indent = _indent_width(raw_line)
		line = raw_line.strip()

		# Close blocks when indentation decreases.
		while block_indents and indent < block_indents[-1]:
			block_indents.pop()
			out.append("}" )

		if line.startswith("#"):
			out.append("//" + line[1:])
			continue

		# print(...) -> console.log(...)
		if line.startswith("print("):
			out.append("console.log" + line[len("print"):])
			continue

		m = _RE_ELIF.match(line)
		if m:
			out.append(f"else if ({m.group(1)}) {{")
			block_indents.append(indent + 1)
			continue

		if _RE_ELSE.match(line):
			out.append("else {")
			block_indents.append(indent + 1)
			continue

		m = _RE_IF.match(line)
		if m:
			out.append(f"if ({m.group(1)}) {{")
			block_indents.append(indent + 1)
			continue

		m = _RE_WHILE.match(line)
		if m:
			out.append(f"while ({m.group(1)}) {{")
			block_indents.append(indent + 1)
			continue

		m = _RE_FOR_RANGE.match(line)
		if m:
			var = m.group(1)
			args = [a.strip() for a in m.group(2).split(",") if a.strip()]
			if len(args) == 1:
				start, end, step = "0", args[0], "1"
			elif len(args) == 2:
				start, end, step = args[0], args[1], "1"
			else:
				start, end, step = args[0], args[1], args[2]

			# Simple direction assumption for step (keeps this lightweight).
			cmp_op = "<" if not step.startswith("-") else ">"
			out.append(f"for (let {var} = {start}; {var} {cmp_op} {end}; {var} += {step}) {{")
			block_indents.append(indent + 1)
			continue

		# Fallback: pass through.
		out.append(line)

	while block_indents:
		block_indents.pop()
		out.append("}")

	return "\n".join(out)


def main() -> None:
	python_script = """\
# This is a comment
print("Hello, World!")
if x > 0:
	print("Positive")
elif x == 0:
	print("Zero")
else:
	print("Negative")

for i in range(5):
	print(i)

while x < 5:
	print(x)
	x += 1
"""

	javascript_script = translate_python_to_javascript(python_script)
	print("Translated JavaScript Code:\n")
	print(javascript_script)


if __name__ == "__main__":
	main()
