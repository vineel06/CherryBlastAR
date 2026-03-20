import mediapipe as mp
import cv2
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.pinch_threshold = 35
        self.prev_pinch = [False, False]

    def find_hand_landmarks(self, frame):
        """Returns list of hand landmarks (each hand is a list of (x,y) tuples)."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        all_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = frame.shape
                landmarks = []
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((cx, cy))
                all_landmarks.append(landmarks)
        return all_landmarks

    def detect_pinch(self, landmarks):
        if len(landmarks) < 21:
            return False
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_tip))
        return distance < self.pinch_threshold

    def get_shoot_position(self, landmarks):
        if len(landmarks) >= 21:
            return landmarks[8]
        return None