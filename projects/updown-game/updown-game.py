"""
[업다운 게임]
- 1~100 사이 랜덤 숫자를 맞추는 게임
- 사용자 입력에 따라 업/다운 힌트 제공
- 정답 시 게임 종료
- 다시 시작 기능 포함
"""

import flet as ft
import random

def main(page: ft.Page):
    # 페이지 기본 설정
    page.title = "업다운 게임"

    answer = random.randint(1, 100)  # 정답 숫자 생성
    attempts = 0                     # 시도 횟수

    # UI 텍스트 요소
    result_text = ft.Text("1부터 100 사이 숫자를 맞춰보세요!")
    attempt_text = ft.Text("시도 횟수: 0")

    # 사용자 입력 필드
    user_input = ft.TextField(label="숫자 입력", width=200)

    # --- [정답 확인 함수] ---
    def check_number(e):
        nonlocal answer, attempts

        # 입력값이 없는 경우
        if user_input.value == "":
            result_text.value = "숫자를 입력하세요!"
        else:
            try:
                user_number = int(user_input.value)
                attempts += 1
                attempt_text.value = f"시도 횟수: {attempts}"

                # 업 / 다운 판정
                if user_number < answer:
                    result_text.value = "업!"
                elif user_number > answer:
                    result_text.value = "다운!"
                else:
                    result_text.value = "정답입니다! 🎉"

            except:
                # 숫자가 아닌 값 입력 시
                result_text.value = "숫자만 입력하세요!"

        page.update()

    # --- [게임 초기화 함수] ---
    def reset_game(e):
        nonlocal answer, attempts

        answer = random.randint(1, 100)  # 새로운 정답 생성
        attempts = 0

        result_text.value = "새 게임 시작!"
        attempt_text.value = "시도 횟수: 0"
        user_input.value = ""

        page.update()

    # 버튼 생성
    submit_btn = ft.ElevatedButton("확인", on_click=check_number)
    reset_btn = ft.ElevatedButton("다시 시작", on_click=reset_game)

    # UI 구성
    page.add(
        result_text,
        attempt_text,
        user_input,
        submit_btn,
        reset_btn
    )

ft.app(target=main)
