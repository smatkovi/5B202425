import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen (we need a screen to capture key events)
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Press 'P' to Play Piano Note")

# Load the audio file
note_sound = pygame.mixer.Sound(
    "68437__pinkyfinger__piano-a.wav")  # Replace with your .wav file path


def play_note():
    # Play the note sound
    note_sound.play()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Check if the 'p' key is pressed
            if event.key == pygame.K_h:
                play_note()

    # Update the display (not strictly necessary for audio but required for event handling)
    pygame.display.flip()
