import cv2
import numpy as np
import mediapipe as mp

# ---------------- Mediapipe setup ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# ---------------- Colors ----------------
colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255),(0,0,0)]
color_names = ["BLUE","GREEN","RED","YELLOW","ERASER"]
draw_color = colors[0]

# ---------------- Setup ----------------
cap = cv2.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))
canvas = np.zeros((height,width,3),np.uint8)

# ---------------- Drawing variables ----------------
prev_x, prev_y = None, None
brush_thickness = 4
undo_stack = []
redo_stack = []

# ---------------- Button positions ----------------
button_y1, button_y2 = 1, 65
button_positions = {
    "CLEAR": (20,button_y1,120,button_y2),
    "SAVE": (540,button_y1,640,button_y2),
}

for i in range(len(colors)):
    button_positions[color_names[i]] = (140+i*100,button_y1,220+i*100,button_y2)

# ---------------- Finger Detection ----------------
def fingers_up(hand_landmarks):
    fingers = []

    # Index finger
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle finger
    if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers

# ---------------- Main Loop ----------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame,1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # ---------------- Draw Buttons ----------------
    cv2.rectangle(frame, button_positions["CLEAR"][:2], button_positions["CLEAR"][2:], (122,122,122), -1)
    cv2.putText(frame,"CLEAR",(35,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    cv2.rectangle(frame, button_positions["SAVE"][:2], button_positions["SAVE"][2:], (122,122,122), -1)
    cv2.putText(frame,"SAVE",(555,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    for i,col in enumerate(colors):
        x1,y1,x2,y2 = button_positions[color_names[i]]
        cv2.rectangle(frame,(x1,y1),(x2,y2),col,-1)
        cv2.putText(frame,color_names[i],(x1+5,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

    # ---------------- Hand Detection ----------------
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            h,w,c = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            cv2.circle(frame,(x,y),8,(255,0,0),-1)

            # ---------------- Button Click ----------------
            if y < button_y2:

                for name,(x1,y1,x2,y2) in button_positions.items():

                    if x1 < x < x2:

                        if name == "CLEAR":
                            canvas = np.zeros((height,width,3),np.uint8)
                            undo_stack.clear()
                            redo_stack.clear()

                        elif name == "SAVE":
                            cv2.imwrite("drawing.png",canvas)

                        elif name in color_names:
                            draw_color = colors[color_names.index(name)]

                prev_x, prev_y = None, None

            # ---------------- Drawing Area ----------------
            else:

                finger_state = fingers_up(hand_landmarks)

                # Draw only when index finger is up
                if finger_state == [1,0]:

                    if prev_x is not None and prev_y is not None:
                        undo_stack.append(canvas.copy())
                        redo_stack.clear()

                        cv2.line(canvas,
                                 (prev_x,prev_y),
                                 (x,y),
                                 draw_color,
                                 brush_thickness)

                    prev_x, prev_y = x, y

                # Pause when index + middle finger up
                elif finger_state == [1,1]:
                    prev_x, prev_y = None, None

    else:
        prev_x, prev_y = None, None

    # ---------------- Display ----------------
    cv2.imshow("Camera Feed",frame)
    cv2.imshow("Drawing Pad",canvas)

    key = cv2.waitKey(1) & 0xFF

    # ---------------- Keyboard Controls ----------------
    if key == ord('q'):
        break

    elif key == ord('u'):  # Undo
        if undo_stack:
            redo_stack.append(canvas.copy())
            canvas = undo_stack.pop()

    elif key == ord('r'):  # Redo
        if redo_stack:
            undo_stack.append(canvas.copy())
            canvas = redo_stack.pop()

    elif key == ord('+'):  # Increase brush
        brush_thickness += 1

    elif key == ord('-'):  # Decrease brush
        brush_thickness = max(1, brush_thickness-1)

cap.release()
cv2.destroyAllWindows()