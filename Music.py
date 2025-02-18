import sys
import numpy as np
import tensorflow as tf
from music21 import stream, note, chord, midi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QComboBox

# Load pre-trained LSTM models for different genres
def load_model(genre):
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(100, 1)),
        tf.keras.layers.LSTM(128),
        tf.keras.layers.Dense(50, activation='relu'),
        tf.keras.layers.Dense(12, activation='softmax')
    ])
    model.load_weights(f"{genre}_model_weights.h5")  # Replace with actual trained model
    return model

# Generate MIDI sequence
def generate_music(model, length=100):
    sequence = np.random.rand(1, 100, 1)  # Random input, replace with seed input
    output_notes = []
    
    for _ in range(length):
        prediction = model.predict(sequence)
        index = np.argmax(prediction)
        
        if index < 8:
            output_notes.append(note.Note(index + 60))
        else:
            output_notes.append(chord.Chord([60, 64, 67]))
        
        sequence = np.roll(sequence, -1, axis=1)
        sequence[0, -1, 0] = index / 12
    
    return output_notes

# Save MIDI file
def save_midi(output_notes, filename="output.mid"):
    midi_stream = stream.Stream(output_notes)
    midi_stream.write("midi", fp=filename)
    print(f"MIDI file saved as {filename}")

# GUI Class
class MusicGeneratorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model = None
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("AI Music Generator", self)
        layout.addWidget(self.label)
        
        self.genre_select = QComboBox(self)
        self.genre_select.addItems(["Classical", "Jazz", "Rock", "Pop"])
        layout.addWidget(self.genre_select)
        
        self.load_button = QPushButton("Load Model", self)
        self.load_button.clicked.connect(self.load_model)
        layout.addWidget(self.load_button)
        
        self.generate_button = QPushButton("Generate Music", self)
        self.generate_button.clicked.connect(self.generate_music)
        layout.addWidget(self.generate_button)
        
        self.save_button = QPushButton("Save as MIDI", self)
        self.save_button.clicked.connect(self.save_midi)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
    
    def load_model(self):
        genre = self.genre_select.currentText().lower()
        self.model = load_model(genre)
        self.label.setText(f"Model for {genre} loaded!")
    
    def generate_music(self):
        if self.model is None:
            self.label.setText("Please load a genre model first!")
            return
        self.output_notes = generate_music(self.model)
        self.label.setText("Music Generated!")
    
    def save_midi(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save MIDI File", "", "MIDI Files (*.mid)")
        if filename:
            save_midi(self.output_notes, filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MusicGeneratorGUI()
    gui.show()
    sys.exit(app.exec_())
