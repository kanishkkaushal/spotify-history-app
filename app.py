from flask import Flask, redirect, request, render_template, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Needed for session management

# Set up Spotify OAuth
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='user-read-recently-played'
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        try:
            token_info = sp_oauth.get_access_token(code)
            session['token_info'] = token_info
            return redirect('/history')
        except Exception as e:
            return f"Error getting access token: {e}"
    else:
        return "Authorization code not found."

@app.route('/history')
def history():
    if 'token_info' not in session:
        return redirect('/login')
    token_info = session['token_info']
    try:
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)
        results = sp.current_user_recently_played(limit=10)
        tracks = results['items']
        return render_template('history.html', tracks=tracks)
    except Exception as e:
        return f"Error fetching history: {e}"

if __name__ == '__main__':
    app.run(debug=True)