import glob
import numpy as np
from music21 import converter, note, chord

def get_notes(dataset_path="datasets/classical/"):
    notes = []

    # Ensure dataset directory exists
    midi_files = glob.glob(dataset_path + "*.mid")
    if not midi_files:
        print("❌ No MIDI files found in datasets/classical/. Please add MIDI files.")
        return

    # Extract notes from MIDI files
    for file in midi_files:
        print(f"Parsing {file}...")
        try:
            midi = converter.parse(file)
            for part in midi.parts:
                for event in part.recurse():
                    if isinstance(event, note.Note):
                        notes.append(str(event.pitch))
                    elif isinstance(event, chord.Chord):
                        notes.append('.'.join(str(n) for n in event.normalOrder))
        except Exception as e:
            print(f"⚠️ Error processing {file}: {e}")

    # Check if notes were extracted
    if not notes:
        print("❌ No notes were extracted. Check your MIDI files!")
        return
    
    print(f"✅ Extracted {len(notes)} notes. Saving to 'notes.npy'...")

    # Save correctly as a NumPy array
    np.save("notes.npy", np.array(notes, dtype=object))

if __name__ == "__main__":
    get_notes()
