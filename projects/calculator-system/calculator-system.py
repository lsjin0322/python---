"""
[Smart Calculator]
- 숫자와 문자를 구분 저장
- 사칙연산, 평균, 최댓값/최솟값 계산
- Flet 기반 UI 계산기
"""

import flet as ft


class SmartCalculator:
    def __init__(self):
        self.numbers = []   # 숫자 저장 리스트
        self.strings = []   # 문자열 저장 리스트

    # 입력값을 숫자/문자로 분리 저장
    def add_value(self, value):
        try:
            num = float(value)
            self.numbers.append(num)
        except:
            self.strings.append(value)

    # 덧셈
    def add(self):
        return sum(self.numbers)

    # 뺄셈 (순차 계산)
    def sub(self):
        if not self.numbers:
            return 0
        result = self.numbers[0]
        for n in self.numbers[1:]:
            result -= n
        return result

    # 곱셈
    def mul(self):
        result = 1
        for n in self.numbers:
            result *= n
        return result

    # 나눗셈 (0 체크 포함)
    def div(self):
        if not self.numbers:
            return 0
        result = self.numbers[0]
        for n in self.numbers[1:]:
            if n == 0:
                return "0으로 나눌 수 없음"
            result /= n
        return result

    # 평균
    def avg(self):
        if not self.numbers:
            return 0
        return sum(self.numbers) / len(self.numbers)

    # 최댓값
    def max(self):
        if not self.numbers:
            return None
        return max(self.numbers)

    # 최솟값
    def min(self):
        if not self.numbers:
            return None
        return min(self.numbers)


def main(page: ft.Page):
    # 페이지 기본 설정
    page.title = "Smart Input Calculator"
    page.bgcolor = "#F4F6F8"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    calc = SmartCalculator()

    # 입력창
    input_field = ft.TextField(
        label="값 입력 후 Enter",
        autofocus=True,
        border_radius=12,
        bgcolor="white"
    )

    # 표시 영역
    number_view = ft.Column(spacing=5)
    string_view = ft.Column(spacing=5)
    result_text = ft.Text(size=18, weight="bold", color="#2F6F3E")

    # 화면 업데이트 (숫자/문자 표시)
    def update_view():
        number_view.controls.clear()
        string_view.controls.clear()

        for n in calc.numbers:
            number_view.controls.append(
                ft.Container(
                    content=ft.Text(str(n)),
                    padding=8,
                    bgcolor="#E8F5E9",
                    border_radius=8
                )
            )

        for s in calc.strings:
            string_view.controls.append(
                ft.Container(
                    content=ft.Text(str(s)),
                    padding=8,
                    bgcolor="#FFF3E0",
                    border_radius=8
                )
            )

        page.update()

    # Enter 입력 처리
    def on_submit(e):
        value = input_field.value.strip()
        if value == "":
            return

        calc.add_value(value)
        input_field.value = ""
        input_field.focus()  # 입력 유지
        update_view()

    input_field.on_submit = on_submit

    # 계산 실행
    def run_calc(func):
        if not calc.numbers:
            result_text.value = "숫자가 없습니다"
        else:
            result = getattr(calc, func)()
            result_text.value = f"{func} 결과: {result}"
        input_field.focus()
        page.update()

    # 버튼 생성 함수
    def calc_button(text, func, color):
        return ft.ElevatedButton(
            text,
            on_click=lambda e: run_calc(func),
            style=ft.ButtonStyle(
                bgcolor=color,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=10
            ),
            expand=True
        )

    # UI 구성
    page.add(
        ft.Container(
            width=600,
            padding=20,
            bgcolor="white",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000015"),
            content=ft.Column([

                ft.Text("🧮 Smart Calculator", size=26, weight="bold", color="#2F6F3E"),

                input_field,

                ft.Row([
                    ft.Container(
                        expand=1,
                        content=ft.Column([
                            ft.Text("🔢 숫자", weight="bold"),
                            number_view
                        ])
                    ),
                    ft.Container(
                        expand=1,
                        content=ft.Column([
                            ft.Text("🔤 문자", weight="bold"),
                            string_view
                        ])
                    ),
                ]),

                ft.Divider(),

                ft.Row([
                    calc_button("더하기", "add", "#4CAF50"),
                    calc_button("빼기", "sub", "#66BB6A"),
                    calc_button("곱하기", "mul", "#81C784"),
                    calc_button("나누기", "div", "#A5D6A7"),
                ]),

                ft.Row([
                    calc_button("평균", "avg", "#388E3C"),
                    calc_button("최댓값", "max", "#2E7D32"),
                    calc_button("최솟값", "min", "#1B5E20"),
                ]),

                ft.Divider(),

                result_text

            ], spacing=15)
        )
    )


ft.app(target=main) 
