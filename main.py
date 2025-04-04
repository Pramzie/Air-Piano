import cv2
import threading
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector

# 🎹 Initialize Pygame MIDI
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)  # 0 = Acoustic Grand Piano

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

    cv2.imshow("Hand Tracking MIDI Chords", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.midi.quit()
