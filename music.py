import tkinter as tk
from tkinter import filedialog
import pygame
import os
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player 1.0")
        self.root.geometry("400x450")
        self.root.configure(bg="#1e1e1e")  # Dark background color

        self.music_list = []
        self.current_index = 0
        self.paused = False

        self.heading_label = tk.Label(
            root, text="MUSIC PLAYER 1.0", font=("Helvetica", 20), bg="#1e1e1e", fg="white")  # White text color
        self.heading_label.pack(pady=10, padx=10)

        self.current_music_label = tk.Label(
            root, text="Now Playing: ", font=("Helvetica", 12), bg="#1e1e1e", fg="white", anchor="w")  # White text color
        self.current_music_label.pack(pady=(0, 20), padx=10)

        self.slider_frame = tk.Frame(root, bg="#1e1e1e")  # Dark background color
        self.slider_frame.pack(pady=10)

        self.timestamp_slider = tk.Scale(self.slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300, command=self.set_music_position,
                                          bg="#1e1e1e", fg="white", highlightthickness=0, troughcolor="#3f3f3f")  # Customized slider
        self.timestamp_slider.pack()

        self.button_frame = tk.Frame(root, bg="#1e1e1e")  # Dark background color
        self.button_frame.pack(pady=10)

        self.load_music_button = tk.Button(
            self.button_frame, text="Load Music", command=self.load_music, bg="#4CAF50", fg="white", font=("Helvetica", 12))  # Green button color
        self.load_music_button.pack(side=tk.LEFT, padx=(10, 5))

        self.load_multiple_button = tk.Button(
            self.button_frame, text="Load Multiple Music", command=self.load_multiple_music, bg="#2196F3", fg="white", font=("Helvetica", 12))  # Blue button color
        self.load_multiple_button.pack(side=tk.LEFT, padx=(5, 10))

        self.play_frame = tk.Frame(root, bg="#1e1e1e")  # Dark background color
        self.play_frame.pack(pady=20)

        self.play_button = tk.Button(self.play_frame, text="▶", command=self.play_music, bg="#1e1e1e", fg="white", font=("Helvetica", 20))
        self.play_button.pack(side=tk.LEFT, padx=(0, 10))

        self.pause_button = tk.Button(self.play_frame, text="||", command=self.pause_music, bg="#1e1e1e", fg="white", font=("Helvetica", 20), state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = tk.Button(self.play_frame, text="■", command=self.stop_music, bg="#1e1e1e", fg="white", font=("Helvetica", 20), state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.play_frame, text="→", command=self.play_next_music, bg="#1e1e1e", fg="white", font=("Helvetica", 20), state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=(10, 0))

        self.previous_button = tk.Button(self.play_frame, text="←", command=self.play_previous_music, bg="#1e1e1e", fg="white", font=("Helvetica", 20), state=tk.DISABLED)
        self.previous_button.pack(side=tk.LEFT)


    def load_music(self):
        self.music_list = filedialog.askopenfilenames(
            initialdir="/", title="Select Music", filetypes=(("MP3 files", "*.mp3"), ("FLAC files", "*.flac"), ("OGG files", "*.ogg")))
        if self.music_list:
            self.update_controls()
            self.paused = False

    def load_multiple_music(self):
        folder_path = filedialog.askdirectory(
            initialdir="/", title="Select Folder")
        if folder_path:
            # Get all files from the selected directory
            music_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith((".mp3", ".flac", ".ogg"))]
            self.music_list = music_files
            if self.music_list:
                self.update_controls()
                self.paused = False

    def update_controls(self):
        self.current_index = 0
        self.update_title()
        self.enable_controls()

    def enable_controls(self):
        self.play_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.previous_button.config(state=tk.NORMAL)

    def play_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_list[self.current_index])
            pygame.mixer.music.play()
            self.update_title()
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.root.after(100, self.update_slider)  # Update slider every 100 milliseconds

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.root.title("Music Player 1.0")
        self.paused = False

    def update_title(self):
        audio = None
        try:
            audio = MP3(self.music_list[self.current_index])
        except:
            try:
                audio = FLAC(self.music_list[self.current_index])
            except:
                audio = OggVorbis(self.music_list[self.current_index])

        total_length = audio.info.length
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        self.current_music_label.config(
            text=f"Now Playing: {os.path.basename(self.music_list[self.current_index])} - {mins:02d}:{secs:02d}")
        self.timestamp_slider.config(to=total_length)

    def set_music_position(self, position):
        pygame.mixer.music.set_pos(float(position))

    def update_slider(self):
        if pygame.mixer.music.get_busy():
            # Get current position of playback
            current_pos = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            self.timestamp_slider.set(current_pos)
        # Schedule the next update
        self.root.after(100, self.update_slider)

    def play_next_music(self):
        self.current_index += 1
        if self.current_index < len(self.music_list):
            self.play_music()

    def play_previous_music(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.play_music()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
