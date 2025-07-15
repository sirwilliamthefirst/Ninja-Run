

import datetime
import os
import threading
import time
import requests
from supabase import create_client, Client
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

auth_complete = threading.Event()
oauth_result = {}
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

class LeaderboardClient:
    supabase: Client = None 
    current_user = None
    refresh_token = None
    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Handle the OAuth callback here
            print(f"Received callback: {self.path}")
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            code = query_params.get('code', [None])[0]
            print(f"code: {code}")
            if code:
                # Store the code in the server instance for later use
                oauth_result['code'] = code
                auth_complete.set()
                print("OAuth code received, you can close this window.")
            else:
                print("No OAuth code found in the callback.")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authentication successful! You can close this window.")
            print("Callback received, you can now close this window.")

    def __init__(self, supabase_url: str = url, supabase_key: str = key):
 
        self.supabase = create_client(supabase_url, supabase_key)

    def start_server(self, port=8000):
        server_address = ('localhost', 8000)
        httpd = HTTPServer(server_address, self.CallbackHandler)
        print(f"Starting server on {server_address[0]}:{server_address[1]}")
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        print(f"🌐 Callback server started on http://localhost:8000")
        return httpd, server_thread

    

    def sign_in_with_oauth(self, provider: str = "google", redirect_to: str = "http://localhost:8000/"):
        # Start server
        httpd, thread = self.start_server(8000)

        response = self.supabase.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {
                    "scopes": "email profile openid",
                    "redirectTo": "http://localhost:8000/"
                }
            }
        )

        webbrowser.open(response.url)

        if auth_complete.wait(timeout=30):  # Wait for the callback to complete
            response = self.supabase.auth.exchange_code_for_session(
            {"auth_code": oauth_result['code']}
        )
            print(f"✅ Successfully authenticated!")
            print(f"👤 Access Token: {response.session.access_token}")
            self.supabase.auth.set_session(response.session.access_token, response.session.refresh_token)
            httpd.shutdown()
            thread.join()
            auth_complete.clear()
            return True
        else:
            print("❌ Authentication failed or timed out")
            httpd.shutdown()
            thread.join()
            auth_complete.clear()
            return False

    def get_username(self):
        """
        Fetch the username of the currently authenticated user.
        :return: The username or None if not authenticated.
        """
        if self.current_user is None:
            self.current_user = self.supabase.auth.get_user() 
        try:
            username = self.supabase.table("profiles").select("username").eq("id", self.current_user.user.id).execute()
        except requests.RequestException as e:
            print(f"Error fetching username: {e}")
            return None
        return username
    def get_scores(self):
        """
        Fetch the leaderboard data from the API.
        :return: A dictionary containing the leaderboard data or an error message.
        """
        try:
            response = self.supabase.table("score").select("*").order("score", desc=True).execute()
            #response = requests.get(f"{self.base_url}/highscores")
            #response.raise_for_status()
            return response
        except requests.RequestException as e:
            return {"error": str(e)}

    def submit_score(
        self, name: str, score: float, kills: int, time_alive: int, user_id: str = None 
    ):
        """
        Submit a player's score to the API.
        :param player_name: The name of the player.
        :param score: The score of the player.
        :return: A dictionary containing the API response or an error message.
        """
        if user_id is None:
            return {"error": "User ID is required for score submission."}
        try:
            data = {
                "name": name,
                "score": score,
                "kills": kills,
                "time_alive": time_alive,
                "user_id": self.supabase.auth.get_user().id,
                "date": datetime.utcnow().isoformat(),  # or datetime.now().isoformat() if local time
            }
            response = self.supabase.table("score").insert(data).execute()
            #response = requests.post(f"{self.base_url}/submit", json=data)
            #response.raise_for_status()
            return response
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_player_rank(self, player_name):
        """
        Fetch the rank of a specific player from the API.
        :param player_name: The name of the player.
        :return: A dictionary containing the player's rank or an error message.
        """
        try:
            response = requests.get(
                f"{self.base_url}/rank", params={"player_name": player_name}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


# APIClient = LeaderboardClient("https://your-production-server.com/")  # Production server URL
