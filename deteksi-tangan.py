import cv2
import mediapipe as mp
import pygame
import os

# Inisialisasi pygame mixer
pygame.mixer.init()

# Inisialisasi Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Kamera
cap = cv2.VideoCapture(0)

# Variabel stabilisasi
last_count = -1
stable_count = -1
stable_frames = 0
STABILITY_THRESHOLD = 2

# Mapping jumlah jari ke kata bahasa isyarat sederhana
gesture_words = {
    1: "halo",
    2: "nama",
    3: "saya",
    4: "naufal",
    5: "terimakasih"
}

# --- Pre-generate suara Google & preload ke pygame ---
sounds = {}
for num, word in gesture_words.items():
    filename = f"voice_{word}.mp3"
    if not os.path.exists(filename):
        from gtts import gTTS
        tts = gTTS(text=word, lang="id")
        tts.save(filename)
    sounds[num] = pygame.mixer.Sound(filename)

def speak_word(num):
    if num in sounds:
        sounds[num].play()

# Fungsi cek jari + lingkaran hijau/merah
def count_fingers(hand_landmarks, img):
    finger_tips = [8, 12, 16, 20]  # index, tengah, manis, kelingking
    finger_pips = [6, 10, 14, 18]
    thumb_tip = 4
    thumb_ip = 3

    fingers = []
    h, w, _ = img.shape

    # Tentukan orientasi tangan (kanan/kiri)
    wrist_x = hand_landmarks.landmark[0].x
    index_mcp_x = hand_landmarks.landmark[5].x
    is_right_hand = wrist_x < index_mcp_x

    # --- Deteksi jempol + lingkaran ---
    thumb_tip_x = hand_landmarks.landmark[thumb_tip].x
    thumb_tip_y = hand_landmarks.landmark[thumb_tip].y
    thumb_ip_x = hand_landmarks.landmark[thumb_ip].x
    cx_thumb, cy_thumb = int(thumb_tip_x * w), int(thumb_tip_y * h)

    if is_right_hand:
        if thumb_tip_x < thumb_ip_x:
            fingers.append(0)
            cv2.circle(img, (cx_thumb, cy_thumb), 6, (0, 0, 255), -1)
        else:
            fingers.append(1)
            cv2.circle(img, (cx_thumb, cy_thumb), 6, (0, 255, 0), -1)
    else:
        if thumb_tip_x > thumb_ip_x:
            fingers.append(0)
            cv2.circle(img, (cx_thumb, cy_thumb), 6, (0, 0, 255), -1)
        else:
            fingers.append(1)
            cv2.circle(img, (cx_thumb, cy_thumb), 6, (0, 255, 0), -1)

    # --- Deteksi 4 jari lain + lingkaran ---
    for tip, pip in zip(finger_tips, finger_pips):
        tip_y = hand_landmarks.landmark[tip].y
        pip_y = hand_landmarks.landmark[pip].y
        cx, cy = int(hand_landmarks.landmark[tip].x * w), int(tip_y * h)

        if tip_y < pip_y:  # jari terbuka
            fingers.append(1)
            cv2.circle(img, (cx, cy), 6, (0, 255, 0), -1)
        else:  # jari tertutup
            fingers.append(0)
            cv2.circle(img, (cx, cy), 6, (0, 0, 255), -1)

    return sum(fingers)

try:
    while True:
        success, img = cap.read()
        if not success:
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                finger_count = count_fingers(handLms, img)

                # Stabilitas biar ga salah deteksi
                if finger_count == stable_count:
                    stable_frames += 1
                else:
                    stable_count = finger_count
                    stable_frames = 1

                if stable_frames >= STABILITY_THRESHOLD and finger_count != last_count:
                    if finger_count in gesture_words:
                        kata = gesture_words[finger_count]
                        print(f"Gestur terdeteksi: {kata}")
                        speak_word(finger_count)
                        last_count = finger_count

                    cv2.putText(img, f"Kata: {gesture_words.get(finger_count, '-')}", 
                                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        cv2.imshow("Deteksi Bahasa Isyarat", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

except KeyboardInterrupt:
    print("\n[INFO] Program dihentikan manual dari terminal.")

cap.release()
cv2.destroyAllWindows()
