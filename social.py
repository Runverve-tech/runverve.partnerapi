from flask import Flask, request, session, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert
import os
from dotenv import load_dotenv
import tweepy
import facebook as fb
import requests
import json
import subprocess

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

app.secret_key = os.getenv('SERVER_SECRET_KEY')

def get_ngrok_url():
    # Call ngrok's API to fetch the public URL
    url = "http://localhost:4040/api/tunnels"
    response = subprocess.check_output(['curl', url])
    tunnels = json.loads(response)
    # Assume the first tunnel is the one used for HTTP traffic
    return tunnels['tunnels'][0]['public_url']

ngrok_url = get_ngrok_url()

# X credentials

x_api_key = os.getenv('X_API_KEY')
x_api_key_secret = os.getenv('X_API_KEY_SECRET')
x_bearer_token = os.getenv('X_BEARER_TOKEN')

callback_x = ngrok_url+'/twitter/callback'

# Facebook credentials

fb_access_token = os.getenv('FB_ACCESS_TOKEN')
fb_app_id = os.getenv('FB_APP_ID')
fb_app_secret = os.getenv('FB_APP_SECRET')

callback_fb = ngrok_url+'/facebook/callback'

fb_state = 'random_string'
fb_auth_url = f'https://www.facebook.com/v17.0/dialog/oauth?client_id={fb_app_id}&redirect_uri={callback_fb}&state={fb_state}&scope=pages_manage_posts,pages_read_engagement,pages_manage_metadata,pages_show_list'


# Instagram credentials

ig_app_id = os.getenv('IG_APP_ID')
ig_app_secret = os.getenv('IG_APP_SECRET')
ig_access_token = os.getenv('IG_ACCESS_TOKEN')

callback_ig = ngrok_url+'/instagram/callback'



# Load database URI directly from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
# Disable modification tracking overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)


class UserToken(db.Model):
    __tablename__ = 'user_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey(
        'users.user_sk'))
    platform = db.Column(db.String(100), db.Enum('X', 'FB', name='type_enum'), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    access_token_secret = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255))
    

# Start of Social Share API

# X platform sharing - START

@app.before_request
def create_tables():
    db.create_all()

@app.route('/twitter/login/<athlete_id>')
def twitter_login(athlete_id):
    auth = tweepy.OAuthHandler(x_api_key, x_api_key_secret, callback_x)
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    session['athlete_id'] = athlete_id
    return redirect(redirect_url)

@app.route('/twitter/callback') # parameter to be passed: oauth_verifier
def twitter_callback():
    request_token = session.pop('request_token')
    athlete_id = session.pop('athlete_id')
    auth = tweepy.OAuthHandler(x_api_key, x_api_key_secret)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    
    # Store user's tokens in your database
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret

    # Save the tokens associated with the user

    record_existing = UserToken.query.filter_by(user_sk=athlete_id).first()    
            
    if record_existing:
        db.session.delete(record_existing)
        
    data = UserToken(user_sk=athlete_id, platform="X", access_token=access_token, access_token_secret=access_token_secret)
    
    db.session.add(data)
    db.session.commit()
    
    return jsonify({"message": "Authentication successful!"}), 200

@app.route('/activity/share/X/<athlete_id>/<activity_id>', methods=['POST'])
def post_content_to_x(athlete_id, activity_id):
    data = request.json
    content = data['content']

    # Retrieve tokens from the database
    data = UserToken.query.filter_by(user_sk=athlete_id, platform="X").first()
    access_token, access_token_secret = data.access_token, data.access_token_secret
    

    # Post to Twitter
    client = tweepy.Client(
    bearer_token=x_bearer_token,
    consumer_key=x_api_key,
    consumer_secret=x_api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
    )
    
    response = client.create_tweet(text=content)
    
    if response:
        return jsonify({"message": "Post successful!"}), 200
    return jsonify({"message": "Posting failed"}), 400

# X platform sharing - END

# Facebook sharing - START

@app.route('/facebook/login/<athlete_id>')
def facebook_login(athlete_id):
    auth = fb.GraphAPI(access_token=fb_access_token, version='2.12')
    permissions = ['pages_manage_posts', 'pages_read_engagement', 'pages_manage_metadata', 'pages_show_list', 'pages_read_user_content', 'pages_manage_engagement', 'pages_messaging']
    session['athlete_id'] = athlete_id
    redirect_url = auth.get_auth_url(fb_app_id, callback_fb, permissions)
    return redirect(redirect_url)

@app.route('/facebook/callback')
def facebook_callback():
    if 'athlete_id' not in session:
        return jsonify({"error": "Session expired or invalid request"}), 400

    athlete_id = session.get('athlete_id')
    auth_code = request.args.get('code')

    if not auth_code:
        return jsonify({"error": "Missing authorization code"}), 400
    
    params = {
        "client_id": fb_app_id,
        "redirect_uri": callback_fb,
        "client_secret": fb_app_secret,
        "code": auth_code
    }
    fb_token_url = f'https://graph.facebook.com/v17.0/oauth/access_token'
    
    response = requests.get(fb_token_url, params=params).json()
    
    if not response:
        return jsonify({"error": "Authorization failed"}), 400
    
    access_token = response['access_token']
    
    record_existing = UserToken.query.filter_by(user_sk=athlete_id).first()    
            
    if record_existing:
        db.session.delete(record_existing)
        
    data = UserToken(user_sk=athlete_id, platform="FB", access_token=access_token)
    
    db.session.add(data)
    db.session.commit()
    
    return jsonify({"message": "Authentication successful!"}), 200

