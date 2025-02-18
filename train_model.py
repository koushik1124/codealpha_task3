import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Load preprocessed notes
notes = np.load("notes.npy", allow_pickle=True)

# Map unique notes to integers
unique_notes = sorted(set(notes))
note_to_int = {note: num for num, note in enumerate(unique_notes)}

sequence_length = 100
input_sequences = []
output_notes = []

# Create input-output pairs
for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    input_sequences.append([note_to_int[n] for n in seq_in])
    output_notes.append(note_to_int[seq_out])

# Reshape and normalize
X = np.reshape(input_sequences, (len(input_sequences), sequence_length, 1)) / len(unique_notes)
y = to_categorical(output_notes, num_classes=len(unique_notes))

# Define LSTM model
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(sequence_length, 1)),
    Dropout(0.2),
    LSTM(128),
    Dense(64, activation='relu'),
    Dense(len(unique_notes), activation='softmax')  # Output layer matches number of unique notes
])

model.compile(loss='categorical_crossentropy', optimizer='adam')

# Train the model
model.fit(X, y, epochs=50, batch_size=64)

# Save model weights
model.save_weights("classical_model_weights.weights.h5")
