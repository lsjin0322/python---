"""
[주소록 프로그램]
- 이름을 기준으로 전화번호, 주소, 직업 정보 관리
- 검색 / 등록 / 수정 / 삭제 기능 제공
- JSON 파일을 통한 데이터 영구 저장
"""

import flet as ft
import json


class AddressBook:
    def __init__(self):
        self.data = {}  # 전체 주소 데이터 저장

    # 데이터 추가
    def add(self, name, phone, address, job):
        self.data[name] = {
            "phone": phone,
            "address": address,
            "job": job
        }

    # 이름 또는 전화번호 기반 검색
    def search(self, keyword):
        result = []
        for name, info in self.data.items():
            if keyword in name or keyword in info["phone"]:
                result.append((name, info))
        return result

    # 일부 정보만 수정
    def update_partial(self, name, phone, address, job):
        if name in self.data:
            if phone:
                self.data[name]["phone"] = phone
            if address:
                self.data[name]["address"] = address
            if job:
                self.data[name]["job"] = job
            return True
        return False

    # 데이터 삭제
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    # JSON 저장
    def save_data(self):
        with open("address.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # JSON 로드
    def load_data(self):
        try:
            with open("address.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except:
            self.data = {}


def main(page: ft.Page):
    book = AddressBook()
    book.load_data()  # 프로그램 시작 시 데이터 불러오기

    selected_name = {"value": None}  # 선택된 사용자 저장

    page.title = "주소록"
    page.bgcolor = "#F5F5F7"
    page.scroll = ft.ScrollMode.AUTO

    # 입력창 스타일 함수
    def input_style(label):
        return ft.TextField(
            label=label,
            border_radius=12,
            filled=True,
            bgcolor="#FFFFFF",
            border_color="#E5E7EB",
            expand=True
        )

    # 입력 필드
    name_input = input_style("이름")
    phone_input = input_style("전화번호")
    address_input = input_style("주소")
    job_input = input_style("직업")
    search_input = input_style("검색")

    # 결과 영역
    result_view = ft.Row(wrap=True, spacing=10, run_spacing=10, expand=True)
    result_text = ft.Text(color="#6B7280")

    # 카드 클릭 시 입력창 자동 채움
    def fill_inputs(name, info):
        selected_name["value"] = name
        name_input.value = name
        phone_input.value = info["phone"]
        address_input.value = info["address"]
        job_input.value = info["job"]
        result_text.value = f"{name} 선택됨"
        search_click(None)
        page.update()

    # 검색 기능
    def search_click(e):
        result_view.controls.clear()
        results = book.search(search_input.value)

        if results:
            for name, info in sorted(results):
                is_selected = name == selected_name["value"]

                result_view.controls.append(
                    ft.Container(
                        width=250,
                        content=ft.Column([
                            ft.Text(name, weight="bold"),
                            ft.Text(info["phone"], size=12, color="#6B7280"),
                            ft.Text(f"{info['address']} · {info['job']}", size=11, color="#9CA3AF")
                        ]),
                        padding=15,
                        border_radius=14,
                        bgcolor="#E8F0FE" if is_selected else "white",
                        border=ft.border.all(2, "#4285F4") if is_selected else None,
                        shadow=ft.BoxShadow(
                            blur_radius=20,
                            color="#00000010",
                            offset=ft.Offset(0, 4)
                        ),
                        on_click=lambda e, n=name, i=info: fill_inputs(n, i)
                    )
                )
            result_text.value = f"{len(results)}명 검색됨"
        else:
            result_text.value = "결과 없음"

        page.update()

    # 등록
    def add_click(e):
        name = name_input.value
        if not name:
            result_text.value = "이름을 입력하세요"
            page.update()
            return

        book.add(name, phone_input.value, address_input.value, job_input.value)
        book.save_data()
        result_text.value = "등록 완료"
        search_click(None)
        page.update()

    # 수정
    def update_click(e):
        name = selected_name["value"] or name_input.value

        success = book.update_partial(
            name,
            phone_input.value,
            address_input.value,
            job_input.value
        )

        if success:
            book.save_data()

        result_text.value = "수정 완료" if success else "대상 없음"
        search_click(None)
        page.update()

    # 삭제
    def delete_click(e):
        name = selected_name["value"] or name_input.value

        success = book.delete(name)

        if success:
            book.save_data()

        result_text.value = "삭제 완료" if success else "대상 없음"
        search_click(None)
        page.update()

    # 버튼 생성 함수
    def main_button(text, color, on_click):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor=color,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=14
            ),
            expand=True
        )

    search_input.on_submit = search_click

    # UI 구성
    page.add(
        ft.Container(
            padding=30,
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Text("🗂️ 주소록", size=28, weight="bold"),

                    # 입력 영역
                    ft.Container(
                        padding=20,
                        border_radius=18,
                        bgcolor="white",
                        content=ft.Column([
                            ft.Text("✨ 개인정보 입력"),
                            ft.ResponsiveRow([
                                ft.Container(name_input, col=6),
                                ft.Container(phone_input, col=6),
                                ft.Container(address_input, col=6),
                                ft.Container(job_input, col=6),
                            ]),
                            ft.ResponsiveRow([
                                main_button("등록", "#428FE2", add_click),
                                main_button("수정", "#9CA3AF", update_click),
                                main_button("삭제", "#DF4C45", delete_click),
                            ])
                        ])
                    ),

                    # 검색 영역
                    ft.Container(
                        padding=20,
                        border_radius=18,
                        bgcolor="white",
                        content=ft.Column([
                            ft.Text("🧭 검색"),
                            ft.ResponsiveRow([
                                ft.Container(search_input, col=9),
                                ft.Container(main_button("검색", "#438EDF", search_click), col=3),
                            ]),
                        ])
                    ),

                    result_text,
                    result_view
                ]
            )
        )
    )


ft.app(target=main)
