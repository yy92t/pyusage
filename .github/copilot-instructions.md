# Copilot Instructions for pyusage

This repository is a Python self-development project containing utility scripts and learning exercises.

## Python Style and Conventions

- **Python Version**: Use Python 3.10+ features
- **Type Hints**: Always use type hints for function parameters and return values
- **Future Imports**: Include `from __future__ import annotations` at the top of all Python files for better type hint support
- **String Formatting**: Use f-strings for string formatting
- **Tabs**: Use tabs for indentation (consistent with existing codebase)

## Code Organization

- **Imports**: Group imports in standard order (standard library, third-party, local)
- **Functions**: Use descriptive function names with snake_case
- **Private Functions**: Prefix internal helper functions with underscore (e.g., `_mask_ip`, `_domain_from_url`)
- **Main Guard**: Always include `if __name__ == "__main__":` guard for executable scripts

## Testing

- **Framework**: Use Python's built-in `unittest` framework
- **Test Files**: Name test files as `test_<module>.py`
- **Test Methods**: Prefix test methods with `test_`
- **Mocking**: Use `unittest.mock.patch` for mocking external dependencies
- **Running Tests**: Execute tests with `python3 -m unittest <test_module>`

## Dependencies

- **Requirements File**: All dependencies are listed in `requirements.txt`
- **Key Dependencies**: requests, beautifulsoup4, pandas
- **Session Management**: Use `requests.Session()` context managers for HTTP requests
- **User Agent**: Set custom User-Agent header as `"pyusage/1.0"` for web requests

## Documentation

- **Docstrings**: Use docstrings for complex functions and classes
- **Comments**: Add inline comments for non-obvious logic
- **README**: Keep README.md updated with script usage examples

## Error Handling

- **Exceptions**: Use specific exception types (e.g., `requests.RequestException`, `ValueError`)
- **Try-Except**: Wrap external calls (network, file I/O) in try-except blocks
- **Error Messages**: Provide clear, informative error messages to users

## Specific Guidelines

### Network Scripts
- Use concurrent execution with `ThreadPoolExecutor` for parallel operations
- Set appropriate timeouts for all network requests (typically 10-20 seconds)
- Handle HTTP error codes gracefully with informative messages

### Privacy Considerations
- The `wifiip.py` script implements privacy-friendly defaults (masks IP addresses)
- Use `--reveal` flag to show full information when needed
- Mask sensitive information in output (e.g., last octets of IPs, MAC addresses)

### Path Handling
- Use `pathlib.Path` for file and directory operations
- Create parent directories with `mkdir(parents=True, exist_ok=True)`
- Use `Path.write_text()` and `Path.read_text()` for simple file operations

## Best Practices

- Write modular, reusable functions
- Keep functions focused on single responsibilities
- Use type hints consistently throughout the codebase
- Test edge cases and error conditions
- Follow existing code patterns and conventions in the repository
