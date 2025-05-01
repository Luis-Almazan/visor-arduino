import cv2
import mediapipe as mp
import serial
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

arduino = serial.Serial('COM3', 9600)
print("Sistema iniciado. Mostrando dedos en consola...")

cap = cv2.VideoCapture(0)
prev_fingers = 0
last_update_time = time.time()

while True:
    success, img = cap.read()
    if not success:
        break
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            fingers_up = 0

            # Dedos índice, medio, anular, meñique (eje Y)
            for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                if landmarks[tip].y < landmarks[pip].y - 0.05:  # Offset ajustable
                    fingers_up += 1

            # Pulgar (eje X + filtro de posición)
            thumb_tip = landmarks[4]
            thumb_ip = landmarks[3]
            wrist = landmarks[0]

            # Solo contar el pulgar si está claramente extendido
            if (thumb_tip.x < thumb_ip.x and thumb_tip.x < wrist.x - 0.05) or \
               (thumb_tip.x > thumb_ip.x and thumb_tip.x > wrist.x + 0.05):
                fingers_up += 1

            finger_count = fingers_up
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Filtrar cambios bruscos (evitar parpadeo)
    current_time = time.time()
    if finger_count != prev_fingers and (current_time - last_update_time) > 0.5:  # 0.5s de delay
        print(f"Dedos detectados: {finger_count}") 
        arduino.write(str(finger_count).encode())
        prev_fingers = finger_count
        last_update_time = current_time

    cv2.putText(img, f"Dedos: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Contador de Dedos", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()