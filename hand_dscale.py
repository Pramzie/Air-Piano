import cv2
import threading
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector #type: ignore

# 🎹 Initialize Pygame MIDI
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)  # 0 = Acoustic Grand Piano

# 🎼 MIDI Instrument List (use General MIDI instrument numbers)
instruments = [
    (0, "Acoustic Grand Piano"),
    (24, "Nylon Guitar"),
    (40, "Violin"),
    (56, "Trumpet"),
    (73, "Flute"),
    (118, "Synth Drum")
]
instrument_index = 0
current_instrument = instruments[instrument_index]
player.set_instrument(current_instrument[0])

# 🎐 Initialize Hand Detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

# 🎺 Chord Mapping for Fingers (D Major Scale)
chords = {
    "left": {
        "thumb": [62, 66, 69],   # D Major (D, F#, A)
        "index": [64, 67, 71],   # E Minor (E, G, B)
        "middle": [66, 69, 73],  # F# Minor (F#, A, C#)
        "ring": [67, 71, 74],    # G Major (G, B, D)
        "pinky": [69, 73, 76]    # A Major (A, C#, E)
    },
    "right": {
        "thumb": [62, 66, 69],   # D Major (D, F#, A)
        "index": [64, 67, 71],   # E Minor (E, G, B)
        "middle": [66, 69, 73],  # F# Minor (F#, A, C#)
        "ring": [67, 71, 74],    # G Major (G, B, D)
        "pinky": [69, 73, 76]    # A Major (A, C#, E)
    }
}

# Sustain Time (in seconds) after the finger is lowered
SUSTAIN_TIME = 2.0

# Track Previous States to Stop Chords
prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

# 🎵 Function to Play a Chord
def play_chord(chord_notes):
    for note in chord_notes:
        player.note_on(note, 127)  # Start playing

# 🎵 Function to Stop a Chord After a Delay
def stop_chord_after_delay(chord_notes):
    time.sleep(SUSTAIN_TIME)  # Sustain for specified time
    for note in chord_notes:
        player.note_off(note, 127)  # Stop playing

# Instrument name display timeout
INSTRUMENT_DISPLAY_TIME = 3.0
last_instrument_change = time.time() - INSTRUMENT_DISPLAY_TIME  # Init to hide immediately

while True:
    success, img = cap.read()
    if not success:
        print("❌ Camera not capturing frames")
        continue

    hands, img = detector.findHands(img, draw=True)

    if hands:
        for hand in hands:
            hand_type = "left" if hand["type"] == "Left" else "right"
            fingers = detector.fingersUp(hand)
            finger_names = ["thumb", "index", "middle", "ring", "pinky"]

            for i, finger in enumerate(finger_names):
                if finger in chords[hand_type]:  # Only check assigned chords
                    if fingers[i] == 1 and prev_states[hand_type][finger] == 0:
                        play_chord(chords[hand_type][finger])  # Play chord
                    elif fingers[i] == 0 and prev_states[hand_type][finger] == 1:
                        threading.Thread(target=stop_chord_after_delay, args=(chords[hand_type][finger],), daemon=True).start()
                    prev_states[hand_type][finger] = fingers[i]  # Update state
    else:
        # If no hands detected, stop all chords after delay
        for hand in chords:
            for finger in chords[hand]:
                threading.Thread(target=stop_chord_after_delay, args=(chords[hand][finger],), daemon=True).start()
        prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

    # Show instrument within display timeout
    if time.time() - last_instrument_change < INSTRUMENT_DISPLAY_TIME:
        cv2.putText(img, f"Instrument: {current_instrument[1]}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Hand Tracking MIDI Chords", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):  # Spacebar to cycle instrument
        instrument_index = (instrument_index + 1) % len(instruments)
        current_instrument = instruments[instrument_index]
        player.set_instrument(current_instrument[0])
        last_instrument_change = time.time()
        print(f"🎹 Switched to: {current_instrument[1]}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.midi.quit()
