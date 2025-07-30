import cv2
import numpy as np

def find_timing_belt(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    
    h, w = th.shape
    roi = th[int(h*0.7):h, int(w*0.9):w]
    
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    timing_rects = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        if 10 < cw < 50 and 10 < ch < 50:
            timing_rects.append((x, y, cw, ch))
    
    timing_rects = sorted(timing_rects, key=lambda r: r[1])
    
    intervals = [timing_rects[i+1][1] - timing_rects[i][1] for i in range(len(timing_rects)-1)]
    base_interval = int(np.median(intervals))
    
    first_y = timing_rects[0][1]
    
    num_questions = len(timing_rects) - 1
    
    y_grid = [first_y + i * base_interval for i in range(num_questions + 1)]
    y_grid = [int(h*0.7) + y for y in y_grid]
    
    return y_grid, base_interval