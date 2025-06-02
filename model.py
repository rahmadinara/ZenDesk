import time
from abc import ABC, abstractmethod
from collections import namedtuple

# === Abstract Base Class ===
class Tracker(ABC):
    @abstractmethod
    def track(self, *args, **kwargs):
        pass

# === Singleton Logger ===
class SessionLogger:
    _instance = None

    def __init__(self):
        if SessionLogger._instance is not None:
            raise Exception("Gunakan get_instance()")
        self.logs = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SessionLogger()
        return cls._instance

    def log_session(self, duration, mode):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append((timestamp, mode, duration))

    def get_logs(self):
        return self.logs

# === Pomodoro Model ===
class PomodoroModel:
    mode = "idle"
    start_time = 0

    @classmethod
    def set_mode(cls, mode):
        cls.mode = mode

# === Mood Tracker ===
class MoodTracker(Tracker):
    def __init__(self):
        self.moods = {}

    def track(self, mood):
        today = time.strftime("%Y-%m-%d")
        self.moods[today] = mood

# === Goal Tracker ===
class GoalTracker(Tracker):
    def __init__(self):
        self.goals = {}

    def add_goal(self, goal):
        self.goals[goal] = False

    def complete_goal(self, goal):
        if goal in self.goals:
            self.goals[goal] = True

    def track(self):
        return self.goals

# === Quotes Berdasarkan Mood ===
quotes_by_mood = {
    "happy": "Keep shining and smiling!",
    "sad": "It's okay to feel down. Tomorrow is a new day.",
    "motivated": "You are capable of amazing things!",
    "tired": "Rest if you must, but don’t quit."
}

def get_quote_by_mood(mood):
    return quotes_by_mood.get(mood, "Stay positive and keep going!")

# === Namedtuple untuk Goal Progress ===
Progress = namedtuple("Progress", ["goal", "status"])
