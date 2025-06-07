class HighScores:
    def __init__(self):
        # Initialize with default scores
        self.scores = [
            {"name": "Happy", "score": 0},
            {"name": "Happy", "score": 0},
            {"name": "Happy", "score": 0}
        ]
        self.load_scores()

    def load_scores(self):
        try:
            with open('high_scores.txt', 'r') as f:
                self.scores = eval(f.read())
            # Ensure we have exactly 3 scores
            if len(self.scores) != 3:
                print(f"Warning: Invalid number of scores in file ({len(self.scores)}), resetting to defaults")
                self.scores = [
                    {"name": "Happy", "score": 0},
                    {"name": "Happy", "score": 0},
                    {"name": "Happy", "score": 0}
                ]
        except Exception as e:
            print(f"Error loading high scores: {e}")
            # Keep default scores if file doesn't exist or is corrupted
            self.scores = [
                {"name": "Happy", "score": 0},
                {"name": "Happy", "score": 0},
                {"name": "Happy", "score": 0}
            ]
        finally:
            # Always save scores after loading
            self.save_scores()

    def save_scores(self):
        try:
            with open('high_scores.txt', 'w') as f:
                f.write(str(self.scores))
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def add_score(self, new_score, player_name):
        # Add new score to list
        self.scores.append({"name": player_name, "score": new_score})
        # Sort scores in descending order
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 3 scores
        self.scores = self.scores[:3]
        # Save updated scores
        self.save_scores()

    def get_high_scores(self):
        # Return scores sorted by score
        return self.scores
