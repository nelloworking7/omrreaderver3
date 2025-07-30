import cv2
import numpy as np

def detect_markings(img, y_grid, num_choices=5, mark_threshold=150):
    """
    각 문제별, 선택지별 마킹 감지 후 선택 번호 반환
    - img: 컬러 이미지 (BGR)
    - y_grid: y축 문제 경계 리스트 (len = 문항수+1)
    - num_choices: 선택지 개수 (기본 5)
    - mark_threshold: 마킹 인식 임계값 (검은색 정도)

    반환: [선택지 번호(1~5), ...] 문항 수만큼 리스트
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, mark_threshold, 255, cv2.THRESH_BINARY_INV)
    h, w = gray.shape

    choice_width = w // num_choices

    detected_answers = []
    for i in range(len(y_grid)-1):
        y_top = y_grid[i]
        y_bottom = y_grid[i+1]

        max_black = 0
        selected_choice = 0
        for choice in range(num_choices):
            x_left = choice * choice_width
            x_right = x_left + choice_width

            roi = binary[y_top:y_bottom, x_left:x_right]
            black_pixels = cv2.countNonZero(roi)

            if black_pixels > max_black:
                max_black = black_pixels
                selected_choice = choice + 1
        
        # 검출된 마킹이 너무 작으면(흑색 픽셀 적으면) 0으로 처리(마킹 안 됨)
        if max_black < 50:
            selected_choice = 0

        detected_answers.append(selected_choice)

    return detected_answers