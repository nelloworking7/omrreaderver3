import cv2

def draw_grid(img, y_grid, num_choices=5):
    img_copy = img.copy()
    h, w, _ = img.shape

    for y in y_grid:
        cv2.line(img_copy, (0, y), (w, y), (0, 255, 0), 2)

    choice_width = w // num_choices
    for c in range(num_choices + 1):
        x = c * choice_width
        cv2.line(img_copy, (x, 0), (x, h), (255, 0, 0), 2)
    
    return img_copy