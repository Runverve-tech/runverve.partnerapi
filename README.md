## Project Structure

runverve.partnerapi/
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── requirements.txt        # Dependencies
├── models/                 # Database models
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
├── controllers/            # Business logic
│   ├── __init__.py
│   ├── auth_controller.py
│   ├── user_controller.py
│   ├── activity_controller.py
│   ├── preferences_controller.py
│   ├── supplements_controller.py
│   ├── injuries_controller.py
│   ├── hydration_controller.py
│   └── geocoding_controller.py
├── middleware/             # Custom middleware
│   ├── __init__.py
│   ├── auth_middleware.py
│   └── error_handler.py
├── routes/                 # API routes
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
└── utils/                  # Utility functions
    ├── __init__.py
    ├── helpers.py
    ├── validators.py
    └── file_handlers.py
## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/runverve.git
cd runverve
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

A `.env` file is already included in the repository. Make sure it contains all the required environment variables, such as:

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_uri
JWT_SECRET_KEY=your_jwt_secret
```

> 🔐 Replace the placeholder values with your actual keys.

### 5. Run the application

```bash
python app.py
```
