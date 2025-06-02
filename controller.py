import time
import threading
from tkinter import messagebox
from model import SessionLogger, PomodoroModel
import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.music_file = None

    def load_music(self, filename):
        self.music_file = filename
        pygame.mixer.music.load(self.music_file)

    def play_music(self):
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

class PomodoroController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.timer_thread = None
        self.music = MusicPlayer()
        self.music.load_music("C:/Users/Lenovo/OneDrive - UGM 365/Project-PBO/Coba2/burung.mp3")  # ganti path jika perlu
        self.focus_duration = 25 * 60
        self.break_duration = 5 * 60
        self.remaining = 0
        self.running = False
        self.paused = False
        self._lock = threading.Lock()

    def update_timer_settings(self, focus_minutes, break_minutes):
        self.focus_duration = focus_minutes * 60
        self.break_duration = break_minutes * 60

    def start_focus(self):
        self.model.set_mode("focus")
        self.view.update_status("Fokus dimulai!")
        self.music.play_music()
        self.start_timer(self.focus_duration)

    def start_break(self):
        self.model.set_mode("break")
        self.view.update_status("Istirahat dimulai!")
        self.music.stop_music()
        self.start_timer(self.break_duration)

    def start_timer(self, duration):
        self.running = True
        self.paused = False
        self.remaining = duration

        def run():
            while self.remaining > 0 and self.running:
                if not self.paused:
                    mins, secs = divmod(self.remaining, 60)
                    self.view.update_timer(f"{mins:02d}:{secs:02d}")
                    time.sleep(1)
                    self.remaining -= 1
            if self.running and not self.paused:
                SessionLogger.get_instance().log_session(duration, self.model.mode)
                if self.model.mode == "focus":
                    messagebox.showinfo("Selesai!", "Sesi fokus selesai! Istirahat sejenak.")
                    self.start_break()
                else:
                    messagebox.showinfo("Istirahat selesai", "Saatnya kembali fokus.")
                    self.start_focus()

        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_thread = threading.Thread(target=run)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def pause_timer(self):
        self.paused = True
        self.view.update_status("Timer dijeda.")

    def resume_timer(self):
        if self.paused:
            self.paused = False
            self.view.update_status("Dilanjutkan.")
            self.start_timer(self.remaining)

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.remaining = 0
        self.view.update_timer("00:00")
        self.view.update_status("Timer direset.")
        self.music.stop_music()
