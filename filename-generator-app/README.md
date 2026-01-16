# Filename Generator Web Application

This project is a web application that generates file names based on a specified prefix, suffix, and extension. It utilizes Flask as the web framework and follows a structured approach to separate concerns through routes, services, and models.

## Project Structure

```
filename-generator-app
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── generator.py
│   ├── services
│   │   ├── __init__.py
│   │   └── filename_service.py
│   ├── models
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── static
│       └── css
│           └── style.css
├── templates
│   ├── base.html
│   └── index.html
├── tests
│   ├── __init__.py
│   └── test_filename_service.py
├── requirements.txt
├── config.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd filename-generator-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app/main.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Use the form on the main page to generate file names by specifying the prefix, suffix, and extension.

## Testing

To run the tests, ensure your virtual environment is activated and execute:
```
pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.