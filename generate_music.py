import numpy as np
from music21 import stream, note, midi

# Example list of generated notes for testing
generated_notes = [44, 33, 56, 56, 74, 45, 65, 61, 75, 45, 50, 33, 74, 75, 61, 50]

# Mapping of integers to MIDI pitches (adjust according to your note mapping)
int_to_note = {
    33: "C4", 44: "E4", 45: "F4", 50: "G4", 56: "A4",
    61: "B4", 65: "C5", 74: "D5", 75: "E5"
}

def notes_to_midi(notes, filename="generated_music.mid"):
    """Converts a list of notes to a MIDI file and saves it."""
    midi_stream = stream.Stream()

    print("Converting notes to MIDI...")
    for note_int in notes:
        try:
            note_str = int_to_note[note_int]  # Convert integer to note string
            new_note = note.Note(note_str)    # Create a music21 note object
            midi_stream.append(new_note)
        except KeyError:
            print(f"Warning: Note {note_int} not found in int_to_note mapping. Skipping.")

    # Save the MIDI file
    try:
        print("Saving MIDI file...")
        midi_stream.write("midi", fp=filename)  # Correct method to write MIDI
        print("MIDI file saved successfully as", filename)
    except Exception as e:
        print(f"Error while saving MIDI file: {e}")

# Call the function to create the MIDI file
notes_to_midi(generated_notes)
