import os
import pygame
import tkinter as tk
from tkinter import messagebox, filedialog
from midiutil import MIDIFile

# Initialize pygame mixer
pygame.init()

# Function to generate random music notes and save as MIDI
def generate_music():
    try:
        # Sample notes for demo purposes (can be extended for more variety)
        notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale

        midi = MIDIFile(1)  # One track
        midi.addTempo(0, 0, 120)  # Set tempo to 120 BPM

        for i, note in enumerate(notes):
            midi.addNote(0, 0, note, i, 1, 100)  # Add each note with duration 1 and velocity 100

        file_path = "generated_music.mid"
        with open(file_path, "wb") as midi_file:
            midi.writeFile(midi_file)

        messagebox.showinfo("Success", f"Music generated and saved as '{file_path}'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate music: {e}")

# Function to play the generated MIDI file
def play_music():
    file_path = "generated_music.mid"
    if not os.path.exists(file_path):
        messagebox.showwarning("Warning", "No music file found. Please generate music first.")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        messagebox.showinfo("Playing", "Music is now playing!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to play music: {e}")

# Function to stop the music
def stop_music():
    try:
        pygame.mixer.music.stop()
        messagebox.showinfo("Stopped", "Music has been stopped.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop music: {e}")

# Create the application window
root = tk.Tk()
root.title("AI Music Generator")
root.geometry("400x300")

# Set an attractive background color and font style
root.configure(bg="#f0f8ff")  # Alice Blue background color
header_font = ("Helvetica", 16, "bold")
button_font = ("Arial", 12)

# Add a header label
header_label = tk.Label(root, text="Welcome to AI Music Generator", bg="#f0f8ff", fg="#333", font=header_font)
header_label.pack(pady=20)

# Add buttons with padding and styles
generate_button = tk.Button(root, text="Generate Music", command=generate_music, font=button_font, bg="#4682b4", fg="white", activebackground="#5a9bd4", activeforeground="white", width=20, height=2)
generate_button.pack(pady=10)

play_button = tk.Button(root, text="Play Music", command=play_music, font=button_font, bg="#4682b4", fg="white", activebackground="#5a9bd4", activeforeground="white", width=20, height=2)
play_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Music", command=stop_music, font=button_font, bg="#4682b4", fg="white", activebackground="#5a9bd4", activeforeground="white", width=20, height=2)
stop_button.pack(pady=10)

# Run the application
root.mainloop()
