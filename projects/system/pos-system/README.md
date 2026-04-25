# 🛒 SmartCart POS System

> Python + Flet 기반 스마트 장바구니(POS) 프로그램  
> 장바구니, 재고 관리, 매출 관리 기능 구현

---

## 📌 Overview

SmartCart는 오프라인 매장의 POS 시스템을 간단하게 구현한 프로젝트입니다.  
상품을 장바구니에 담고 결제할 수 있으며, 재고 및 매출을 함께 관리할 수 있습니다.

👉 자세한 설계 및 개발 과정은 Notion에서 확인할 수 있습니다:  
https://www.notion.so/9-4-POS-34df07c99a8980cf94ecf40687c8a299?source=copy_link

---

## 🚀 Features

- 장바구니 추가 및 총 금액 계산
- 결제 및 영수증 출력
- 재고 관리 (부족 시 제한, 5개 이하 표시)
- 매출 관리 (주간 / 월간 / 연간)
- 관리자 상품 검색 기능
- 랜덤 할인 적용

---

## 🧠 Data Structure

- products : {상품명: {price, stock}}
- cart : {상품명: 수량}
- discount : {상품명: 할인율}

---

## 🔄 Workflow

상품 입력 → 장바구니 담기 → 결제 → 재고 감소 → 매출 저장

---

## 💾 Storage

- `sales_data.json`
- 최근 7일 매출 데이터 유지

---

## 🛠️ Tech Stack

- Python
- Flet
- JSON

---

## ⚙️ How to Run

