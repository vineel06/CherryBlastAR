import cv2
import numpy as np

def draw_ui(frame, score, remaining_time=None):
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (280, 90), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, f"SCORE: {score}", (20, 45), font, 1, (0, 255, 255), 2)
    if remaining_time is not None:
        mins = int(remaining_time // 60)
        secs = int(remaining_time % 60)
        cv2.putText(frame, f"TIME: {mins:02d}:{secs:02d}", (20, 80), font, 0.8, (255, 255, 0), 2)

def draw_crosshair(frame, pos, color=(0,255,0)):
    if pos:
        x, y = pos
        cv2.circle(frame, (x, y), 15, color, 2)
        cv2.circle(frame, (x, y), 3, color, -1)
        cv2.line(frame, (x-25, y), (x-10, y), color, 2)
        cv2.line(frame, (x+10, y), (x+25, y), color, 2)
        cv2.line(frame, (x, y-25), (x, y-10), color, 2)
        cv2.line(frame, (x, y+10), (x, y+25), color, 2)

def draw_game_over(frame, score1, score2=None, high_score=None):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    font = cv2.FONT_HERSHEY_TRIPLEX
    cv2.putText(frame, "GAME OVER", (w//2-150, h//2-90), font, 2, (0, 0, 255), 3)
    if score2 is None:
        cv2.putText(frame, f"YOUR SCORE: {score1}", (w//2-130, h//2-20), font, 1, (255, 255, 255), 2)
    else:
        cv2.putText(frame, f"PLAYER 1: {score1}   PLAYER 2: {score2}", (w//2-200, h//2-20), font, 1, (255, 255, 255), 2)
    if high_score is not None:
        cv2.putText(frame, f"HIGH SCORE: {high_score}", (w//2-120, h//2+40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, "Press R to Restart | Q to Quit", (w//2-250, h//2+100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def draw_menu(frame, width, height, high_score):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    cv2.putText(frame, "CherryBlastAR", (width//2-150, height//2-120), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 255), 3)
    cv2.putText(frame, f"HIGH SCORE: {high_score}", (width//2-100, height//2-70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, "1 - Single Player", (width//2-100, height//2-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "2 - Multiplayer", (width//2-100, height//2+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "3 - Time Challenge", (width//2-100, height//2+80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "Q - Quit", (width//2-100, height//2+130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

def draw_time_menu(frame, width, height):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    cv2.putText(frame, "Select Time", (width//2-80, height//2-50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, "1 - 1 Minute", (width//2-100, height//2+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "2 - 2 Minutes", (width//2-100, height//2+60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "3 - 5 Minutes", (width//2-100, height//2+110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "Press ESC to go back", (width//2-150, height//2+170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)