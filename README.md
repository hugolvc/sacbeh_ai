# Sacbeh

A Python application built with MVC architecture using Streamlit for the view, Pydantic for the model, and a singleton controller.

## Architecture

- **View**: Streamlit web interface
- **Model**: Pydantic models with Python data structures
- **Controller**: Singleton pattern for shared state management

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
sacbeh/
├── app.py                 # Main Streamlit application entry point
├── controller/
│   ├── __init__.py
│   └── app_controller.py  # Singleton controller
├── model/
│   ├── __init__.py
│   └── data_models.py     # Pydantic models
├── view/
│   ├── __init__.py
│   └── pages/
│       ├── __init__.py
│       └── welcome.py     # Welcome page
├── requirements.txt
└── README.md
``` 