## 📁 Runverve Backend Structure

```
runverve/
├── .env                       # Environment variables (DO NOT expose in public repos)
├── app.py                     # Main application file
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── models/                    # Database models
│   ├── user.py
│   ├── activity.py
│   ├── user_preferences.py
│   ├── photos.py
│   ├── shoe_type.py
│   ├── spark_points.py
│   ├── supplements.py
│   ├── injuries.py
│   ├── hydration.py
│   └── geocoding.py
├── controllers/               # Business logic
│   ├── __init__.py
│   ├── auth_controller.py
│   ├── user_controller.py
│   ├── activity_controller.py
│   ├── preferences_controller.py
│   ├── supplements_controller.py
│   ├── injuries_controller.py
│   ├── hydration_controller.py
│   └── geocoding_controller.py
├── middleware/                # Custom middleware
│   ├── __init__.py
│   ├── auth_middleware.py
│   └── error_handler.py
├── routes/                    # API route definitions
│   ├── __init__.py
│   ├── activity.py
│   ├── auth.py
│   ├── geocoding.py
│   ├── hydration.py
│   ├── injuries.py
│   ├── preferences.py
│   ├── spark_points.py
│   ├── supplements.py
│   └── user.py
└── utils/                     # Utility functions
    ├── __init__.py
    ├── helpers.py
    ├── validators.py
    └── file_handlers.py
```
## 🚀 Installation

Follow these steps to set up and run the project locally:

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/runverve.git
cd runverve
```

### 2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the application:
```bash
python app.py
```

The application will be available at [http://localhost:5000](http://localhost:5000).

---
