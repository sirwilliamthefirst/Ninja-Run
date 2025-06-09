import datetime
import requests


class LeaderboardClient:

    def __init__(self, base_url=None):
        self.base_url = base_url or "http://127.0.0.1:8000/"  # Default to local server

    def get_scores(self):
        """
        Fetch the leaderboard data from the API.
        :return: A dictionary containing the leaderboard data or an error message.
        """
        try:
            response = requests.get(f"{self.base_url}/highscores")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def submit_score(
        self, api_url: str, name: str, score: float, kills: int, time_alive: int
    ):
        """
        Submit a player's score to the API.
        :param player_name: The name of the player.
        :param score: The score of the player.
        :return: A dictionary containing the API response or an error message.
        """
        try:
            data = {
                "name": name,
                "score": score,
                "kills": kills,
                "time_alive": time_alive,
                "date": datetime.utcnow().isoformat(),  # or datetime.now().isoformat() if local time
            }

            response = requests.post(f"{self.base_url}/submit", json=data)
            response.raise_for_status()
            return response.json()
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


APIClient = LeaderboardClient("http://127.0.0.1:8000/")  # Local server URL
# APIClient = LeaderboardClient("https://your-production-server.com/")  # Production server URL
