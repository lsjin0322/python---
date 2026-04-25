"""
[볼링 전광판 프로그램]
- 볼링 점수를 입력하면 전광판 형태로 표시
- 스트라이크 / 스페어 / 일반 점수 처리
- 누적 점수 자동 계산
- GUI 버튼으로 점수 입력
"""

import flet as ft

def main(page: ft.Page):
    page.title = "볼링 전광판"
    page.window_width = 1100
    page.padding = 20
    page.scroll = "auto" 

    # --- [데이터 관리] ---
    all_rolls = []                     # 모든 투구 기록
    display_data = ["" for _ in range(10)]  # 화면 표시용 데이터
    cumulative_scores = [None for _ in range(10)]  # 누적 점수
    current_frame = 0                  # 현재 프레임
    is_second_roll = False             # 두 번째 투구 여부

    # --- [점수 계산 함수] ---
    def calculate_scores():
        nonlocal cumulative_scores
        new_scores = [None] * 10
        total = 0
        r_idx = 0
        
        try:
            for f in range(10):
                # 스트라이크 처리
                if all_rolls[r_idx] == 10:
                    score = 10 + all_rolls[r_idx + 1] + all_rolls[r_idx + 2]
                    total += score
                    r_idx += 1

                # 스페어 처리
                elif all_rolls[r_idx] + all_rolls[r_idx + 1] == 10:
                    score = 10 + all_rolls[r_idx + 2]
                    total += score
                    r_idx += 2

                # 일반 점수 처리
                else:
                    score = all_rolls[r_idx] + all_rolls[r_idx + 1]
                    total += score
                    r_idx += 2

                new_scores[f] = total

        except IndexError:
            # 아직 점수가 완전히 계산되지 않은 경우 무시
            pass

        cumulative_scores = new_scores

    # --- [점수 입력 이벤트] ---
    def handle_score(e):
        nonlocal current_frame, is_second_roll
        val = int(e.control.data)
        
        # 10프레임 이후 입력 제한
        if current_frame > 9:
            return

        # 투구 기록 저장
        all_rolls.append(val)

        # --- [표시 로직] ---
        if current_frame < 9:  # 1~9프레임
            if not is_second_roll:
                if val == 10:  # 스트라이크
                    display_data[current_frame] = "X"
                    current_frame += 1
                else:
                    display_data[current_frame] = str(val)
                    is_second_roll = True
            else:  # 두 번째 투구
                if display_data[current_frame] != "10" and int(display_data[current_frame]) + val == 10:
                    display_data[current_frame] += " | /"  # 스페어
                else:
                    display_data[current_frame] += f" | {val}"
                is_second_roll = False
                current_frame += 1

        else:  # 10프레임
            if display_data[9] == "":
                display_data[9] = "X" if val == 10 else str(val)
            else:
                prev = display_data[9].split(" | ")[-1]
                char = "X" if val == 10 else "/" if (prev != "X" and prev != "/" and int(prev) + val == 10) else str(val)
                display_data[9] += f" | {char}"
            
            # 게임 종료 조건
            d_list = display_data[9].split(" | ")
            if len(d_list) == 2 and "X" not in d_list and "/" not in d_list:
                current_frame += 1
            elif len(d_list) == 3:
                current_frame += 1

        # 점수 계산 및 UI 업데이트
        calculate_scores()
        render_table()
        page.update()

    # --- [테이블 UI] ---
    scoreboard = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("이름"))] + [ft.DataColumn(ft.Text(f"{i+1}F")) for i in range(10)],
        rows=[],
        border=ft.border.all(1, "black")
    )

    # 전광판 렌더링
    def render_table():
        cells = [ft.DataCell(ft.Text("플레이어 1", weight="bold"))]
        for i in range(10):
            cells.append(ft.DataCell(ft.Column([
                ft.Text(display_data[i] if display_data[i] else "-"),  # 투구 표시
                ft.Text(str(cumulative_scores[i]) if cumulative_scores[i] is not None else "", color="blue", weight="bold")  # 누적 점수
            ])))
        scoreboard.rows = [ft.DataRow(cells=cells)]

    # 초기 렌더링
    render_table()

    # UI 구성
    page.add(
        ft.Text("🎳 볼링 전광판", size=24, weight="bold"),
        ft.Row([ft.ElevatedButton(str(i), data=i, on_click=handle_score, width=50) for i in range(11)], wrap=True),
        ft.Divider(),
        scoreboard
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
