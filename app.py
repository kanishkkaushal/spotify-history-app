from flask import Flask, redirect, request, render_template, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Ensure this is set

print("Starting app, SPOTIPY_REDIRECT_URI:", os.getenv('SPOTIPY_REDIRECT_URI'))
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='user-read-recently-played'
)

@app.route('/')
def home():
    code = request.args.get('code')
    if code:
        print("Code received at /:", code)
        return redirect('/callback?code=' + code)  # Redirect to /callback if code is sent here
    print("Serving home page")
    return render_template('home.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    print("Redirecting to Spotify, auth_url:", auth_url)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print("Callback received, code:", code)
    if code:
        try:
            token_info = sp_oauth.get_access_token(code)
            print("Token info:", token_info)
            session['token_info'] = token_info
            print("Redirecting to /history")
            return redirect('/history')
        except Exception as e:
            print("Error in callback:", str(e))
            return f"Error getting access token: {e}"
    else:
        print("No code received in callback")
        return "Authorization code not found."

@app.route('/history')
def history():
    print("History route accessed, token in session:", 'token_info' in session)
    if 'token_info' not in session:
        print("No token, redirecting to /login")
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
    app.run(host='0.0.0.0', port=5000, debug=True)