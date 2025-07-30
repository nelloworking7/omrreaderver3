import streamlit as st
import cv2
import numpy as np
from timing_belt import find_timing_belt
from draw_grid import draw_grid
from highlight import highlight_answers
from marking_detection import detect_markings

st.title("OMR 자동채점 웹앱 (타이밍벨트 기반)")

uploaded_file = st.file_uploader("OMR 이미지 업로드", type=['jpg','png','jpeg'])
num_choices = 5

num_questions = st.number_input("문항 수 입력", min_value=1, max_value=100, value=5)
st.write("정답을 입력하세요.")
answer_key = []
for i in range(num_questions):
    ans = st.selectbox(f"{i+1}번 문제 정답", options=[1,2,3,4,5], index=0, key=f"ans_{i}")
    answer_key.append(ans)

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    y_grid, base_interval = find_timing_belt(img)
    img_grid = draw_grid(img, y_grid, num_choices)
    st.image(img_grid, caption="타이밍벨트 기반 그리드 시각화", use_column_width=True)

    detected_answers = detect_markings(img, y_grid, num_choices)
    
    img_highlight = highlight_answers(img, y_grid, detected_answers, answer_key, num_choices)
    st.image(img_highlight, caption="오답 표시 및 정답 비교", use_column_width=True)

    score = sum([1 for d,a in zip(detected_answers, answer_key) if d==a])
    st.write(f"점수: {score} / {num_questions}")

else:
    st.write("OMR 이미지를 업로드해주세요.")