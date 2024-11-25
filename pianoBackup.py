import pygame
import numpy as np

# Farben definieren
white = (255, 255, 255)
black = (0, 0, 0)

# Fenstergröße
width = 700
height = 200

# Fenster erstellen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Klavier')

# Töne und ihre entsprechenden Frequenzen (in Hertz)
notes = {
    pygame.K_a: 261.63,  # C4
    pygame.K_s: 293.66,  # D4
    pygame.K_d: 329.63,  # E4
    pygame.K_f: 349.23,  # F4
    pygame.K_g: 392.00,  # G4
    pygame.K_h: 440.00,  # A4
    pygame.K_j: 493.88,   # B4
    pygame.K_k: 523.26   # B4
}

# Pygame-Mixer initialisieren
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

def generate_piano_wave(frequency, duration, sample_rate=44100):
    """
    Erzeugt einen Klavierton für eine bestimmte Frequenz mit Obertönen.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Grundfrequenz
    wave = 0.6 * np.sin(2 * np.pi * frequency * t)
    
    # Obertöne hinzufügen (2x, 3x, 4x der Frequenz)
    wave += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)  # 2. Oberton
    wave += 0.15 * np.sin(2 * np.pi * frequency * 3 * t)  # 3. Oberton
    wave += 0.1 * np.sin(2 * np.pi * frequency * 4 * t)   # 4. Oberton
    
    # Hüllkurve (Attack-Decay-Sustain)
    envelope = np.exp(-3 * t)  # Exponentielles Abklingen
    wave *= envelope
    
    # Normieren und in 16-Bit konvertieren
    audio = (wave * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(audio)

# Hauptschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in notes:
                frequency = notes[event.key]
                sound = generate_piano_wave(frequency, 1.0)  # 1 Sekunde Ton
                sound.play()

    # Bildschirm aktualisieren
    screen.fill(white)
    pygame.display.flip()

# Pygame beenden
pygame.quit()
