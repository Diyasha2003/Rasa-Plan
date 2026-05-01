"""
RasaPlan Memory Module
Handles student profile and conversation memory.
"""

from langchain.memory import ConversationBufferWindowMemory


def create_memory() -> ConversationBufferWindowMemory:
    """Creates a windowed conversation memory that keeps last 10 exchanges."""
    return ConversationBufferWindowMemory(
        k=10,
        memory_key="chat_history",
        return_messages=True,
        human_prefix="Student",
        ai_prefix="RasaPlan"
    )


class StudentProfile:
    """Stores and manages the student's preferences across the session."""

    def __init__(self):
        self.budget_lkr: int = 2000
        self.diet: str = "vegetarian"
        self.skill: str = "beginner"
        self.preferred_store: str = "Keells"
        self.disliked_foods: list = []
        self.allergies: list = []
        self.num_people: int = 1

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def to_dict(self) -> dict:
        return {
            "budget_lkr": self.budget_lkr,
            "diet": self.diet,
            "skill": self.skill,
            "preferred_store": self.preferred_store,
            "disliked_foods": self.disliked_foods,
            "allergies": self.allergies,
            "num_people": self.num_people
        }

    def to_context_string(self) -> str:
        return (
            f"Student Profile: Budget=LKR {self.budget_lkr}/week, "
            f"Diet={self.diet}, Skill={self.skill}, "
            f"Store={self.preferred_store}, "
            f"Dislikes={self.disliked_foods or 'none'}, "
            f"People={self.num_people}"
        )
