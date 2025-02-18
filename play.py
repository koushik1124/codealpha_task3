import pygame

def play_midi(file):
    """Play a MIDI file using pygame."""
    pygame.init()
    pygame.mixer.init()

    print(f"Loading MIDI file: {file}...")
    try:
        pygame.mixer.music.load(file)
        print("Playing MIDI...")
        pygame.mixer.music.play()

        # Keep the program running until the music is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Wait to allow music to play
    except Exception as e:
        print(f"Error while playing MIDI: {e}")
    finally:
        pygame.quit()

# Play the generated MIDI file
play_midi("generated_music.mid")
