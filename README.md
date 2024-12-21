# Strava Integration Flask Application

This is a Flask-based web application that integrates with the Strava API. The is designed to fetch athlete data and activities from Strava and store them in a PostgreSQL database. The application uses OAuth authentication for secure access to the Strava API.

## Features

- Authenticate with Strava via OAuth.
- Fetch athlete data and activities from Strava.
- Insert fetched activity data into a PostgreSQL database, modify athlete data and credit points.
- API endpoints for:
  - Getting athlete information.
  - Handling OAuth authorization.
  - Fetching and storing Strava activities.
  - Spark ledger debit functionality.

## Requirements

- Python 3.x
- Flask
- psycopg2
- requests
- PostgreSQL Database
- Strava Developer Account (for API credentials)

## Installation

### 1. Clone the Repository

First, clone this repository to your local machine:

git clone <replace with repo_url>  
cd <replace with repo_directory>

### 2. Install Dependencies

Make sure you have Python 3.x installed, then install the required dependencies:

pip install Flask
pip install psycopg2

### 3. Set Up PostgreSQL

Make sure you have PostgreSQL set up on your machine and create a database for the application. Use the following SQL to create the necessary tables:

CREATE TABLE users (  
    user_sk SERIAL PRIMARY KEY,  
    username VARCHAR(100),  
    email VARCHAR(100),  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);

CREATE TABLE user_token (  
    user_sk INT,  
    token VARCHAR(255),  
    FOREIGN KEY (user_sk) REFERENCES users(user_sk)  
);

CREATE TABLE spark_ledger (  
    id SERIAL PRIMARY KEY,  
    user_sk INT,  
    credit_score INT,  
    debit_score INT,  
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (user_sk) REFERENCES users(user_sk)  
);

CREATE TABLE activity (  
    activity_id INT PRIMARY KEY,  
    athlete_id INT,  
    name VARCHAR(255),  
    distance FLOAT,  
    moving_time INT,  
    elapsed_time INT,  
    total_elevation_gain FLOAT,  
    type VARCHAR(50),  
    start_date TIMESTAMP,  
    description TEXT,  
    calories FLOAT,  
    FOREIGN KEY (athlete_id) REFERENCES users(user_sk)  
);

Make sure to adjust the table schemas as necessary based on your needs, and update the tables as given in the repo files.

### 4. Configuration

Create a `configFile.ini` file in the root directory (similar to the one in the repo, but wit your credentials) and configure it with the following information:

[RunVerveDB]  
DB_HOST = <your_database_host>  
DB_PORT = <your_database_port>  
DB_NAME = <your_database_name>  
DB_USER = <your_database_user>  
DB_PASSWORD = <your_database_password>  

[RunVerveStrava]  
ID = <your_strava_client_id>  
secret = <your_strava_client_secret>  
access_token = <your_strava_access_token>  
refresh_token = <your_strava_refresh_token>  
redirect_uri = <your_redirect_uri>  
authorization_code = <your_authorization_code>  

- Replace `<your_database_*>` with your PostgreSQL database details.
- Replace `<your_strava_*>` with your Strava API credentials. You will need to go to the Strava developer portal to create an app and obtain these values.

### 5. Run the Application

Once you've configured the `configFile.ini` and set up the database, you can start the Flask application:

python app.py

By default, the application will run on `http://localhost:5000`.

## API Endpoints

### 1. `/athlete` (POST)
Fetches athlete data from Strava.

**Response:**
- `200 OK`: Returns the athlete's data along with a redirect URL for authorization if the access token is incorrect.
- `401 Unauthorized`: If the access token is incorrect.
- `500 Internal Server Error`: For other issues.

### 2. `/auth` (POST)
Handles the OAuth authorization with Strava.

**Request Body:**
- `code`: The authorization code received after the user authorizes the app.

**Response:**
- `200 OK`: Returns the access token and refresh token.
- `500 Internal Server Error`: If any error occurs during authorization.

### 3. `/athlete/activities` (GET)
Fetches the athlete's activities from Strava and inserts them into the database.

**Response:**
- `200 OK`: Returns the list of activities.
- `500 Internal Server Error`: If any error occurs.

### 4. `/spark_debit` (POST)
Updates the user's Spark debit ledger.

**Request Body:**
- `user_sk`: The user identifier.
- `redeem_points`: The points to redeem.
- `token`: The authentication token.

**Response:**
- `200 OK`: Confirms the redemption and returns the updated ledger information.
- `400 Bad Request`: If the credit score is insufficient or required parameters are missing.
- `403 Forbidden`: If the token is invalid.
- `404 Not Found`: If the user is not found.

### 5. `/athlete/activities` (GET)
Fetches a list of the athlete's activities from Strava.

**Response:**
- `200 OK`: Returns the list of activities from Strava.
- `500 Internal Server Error`: If an error occurs when fetching the activities.

### 6. `/activities` (GET)
Fetches all activities of the user from Strava and stores them in the database.

**Response:**
- `200 OK`: Returns a success message indicating that the activities have been inserted successfully into the database.
- `500 Internal Server Error`: If there is a failure in inserting activities into the database.


### 7. `/spark_update` (POST)
Updates the Spark ledger for a user. This endpoint will redeem points from the user’s credit score.

**Request Body:**
- `user_sk`: The user identifier.
- `redeem_points`: The points to redeem.
- `token`: The authentication token.

**Response:**
- `200 OK`: Confirms the redemption and returns the updated ledger information.
- `400 Bad Request`: If the credit score is insufficient or required parameters are missing.
- `403 Forbidden`: If the token is invalid.
- `404 Not Found`: If the user is not found.

**Response:**
- `200 OK`: Confirms the redemption and returns the updated ledger information.
- `400 Bad Request`: If the credit score is insufficient or required parameters are missing.
- `403 Forbidden`: If the token is invalid.
- `404 Not Found`: If the user is not found.

## Notes

- You must use your own Strava API credentials (client ID, client secret, etc.).
- Ensure your PostgreSQL database is accessible and configured correctly.
- The app uses `psycopg2` to interact with the PostgreSQL database and `requests` to interact with the Strava API.
- Make sure to handle sensitive data, such as your database credentials and Strava API keys, securely.

## Troubleshooting

- If you face issues with database connections, check your PostgreSQL setup and credentials.
- If the Strava API responds with `401 Unauthorized`, ensure your access token is valid and not expired.
- If any routes fail, check the server logs for detailed error messages.
