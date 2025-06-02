import tkinter as tk
from tkinter import messagebox, simpledialog, Menu
from model import get_quote_by_mood, SessionLogger

class PomodoroView(tk.Tk):
    def __init__(self, controller, mood_tracker, goal_tracker):
        super().__init__()
        self.controller = controller
        self.mood_tracker = mood_tracker
        self.goal_tracker = goal_tracker
        self.title("Pomodoro Productivity App")

        self.timer_label = tk.Label(self, text="00:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=10)

        self.status_label = tk.Label(self, text="Status: Idle", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        # Buttons
        tk.Button(self, text="Start Fokus", command=self.controller.start_focus).pack(pady=5)
        tk.Button(self, text="Pause", command=self.pause_timer).pack(pady=5)      # Tambah Pause
        tk.Button(self, text="Reset", command=self.reset_timer).pack(pady=5)      # Tambah Reset
        tk.Button(self, text="Tambah Goal", command=self.add_goal).pack(pady=5)
        tk.Button(self, text="Lihat Progress", command=self.show_progress).pack(pady=5)
        tk.Button(self, text="Set Mood", command=self.set_mood).pack(pady=5)
        tk.Button(self, text="Log Fokus", command=self.show_logs).pack(pady=5)

        # Menu bar
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # Menu Settings
        settings_menu = Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="Set Timer Durasi", command=self.set_timer_settings)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)

    def update_timer(self, text):
        self.timer_label.config(text=text)

    def update_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    def pause_timer(self):
        self.controller.pause_timer()

    def reset_timer(self):
        self.controller.reset_timer()

    # dialog untuk setting timer
    def set_timer_settings(self):
        focus_time = simpledialog.askinteger("Set Durasi Fokus", "Masukkan durasi fokus (menit):", minvalue=1, maxvalue=180)
        break_time = simpledialog.askinteger("Set Durasi Istirahat", "Masukkan durasi istirahat (menit):", minvalue=1, maxvalue=60)
        if focus_time and break_time:
            self.controller.update_timer_settings(focus_time, break_time)
            messagebox.showinfo("Sukses", f"Durasi fokus: {focus_time} menit\nDurasi istirahat: {break_time} menit")

    def set_mood(self):
        mood = simpledialog.askstring("Mood", "Apa mood Anda hari ini? (happy/sad/motivated/tired)")
        if mood:
            self.mood_tracker.track(mood)
            quote = get_quote_by_mood(mood)
            messagebox.showinfo("Motivasi", quote)

    def add_goal(self):
        goal = simpledialog.askstring("Tambah Goal", "Masukkan tujuan hari ini:")
        if goal:
            self.goal_tracker.add_goal(goal)
            messagebox.showinfo("Goal", f"Goal '{goal}' berhasil ditambahkan.")

    def show_progress(self):
        progress = self.goal_tracker.track()
        if not progress:
            messagebox.showinfo("Progress", "Belum ada goals.")
        else:
            lines = [f"{g}: {'Selesai' if v else 'Belum'}" for g, v in progress.items()]
            messagebox.showinfo("Progress", "\n".join(lines))

    def show_logs(self):
        logs = SessionLogger.get_instance().get_logs()
        if not logs:
            messagebox.showinfo("Log Fokus", "Belum ada sesi yang tercatat.")
        else:
            entries = [f"{t} - {m} - {d//60} menit" for t, m, d in logs]
            messagebox.showinfo("Log Fokus", "\n".join(entries))
