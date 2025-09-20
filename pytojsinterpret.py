def translate_python_to_javascript(python_code):
js_code = python_code

# Translate print statements
js_code = js_code.replace("print(", "console.log(")

# Translate comments
js_code = js_code.replace("#", "//")

# Translate if-else statements
js_code = js_code.replace("elif", "else if")
js_code = js_code.replace("else:", "else {")
js_code = js_code.replace("if ", "if (")
js_code = js_code.replace("):", ") {")

# Translate for loops
js_code = js_code.replace("for ", "for (let ")
js_code = js_code.replace(" in range(", " = 0; ")
js_code = js_code.replace("):", ") {")

# Translate while loops
js_code = js_code.replace("while ", "while (")
js_code = js_code.replace(":", ") {")

# Close brackets
js_code = js_code.replace("\n", "\n}\n")

return js_code

# Example usage
python_script = ““”
# This is a comment
print(“Hello, World!”)
if x > 0:
print(“Positive”)
elif x == 0:
print(“Zero”)
else:
print(“Negative”)`

for i in range(5):
print(i)

`while x < 5:
print(x)
x += 1
““”`

`javascript_script = translate_python_to_javascript(python_script)
print(“Translated JavaScript Code:”, javascript_script)`