@app.route('/facebook/get_pages/<athlete_id>', methods=['GET'])
def get_pages(athlete_id):
    # Retrieve user access token from the database
    user_token = UserToken.query.filter_by(user_sk=athlete_id, platform="FB").first()
    if not user_token:
        return jsonify({"error": "User not authenticated"}), 401

    # Fetch the list of pages
    graph = fb.GraphAPI(access_token=user_token.access_token, version='2.12')
    pages = graph.get_object("me/accounts")
    
    # Store or display pages and their access tokens
    return jsonify({"pages": pages}), 200

@app.route('/activity/share/facebook/<athlete_id>/<activity_id>', methods=['POST'])
def post_content_to_fb(athlete_id, activity_id):
    
    '''
    Required JSON:
    
    Get the details from the /facebook/get_pages/<athlete_id> route
    
    {
    "id": [list of page IDs],
    "access_token": [list of acces tokens],
    "content": "string containing the message"
    }
    
    '''
    
    
    data = request.json
    ids = data['id']
    access_tokens = data['access_token']
    content = data['content']

    # Retrieve tokens from the database
    data = UserToken.query.filter_by(user_sk=athlete_id, platform="FB").first()
    access_token = data.access_token
    

    # Post to FaceBook
    
    parameters = zip(ids, access_tokens)
    
    for (page_id, access_token) in parameters:
        graph = fb.GraphAPI(access_token=access_token)
        response = graph.put_object(parent_object=page_id, connection_name='feed', message=content)
        if not response:
            return jsonify({"message": "Some post(s) have failed"}), 400
    
    return jsonify({"message": "Post successful!"}), 200
    
    
# Facebook sharing - END

# Instagram sharing - START

@app.route("/instagram/login/<athlete_id>")
def instagram_login(athlete_id):
    auth = fb.GraphAPI(access_token=ig_access_token, version='2.12')
    permissions = ['instagram_basic', 'instagram_branded_content_ads_brand', 'instagram_branded_content_brand', 'instagram_branded_content_creator', 'instagram_content_publish', 'instagram_manage_comments', 'instagram_manage_insights', 'instagram_manage_messages', 'read_insights']
    session['athlete_id'] = athlete_id
    redirect_url = f"https://www.instagram.com/oauth/authorize?enable_fb_login=0&force_authentication=1&client_id=875851897785803&redirect_uri={callback_ig}&response_type=code&scope=instagram_manage_messages%2Cinstagram_manage_comments%2Cinstagram_content_publish%2Cinstagram_content_publish%2Cinstagram_manage_insights"
    return redirect(redirect_url)

@app.route("/instagram/callback")
def instagram_callback():
    if 'athlete_id' not in session:
        return jsonify({"error": "Session expired or invalid request"}), 400

    athlete_id = session.get('athlete_id')
    auth_code = request.args.get('code')

    if not auth_code:
        return jsonify({"error": "Missing authorization code"}), 400
    
    params = {
        "client_id": ig_app_id,
        "redirect_uri": callback_ig,
        "client_secret": ig_app_secret,
        "code": auth_code,
        "grant_type": "authorization_code"
    }
    ig_token_url = f'https://www.instagram.com/oauth/access_token'
    
    response = requests.post(ig_token_url, data=params).json()
    
    if "code" in response:
        return jsonify({"error": "Authorization failed"}), 400
    
    access_token = response['access_token']
    
    record_existing = UserToken.query.filter_by(user_sk=athlete_id).first()    
            
    if record_existing:
        db.session.delete(record_existing)
        
    data = UserToken(user_sk=athlete_id, platform="IG", access_token=access_token)
    
    db.session.add(data)
    db.session.commit()
    
    return jsonify({"message": "Authentication successful!"}), 200

@app.route('/activity/share/instagram/<athlete_id>/<activity_id>', methods=['POST'])
def post_content_to_ig(athlete_id):
    
    '''
    Required JSON:
    
    Get the details from the /facebook/get_pages/<athlete_id> route
    
    {
    "id": [list of page IDs],
    "access_token": [list of acces tokens],
    "content": "string containing the message"
    }
    
    '''
    
    
    data = request.json
    content = data['content']

    # Retrieve tokens from the database
    data = UserToken.query.filter_by(user_sk=athlete_id, platform="IG").first()
    access_token = data.access_token

    # Post to FaceBook
    
    graph = fb.GraphAPI(access_token=access_token)
    response = graph.put_object(parent_object='me', connection_name='feed', message=content)
    if not response:
        return jsonify({"message": "Some post(s) have failed"}), 400
    
    return jsonify({"message": "Post successful!"}), 200


# Instagram sharing - END

# End of Social Share API


if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8000))  # Railway provides a PORT env variable
    app.run(host="0.0.0.0", port=PORT)
