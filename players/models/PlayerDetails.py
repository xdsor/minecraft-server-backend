class PlayerDetails:
    def __init__(self, food_level: int = 0, health: float = 0.0, experience: int = 0):
        self.food_level = food_level
        self.health = health
        self.experience = experience

    def to_dict(self) -> dict:
        return {
            "food_level": self.food_level,
            "health": self.health,
            "experience": self.experience
        }

    def __str__(self) -> str:
        return f"Player Details:\n  Food Level: {self.food_level}\n  Health: {self.health:.2f}"

    def __repr__(self) -> str:
        return f"PlayerDetails(food_level={self.food_level}, health={self.health:.2f})"