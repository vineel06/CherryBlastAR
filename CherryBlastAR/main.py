import cv2
import numpy as np
import time
import os
from hand_tracker import HandTracker
from game import Game
from utils import draw_ui, draw_crosshair, draw_game_over, draw_menu, draw_time_menu

# Load and save high score
def load_high_score():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    tracker = HandTracker()

    high_score = load_high_score()

    state = "menu"          # menu, time_menu, playing, game_over
    mode = None             # single, multi, time
    time_limit = None
    start_time = None
    game = None
    game1 = None
    game2 = None
    pinch_cooldown = [0, 0]
    final_score1 = 0
    final_score2 = 0

    # Sound
    try:
        import pygame
        pygame.mixer.init()
        pop_sound = pygame.mixer.Sound("assets/sounds/pop.wav")
        bomb_sound = pygame.mixer.Sound("assets/sounds/bomb.wav")
        pop_sound.set_volume(1.0)
        bomb_sound.set_volume(1.0)
        sound_enabled = True
    except:
        sound_enabled = False

    cv2.namedWindow("CherryBlastAR", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("CherryBlastAR", 640, 480)
    logical_width = 640
    logical_height = 480

    def get_scaled_frame(frame, window_size):
        h, w = frame.shape[:2]
        win_w, win_h = window_size
        if win_w <= 0 or win_h <= 0:
            return frame
        scale = min(win_w/w, win_h/h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(frame, (new_w, new_h))
        canvas = np.zeros((win_h, win_w, 3), dtype=np.uint8)
        x_offset = (win_w - new_w) // 2
        y_offset = (win_h - new_h) // 2
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        return canvas

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        # Check if window is closed
        try:
            if cv2.getWindowProperty("CherryBlastAR", cv2.WND_PROP_VISIBLE) < 1:
                break
        except:
            pass

        try:
            window_rect = cv2.getWindowImageRect("CherryBlastAR")
            win_w, win_h = window_rect[2], window_rect[3]
        except:
            win_w, win_h = 640, 480

        if state == "menu":
            draw_menu(frame, logical_width, logical_height, high_score)
            scaled = get_scaled_frame(frame, (win_w, win_h))
            cv2.imshow("CherryBlastAR", scaled)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('1'):
                state = "playing"
                mode = "single"
                game = Game(logical_width, logical_height)
                start_time = time.time()
                final_score1 = 0
            elif key == ord('2'):
                state = "playing"
                mode = "multi"
                game1 = Game(logical_width//2, logical_height)
                game2 = Game(logical_width//2, logical_height)
                start_time = time.time()
                final_score1 = 0
                final_score2 = 0
            elif key == ord('3'):
                state = "time_menu"

        elif state == "time_menu":
            draw_time_menu(frame, logical_width, logical_height)
            scaled = get_scaled_frame(frame, (win_w, win_h))
            cv2.imshow("CherryBlastAR", scaled)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('1'):
                time_limit = 60
                state = "playing"
                mode = "time"
                game = Game(logical_width, logical_height)
                start_time = time.time()
                final_score1 = 0
            elif key == ord('2'):
                time_limit = 120
                state = "playing"
                mode = "time"
                game = Game(logical_width, logical_height)
                start_time = time.time()
                final_score1 = 0
            elif key == ord('3'):
                time_limit = 300
                state = "playing"
                mode = "time"
                game = Game(logical_width, logical_height)
                start_time = time.time()
                final_score1 = 0
            elif key == 27:  # ESC
                state = "menu"

        elif state == "playing":
            if mode == "single" or mode == "time":
                hands = tracker.find_hand_landmarks(frame)
                if hands:
                    landmarks = hands[0]
                    pinch = tracker.detect_pinch(landmarks)
                    shoot_pos = tracker.get_shoot_position(landmarks)
                    if pinch and not tracker.prev_pinch[0] and pinch_cooldown[0] <= 0:
                        if shoot_pos:
                            game_over, hit = game.shoot(shoot_pos)
                            if hit and sound_enabled:
                                if game_over:
                                    bomb_sound.play()
                                else:
                                    pop_sound.play()
                        pinch_cooldown[0] = 8
                    tracker.prev_pinch[0] = pinch
                    if pinch_cooldown[0] > 0:
                        pinch_cooldown[0] -= 1
                    game.update()
                else:
                    game.update()

                # Time challenge check
                remaining = None
                if mode == "time":
                    elapsed = time.time() - start_time
                    remaining = max(0, time_limit - elapsed)
                    if remaining <= 0:
                        state = "game_over"
                        final_score1 = game.score
                        final_score2 = None
                        if final_score1 > high_score:
                            high_score = final_score1
                            save_high_score(high_score)

                # Draw game on camera frame
                game.draw_balloons(frame)
                game.draw_particles(frame)
                draw_ui(frame, game.score, remaining)
                if hands:
                    draw_crosshair(frame, shoot_pos, (0,0,255) if pinch else (0,255,0))

                # Single player game over (bomb hit)
                if game.game_over:
                    state = "game_over"
                    final_score1 = game.score
                    final_score2 = None
                    if final_score1 > high_score:
                        high_score = final_score1
                        save_high_score(high_score)

            elif mode == "multi":
                hands = tracker.find_hand_landmarks(frame)
                left_hand = None
                right_hand = None
                for h in hands:
                    if h:
                        center_x = h[8][0]
                        if center_x < logical_width // 2:
                            left_hand = h
                        else:
                            right_hand = h

                # Left player
                if left_hand:
                    pinch_left = tracker.detect_pinch(left_hand)
                    shoot_pos_left = tracker.get_shoot_position(left_hand)
                    if pinch_left and not tracker.prev_pinch[0] and pinch_cooldown[0] <= 0:
                        if shoot_pos_left:
                            game_over1, hit1 = game1.shoot(shoot_pos_left)
                            if hit1 and sound_enabled:
                                if game_over1:
                                    bomb_sound.play()
                                else:
                                    pop_sound.play()
                        pinch_cooldown[0] = 8
                    tracker.prev_pinch[0] = pinch_left
                    if pinch_cooldown[0] > 0:
                        pinch_cooldown[0] -= 1

                # Right player
                if right_hand:
                    pinch_right = tracker.detect_pinch(right_hand)
                    shoot_pos_right = tracker.get_shoot_position(right_hand)
                    if pinch_right and not tracker.prev_pinch[1] and pinch_cooldown[1] <= 0:
                        if shoot_pos_right:
                            right_shoot = (shoot_pos_right[0] - logical_width//2, shoot_pos_right[1])
                            game_over2, hit2 = game2.shoot(right_shoot)
                            if hit2 and sound_enabled:
                                if game_over2:
                                    bomb_sound.play()
                                else:
                                    pop_sound.play()
                        pinch_cooldown[1] = 8
                    tracker.prev_pinch[1] = pinch_right
                    if pinch_cooldown[1] > 0:
                        pinch_cooldown[1] -= 1

                # Update games
                game1.update()
                game2.update()

                # Draw left half on original frame
                left_roi = frame[:, :logical_width//2]
                game1.draw_balloons(left_roi)
                game1.draw_particles(left_roi)
                draw_ui(left_roi, game1.score, None)
                if left_hand:
                    draw_crosshair(left_roi, shoot_pos_left, (0,0,255) if pinch_left else (0,255,0))

                # Draw right half
                right_roi = frame[:, logical_width//2:]
                game2.draw_balloons(right_roi)
                game2.draw_particles(right_roi)
                draw_ui(right_roi, game2.score, None)
                if right_hand:
                    adjusted_x = shoot_pos_right[0] - logical_width//2
                    draw_crosshair(right_roi, (adjusted_x, shoot_pos_right[1]), (0,0,255) if pinch_right else (0,255,0))

                # Draw dividing line
                cv2.line(frame, (logical_width//2, 0), (logical_width//2, logical_height), (255,255,255), 2)

                # Multiplayer game over
                if game1.game_over or game2.game_over:
                    state = "game_over"
                    final_score1 = game1.score
                    final_score2 = game2.score
                    max_score = max(final_score1, final_score2)
                    if max_score > high_score:
                        high_score = max_score
                        save_high_score(high_score)

            scaled = get_scaled_frame(frame, (win_w, win_h))
            cv2.imshow("CherryBlastAR", scaled)

        elif state == "game_over":
            # Show game over screen with scores
            if mode == "multi":
                draw_game_over(frame, final_score1, final_score2, high_score)
            else:
                draw_game_over(frame, final_score1, None, high_score)
            scaled = get_scaled_frame(frame, (win_w, win_h))
            cv2.imshow("CherryBlastAR", scaled)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                # Reset everything
                state = "menu"
                mode = None
                game = None
                game1 = None
                game2 = None
                time_limit = None
                start_time = None
                tracker.prev_pinch = [False, False]
                pinch_cooldown = [0, 0]
                final_score1 = 0
                final_score2 = 0
            elif key == ord('q'):
                break

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()