import cv2

def highlight_answers(img, y_grid, detected_answers, answer_key, num_choices=5):
    img_copy = img.copy()
    h, w, _ = img.shape
    choice_width = w // num_choices
    
    for i in range(len(answer_key)):
        y_top = y_grid[i]
        y_bottom = y_grid[i+1]

        detected = detected_answers[i]
        correct = answer_key[i]

        if detected > 0:
            x_left = (detected -1) * choice_width
            x_right = x_left + choice_width
        else:
            x_left = 0
            x_right = 0

        color = (0, 255, 0) if detected == correct else (0, 0, 255)

        cv2.rectangle(img_copy, (0, y_top), (w, y_bottom), color, 2)

        if x_right > 0:
            cv2.rectangle(img_copy, (x_left, y_top), (x_right, y_bottom), color, 3)

    return img_copy