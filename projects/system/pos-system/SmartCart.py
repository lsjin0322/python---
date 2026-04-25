"""
SmartCart POS System
- 장바구니 / 재고 / 매출 관리 프로그램
- JSON 파일 기반 주간 매출 저장
"""

import flet as ft
import random
from datetime import datetime
import json
import os

DATA_FILE = "sales_data.json"

items = [
 "비누","치약","샴푸","린스","바디워시","폼클렌징","칫솔","수건",
 "휴지","물티슈","세탁세제","섬유유연제","주방세제","수세미","고무장갑",
 "쌀","라면","햇반","생수","우유","계란","두부","콩나물","시금치",
 "양파","감자","고구마","사과","바나나","오렌지","귤","토마토",
 "김치","된장","고추장","간장","식용유","참기름","소금","설탕",
 "커피","차","과자","빵","젤리","초콜릿","음료수","맥주","소주",
 "고기(돼지고기)","고기(소고기)","닭고기","생선","오징어","새우","게",
 "쌀국수","파스타","잼","버터","치즈","요거트","아이스크림","통조림",
 "냉동만두","어묵","햄","소시지","김","미역","다시마","멸치",
 "밀가루","부침가루","튀김가루","빵가루","식초","소스","향신료",
 "양초","성냥","건전지","전구","쓰레기봉투","지퍼백","호일","랩"
]

# POS 시스템 핵심 로직 (상품, 장바구니, 매출 관리)
class SmartCart:

    # 상품 초기화 및 할인 상품 랜덤 설정
    def __init__(self):
        self.products = {i: {"price": random.randint(1000,8000), "stock": random.randint(5,20)} for i in items}
        self.cart = {}
        self.monthly = 0
        self.yearly = 0

        discount_items = random.sample(items, 5)
        self.discount = {i: random.randint(10,50) for i in discount_items}

    # 할인 적용된 가격 반환
    def price(self, n):
        p = self.products[n]["price"]
        if n in self.discount:
            p -= p * self.discount[n] / 100
        return int(p)

    # 장바구니 총 금액 계산
    def total(self):
        return sum(self.price(n)*q for n,q in self.cart.items())

    # 신규 상품 등록 또는 재고 추가
    def register(self, n, q):
        if n not in self.products:
            self.products[n] = {"price": random.randint(1000,8000), "stock": q}
            return f"{n} 신규 등록 완료"
        else:
            self.products[n]["stock"] += q
            return f"{n} 재고 {q}개 추가됨"

    # 장바구니 담기 (재고 체크 포함)
    def add(self, n, q):
        if n not in self.products:
            return "상품 없음 (등록 먼저)"
        if self.products[n]["stock"] < q:
            return "재고 부족"
        self.cart[n] = self.cart.get(n,0) + q
        return "담기 완료"

    # 결제 처리 및 재고 차감
    def pay(self):
        t = self.total()
        for n,q in self.cart.items():
            self.products[n]["stock"] -= q
        self.monthly += t
        self.yearly += t
        return t


# 매출 데이터를 JSON 파일에 저장 (최근 7일 유지)
def save_sales(amount):
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    data.append({"date": today, "amount": amount})

    new_data = []
    for d in data:
        diff = (datetime.now() - datetime.strptime(d["date"], "%Y-%m-%d")).days
        if diff <= 7:
            new_data.append(d)

    with open(DATA_FILE, "w") as f:
        json.dump(new_data, f)


# 최근 7일 매출 합계 반환
def load_weekly():
    if not os.path.exists(DATA_FILE):
        return 0

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    return sum(d["amount"] for d in data)


