# Air-Piano🎹:

Control MIDI piano chords in real-time using hand gestures captured from your webcam. Each finger is mapped to a chord in the D major scale, and chords play and sustain naturally as you move your fingers.

---

## 📦 Features

- 🖐️ Real-time hand detection using [cvzone](https://github.com/cvzone/cvzone)
- 🎼 Chord mapping to fingers (D major scale)
- 🎹 MIDI output with sustain effect using `pygame.midi`
- 👏 Supports both left and right hands
- 🎶 Dynamic gesture-based music interaction

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hand-midi-chords.git
cd hand-midi-chords
```

### 2. Install Dependencies

Make sure Python 3.7+ is installed.

```bash
pip install opencv-python pygame cvzone
```

> If `cvzone` is not found, install directly from GitHub:
```bash
pip install git+https://github.com/cvzone/cvzone.git
```

---

## 🎛️ How It Works

- The webcam detects your hands in real-time using `cvzone`’s `HandDetector`.
- Each finger corresponds to a specific chord (left and right hands are mapped identically).
- When a finger is raised (`fingersUp`), a chord is played.
- When the finger is lowered, the chord sustains for a short delay before stopping.

### 🎵 Chord Mapping (D Major Scale)

| Finger  | Chord (Notes)        | Description        |
|---------|----------------------|--------------------|
| Thumb   | D Major (62, 66, 69) | D - F# - A          |
| Index   | E Minor (64, 67, 71) | E - G - B           |
| Middle  | F# Minor (66, 69, 73)| F# - A - C#         |
| Ring    | G Major (67, 71, 74) | G - B - D           |
| Pinky   | A Major (69, 73, 76) | A - C# - E          |

Both hands use the same chord mapping.

---

## 🧠 Code Overview

- `pygame.midi.init()` initializes MIDI output.
- `cvzone.HandTrackingModule.HandDetector` handles hand and finger tracking.
- `fingersUp()` determines which fingers are raised.
- MIDI notes are triggered with `note_on` and `note_off` functions.
- Chords are sustained for a configurable delay (`SUSTAIN_TIME = 2.0`).

---

## 💡 Customization

- 🔁 **Change Instrument**:  
  Modify the instrument using:
  ```python
  player.set_instrument(<instrument_number>)
  ```
  Refer to the [General MIDI Instrument List](https://www.midi.org/specifications-old/item/gm-level-1-sound-set) for codes.

- 🎼 **Change Chord Scale**:  
  Replace the `chords` dictionary with your preferred scales or custom mappings.

- ⏱️ **Adjust Sustain Time**:  
  Modify `SUSTAIN_TIME` (in seconds) to lengthen or shorten the delay after chord release.

---

## 🛑 Exit Instructions

- Press `q` on your keyboard to quit the application safely.
- This releases the webcam and MIDI resources.

---

## 🤝 Credits

- [cvzone by Murtaza Hassan](https://github.com/cvzone/cvzone)
- `pygame.midi` for MIDI interfacing
- OpenCV for real-time camera input

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).


Code for Offcampus by AWS: 99RNYA
---
