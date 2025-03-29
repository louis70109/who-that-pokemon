# Who That Pokemon

This is a simple FastAPI application that includes:
- A health check endpoint (`/health`) to verify the service status.
- An index route (`/`) that renders an HTML page using Jinja2 templates.

## Requirements

Make sure you have Python 3.7+ installed. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Setting Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Follow these steps:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
   - Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
   - Index page: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Project Structure

```
/who-that-pokemon
├── main.py                # FastAPI application
├── requirements.txt       # Dependencies
├── templates/
│   └── index.html         # HTML template for the index route
├── static/                # Directory for static files (optional)
└── README.md              # Project documentation
```

## Endpoints

### `/health`
- **Method**: GET
- **Description**: Returns a JSON response with the service status.
- **Response**:
  ```json
  {
    "status": "ok"
  }
  ```

### `/`
- **Method**: GET
- **Description**: Renders the `index.html` template.

## Notes

- You can add static files (e.g., CSS, JS) to the `static/` directory if needed.
- Modify the `templates/index.html` file to customize the front-end content.