# Flet UI 구성 및 이벤트 처리
def main(page: ft.Page):

    cart_sys = SmartCart()

    PRIMARY = "#4CAF50"
    ACCENT = "#81C784"
    BG = "#FAFAFA"
    BROWN = "#2E7D32"

    page.title = "[Bio SmartCart]"
    page.bgcolor = BG
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    item_input = ft.TextField(label="상품명", expand=True, border_color=PRIMARY, border_radius=12, bgcolor="white")
    qty_input = ft.TextField(label="수량", expand=True, border_color=PRIMARY, border_radius=12, bgcolor="white")
    admin_search = ft.TextField(label="관리자 검색", expand=True, border_color=PRIMARY, border_radius=12, bgcolor="white")

    cart_view = ft.Column()
    receipt_view = ft.Column()
    admin_view = ft.Column()
    low_stock_view = ft.Column()

    sales_text = ft.Text(color=PRIMARY)
    error_text = ft.Text(color="red")
    total_text = ft.Text("총합: 0원", size=18, color=BROWN)

    # 장바구니 UI 갱신
    def update():
        cart_view.controls.clear()
        for n,q in cart_sys.cart.items():
            cart_view.controls.append(
                ft.Text(f"{n} x{q} = {cart_sys.price(n)*q}원", color=BROWN)
            )
        total_text.value = f"총합: {cart_sys.total()}원"
        page.update()

    # 상품 등록 버튼 이벤트
    def register(e):
        try:
            q = int(qty_input.value)
        except:
            error_text.value = "수량 오류"
            page.update()
            return

        error_text.value = cart_sys.register(item_input.value.strip(), q)
        update_low_stock()
        page.update()

    # 장바구니 추가 이벤트
    def add(e):
        try:
            q = int(qty_input.value)
        except:
            error_text.value = "잘못 입력"
            page.update()
            return

        error_text.value = cart_sys.add(item_input.value.strip(), q)
        update()

    # 결제 버튼 이벤트
    def pay(e):
        if not cart_sys.cart:
            error_text.value = "장바구니 비어있음"
            page.update()
            return

        t = cart_sys.pay()
        save_sales(t)
        ask_receipt(t)

    # 영수증 출력 여부 선택
    def ask_receipt(t):
        receipt_view.controls.clear()
        receipt_view.controls.append(ft.Text("영수증을 드릴까요?"))

        def yes(e):
            show_receipt(t)

        def no(e):
            cart_sys.cart.clear()
            receipt_view.controls.clear()
            update()
            update_sales()
            page.update()

        receipt_view.controls.append(
            ft.Row([
                ft.ElevatedButton("네", bgcolor=PRIMARY, color="white", on_click=yes),
                ft.ElevatedButton("아니오", bgcolor=ACCENT, color="white", on_click=no)
            ])
        )
        page.update()

    # 영수증 UI 출력
    def show_receipt(t):
        receipt_view.controls.clear()

        receipt_view.controls.append(ft.Text("===== 영수증 =====", size=18, color=PRIMARY))

        for n,q in cart_sys.cart.items():
            receipt_view.controls.append(
                ft.Text(f"{n} x{q} = {cart_sys.price(n)*q}원")
            )

        receipt_view.controls.append(ft.Text("----------------"))
        receipt_view.controls.append(ft.Text(f"총합: {t}원"))
        receipt_view.controls.append(ft.Text("================"))

        def close(e):
            cart_sys.cart.clear()
            receipt_view.controls.clear()
            update()
            update_sales()
            update_low_stock()
            page.update()

        receipt_view.controls.append(
            ft.ElevatedButton("닫기", bgcolor=PRIMARY, color="white", on_click=close)
        )

        page.update()

    # 상품 검색 (재고 / 가격 확인)
    def update_admin(e=None):
        admin_view.controls.clear()
        key = admin_search.value.strip()

        if not key:
            admin_view.controls.append(ft.Text("검색 후 표시됩니다", color="gray"))
            page.update()
            return

        for n,v in cart_sys.products.items():
            if key in n:
                admin_view.controls.append(
                    ft.Text(f"{n} | 재고:{v['stock']} | {v['price']}원", color=BROWN)
                )
        page.update()

    # 매출 정보 UI 갱신
    def update_sales():
        weekly = load_weekly()
        sales_text.value = f"주간매출: {weekly}원 / 월매출: {cart_sys.monthly}원 / 연매출: {cart_sys.yearly}원"
        page.update()

    # 재고 5개 이하 상품 표시
    def update_low_stock():
        low_stock_view.controls.clear()
        for n,v in cart_sys.products.items():
            if v["stock"] <= 5:
                low_stock_view.controls.append(
                    ft.Text(f"⚠️ {n} → 재고 {v['stock']}개", color="#D32F2F")
                )
        page.update()

    discount_box = ft.Container(
        padding=12,
        bgcolor="#F1F8E9",
        border_radius=12
    )

    # 할인 상품 UI 업데이트
    def update_discount():
        col = ft.Column()
        col.controls.append(ft.Text("📢 할인 정보", color=PRIMARY, size=16))
        for n,r in cart_sys.discount.items():
            col.controls.append(ft.Text(f"{n} - {r}%", color=ACCENT))
        discount_box.content = col

    register_btn = ft.ElevatedButton("등록", bgcolor="#388E3C", color="white", on_click=register)
    add_btn = ft.ElevatedButton("담기", bgcolor=PRIMARY, color="white", on_click=add)
    pay_btn = ft.ElevatedButton("결제", bgcolor=ACCENT, color="white", on_click=pay)

    page.add(
        ft.Container(
            width=800,
            padding=25,
            bgcolor="white",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=15, color="#dddddd"),
            content=ft.Column(
                [
                    ft.Text("🌿 Bio SmartCart", size=26, weight="bold", color=PRIMARY),
                    ft.Text(f"📅 {datetime.now().strftime('%Y.%m.%d')}", color=BROWN),

                    ft.Divider(),

                    ft.Row([
                        ft.Container(
                            expand=2,
                            content=ft.Column([
                                ft.Text("🔎 상품 입력", color=PRIMARY),
                                item_input,
                                qty_input,
                                ft.Row([register_btn, add_btn, pay_btn])
                            ])
                        ),
                        ft.Container(expand=1, content=discount_box)
                    ], spacing=20),

                    error_text,

                    ft.Divider(),

                    ft.Text("🛒 장바구니", color=PRIMARY),
                    cart_view,
                    total_text,

                    ft.Divider(),

                    ft.Text("🧾 영수증", color=PRIMARY),
                    receipt_view,

                    ft.Divider(),

                    ft.Text("👨‍💼 관리자", color=PRIMARY),
                    admin_search,
                    ft.ElevatedButton("검색", on_click=update_admin, bgcolor=PRIMARY, color="white"),
                    admin_view,

                    ft.Divider(),

                    ft.Text("⚠️ 재고 부족 상품", color=PRIMARY),
                    low_stock_view,

                    ft.Divider(),

                    sales_text
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            )
        )
    )

    update_discount()
    update()
    update_sales()
    update_low_stock()


# 앱 실행
ft.app(target=main)
