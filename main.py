from model import PomodoroModel, MoodTracker, GoalTracker
from controller import PomodoroController
from view import PomodoroView

if __name__ == "__main__":
    mood_tracker = MoodTracker()
    goal_tracker = GoalTracker()
    model = PomodoroModel()
    controller = PomodoroController(model, None)

    app = PomodoroView(controller, mood_tracker, goal_tracker)
    controller.view = app

    app.mainloop()
