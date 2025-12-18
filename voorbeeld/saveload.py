import json
import os
from datetime import datetime   # ✅ FIX: import at top


class SaveManager:
    def __init__(self, filename="save_data.json"):
        self.filename = filename
        self.data = {
            "highscore": 0,
            "selected_skin": 0
        }
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.data.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                print("[WARN] Save file corrupted, using defaults")

    def save(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.data, f, indent=4)
        except IOError:
            print("[ERROR] Could not save game")

    def get_highscore(self):
        return self.data["highscore"]

    def set_highscore(self, value):
        if value > self.data["highscore"]:
            self.data["highscore"] = value
            self.save()

    def get_skin(self):
        return self.data["selected_skin"]

    def set_skin(self, index):
        self.data["selected_skin"] = index
        self.save()


# ✅ FIX: OUTSIDE SaveManager
class ScoreHistory:
    def __init__(self, filename="highscore_history.txt"):
        self.filename = filename

    def add_score(self, score):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        line = f"{timestamp}  Score: {score}\n"

        with open(self.filename, "a") as f:
            f.write(line)