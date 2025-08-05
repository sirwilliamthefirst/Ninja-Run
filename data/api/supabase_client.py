

from datetime import datetime, timezone
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
    user_highscore = None
    refresh_token = None
    username = None
    profile_id = None
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

    def sign_out(self):
        self.supabase.auth.sign_out()
        self.current_user = None
        self.username = None
        self.profile_id = None
        self.user_highscore = None
        self.refresh_token = None
        

    def get_username(self):
        """
        Fetch the username of the currently authenticated user.
        :return: The username or None if not authenticated.
        """
        if self.current_user is None or self.username is None:
            self.current_user = self.supabase.auth.get_user() 
        try:
            response = self.supabase.table("profiles").select("username", "profile_id").eq("id", self.current_user.user.id).execute()
            self.username = response.data[0]['username'] if response.data else None
            self.profile_id = response.data[0]['profile_id'] if response.data else None
        except requests.RequestException as e:
            print(f"Error fetching username: {e}")
            return None
        return self.username

    def get_user_id(self):
        """
        Fetch the id of the currently authenticated user.
        :return: The id or None if not authenticated.
        """
        if self.current_user is None:
            self.current_user = self.supabase.auth.get_user() 
        return self.current_user.user.id



    def get_scores(self):
        """
        Fetch the leaderboard data from the API, joining with profiles to get the username.
        :return: A dictionary containing the leaderboard data or an error message.
        """
        try:
            # Join the "score" table with the "profiles" table to get the username for each score entry
            response = (
                self.supabase.table("score")
                .select("score, kills, time_alive, profile_id, profiles(username)")
                .order("score", desc=True)
                .execute()
            )
            # The returned data will have a "profiles" field with the username for each score
            # Optionally, you can flatten the data here if needed
            return response
        except requests.RequestException as e:
            return {"error": str(e)}

    def submit_score(
        self, name: str, score: float, kills: int, time_alive: int, profile_id: str = None 
    ):
        """
        Submit a player's score to the API.
        :param player_name: The name of the player.
        :param score: The score of the player.
        :return: A dictionary containing the API response or an error message.
        """
        if profile_id is None or self.current_user is None:
            return {"error": "User ID is required for score submission."}
        try:
            data = {
                "score": score,
                "kills": kills,
                "time_alive": time_alive,
                "profile_id": profile_id,
                #"date": datetime.now(timezone.utc).isoformat()  # or datetime.now().isoformat() if local time
            }
            if self.user_highscore is None:
                response = self.supabase.table("score").select("score").eq("profile_id", profile_id).execute()
                self.user_highscore = response.data[0]["score"] if response.data else None 
            if self.user_highscore is None or self.user_highscore < score:
                response = self.supabase.table("score").upsert(data, on_conflict="profile_id").execute()
                self.user_highscore = score
                return {
                "success": True,
                "data": response.data,
                "count": response.count
                } 
            else:
                return None
            #response = requests.post(f"{self.base_url}/submit", json=data)
            #response.raise_for_status()
            
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
            return response
        except requests.RequestException as e:
            return {"error": str(e)}

    def set_username(self, username: str, id: str = None):  
        try:
            if id is None:
                id = self.current_user.user.id
            response = self.supabase.table("profiles").upsert({"id": id , "username": username}).execute()
            return response
        except requests.RequestException as e:
            return {"error": str(e)}
        
# APIClient = LeaderboardClient("https://your-production-server.com/")  # Production server URL
