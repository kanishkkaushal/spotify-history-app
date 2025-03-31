Spotify History App



A simple Flask web application that uses the Spotify API to fetch and display a user's last 10 recently played songs. The app features a colorful theme inspired by Spotify and includes automated testing with GitHub Actions for Continuous Integration/Continuous Deployment (CI/CD).

## Features
- **Home Page**: A single "Get my History" button styled with Spotify’s green accent.
- **History Page**: Displays the user’s last 10 played songs after authentication with Spotify.
- **Theme**: Dark background (`#121212`) with green accents (`#1DB954`), mimicking Spotify’s aesthetic.
- **Testing**: Unit tests with `pytest` to ensure functionality.
- **CI/CD**: Automated testing via GitHub Actions on every push or pull request.

## Prerequisites
- Python 3.x installed on your system.
- A Spotify account and access to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
- Git installed for version control.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/spotify_history_app.git
cd spotify_history_app
```

### 2. Create a Virtual Environment
```bash
python -m venv myenv
```
Activate it:
- Windows: `myenv\Scripts\activate`
- Linux/Mac: `source myenv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Spotify API Credentials
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create a new app (e.g., "Spotify History App").
3. Note your **Client ID** and **Client Secret**.
4. Add `http://localhost:5000/callback` as a Redirect URI in the app settings.

### 5. Set Environment Variables
Set these variables in your terminal:
- Windows:
  ```bash
  set SPOTIPY_CLIENT_ID=your_client_id
  set SPOTIPY_CLIENT_SECRET=your_client_secret
  set SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
  ```
- Linux/Mac:
  ```bash
  export SPOTIPY_CLIENT_ID=your_client_id
  export SPOTIPY_CLIENT_SECRET=your_client_secret
  export SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
  ```
Replace `your_client_id` and `your_client_secret` with your actual Spotify credentials.

### 6. Run the App Locally
```bash
python app.py
```
Open your browser to `http://localhost:5000`, click "Get my History," log in to Spotify, and see your song history.

## Running Tests Locally
1. Ensure you’re in the virtual environment and have set the environment variables.
2. Run:
   ```bash
   pytest
   ```
   Tests are defined in `tests/test_app.py` and verify the home page, login redirect, and history page behavior.

## GitHub Actions for CI/CD
This project uses **GitHub Actions** to automate testing as part of a Continuous Integration/Continuous Deployment (CI/CD) pipeline. The workflow is defined in `.github/workflows/test.yml`.

### How It Works
- **Trigger**: Runs on every `push` or `pull_request` to the repository.
- **Steps**:
  1. Checks out the code.
  2. Sets up Python 3.x on an Ubuntu runner.
  3. Installs dependencies from `requirements.txt`.
  4. Runs `pytest` to execute all tests.
- **Environment Variables**: Sensitive Spotify credentials (`SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`) are stored as GitHub Secrets and injected into the workflow, ensuring security. The redirect URI is hardcoded for simplicity.

### Configuration
To replicate this in your repository:
1. Push your code to GitHub.
2. Go to **Settings > Secrets and variables > Actions > Secrets** in your GitHub repo.
3. Add:
   - `SPOTIPY_CLIENT_ID`: Your Spotify Client ID.
   - `SPOTIPY_CLIENT_SECRET`: Your Spotify Client Secret.
4. The workflow file (`test.yml`) uses these secrets:
   ```yaml
   - name: Run tests
     env:
       SPOTIPY_CLIENT_ID: ${{ secrets.SPOTIPY_CLIENT_ID }}
       SPOTIPY_CLIENT_SECRET: ${{ secrets.SPOTIPY_CLIENT_SECRET }}
       SPOTIPY_REDIRECT_URI: "http://localhost:5000/callback"
     run: |
       pytest
   ```
5. Check the **Actions** tab in your repo to see test results after pushing changes.

This setup ensures that every code change is automatically tested, providing confidence that the app works as expected.

## Project Structure
```
spotify_history_app/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── home.html       # Home page with "Get my History" button
│   └── history.html    # Song history display page
├── tests/              # Test files
│   └── test_app.py     # Pytest unit tests
├── requirements.txt    # Project dependencies
├── .github/            # GitHub Actions configuration
│   └── workflows/
│       └── test.yml    # CI/CD workflow
└── README.md           # This file
```

## Future Deployment
The app is designed to be error-free and ready for deployment to an AWS EC2 instance. For deployment:
- Update `SPOTIPY_REDIRECT_URI` to your EC2 public URL (e.g., `http://<ec2-ip>:5000/callback`).
- Set environment variables on the EC2 instance.
- Use a production server like Gunicorn: `gunicorn -b 0.0.0.0:5000 app:app`.

## Contributing
Feel free to fork this repository, submit pull requests, or open issues for suggestions or bug reports.

## License
This project is unlicensed and free for personal use. Enjoy!

---

### Notes
- Replace `your-username` in the clone command with your actual GitHub username.
- If you want to add a license (e.g., MIT), you can include a `LICENSE` file and update the "License" section accordingly.
- This README assumes your repository is public. If it’s private, the GitHub Actions setup still works the same way.

Save this as `README.md` in your project root, and you’ll have a professional-looking documentation file that reflects your project and its CI/CD setup with GitHub Actions! Let me know if you’d like to tweak anything.
