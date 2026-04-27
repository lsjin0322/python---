# 🗂️ Address Book System

> Python + Flet 기반 주소록 관리 프로그램

---

## 📌 Overview

이름을 기준으로 전화번호, 주소, 직업 정보를 관리하는 주소록 프로그램입니다.  
검색, 수정, 삭제 기능과 함께 JSON 파일을 활용한 데이터 저장 기능을 제공합니다.

---
<img width="330" height="438" alt="image" src="https://github.com/user-attachments/assets/1d0b7efb-b2e7-4522-b137-11ff623e2be3" />


---

## 🚀 Features

- 연락처 등록 / 수정 / 삭제
- 이름 및 전화번호 검색 기능
- 카드 형태 UI + 클릭 시 자동 입력
- JSON 기반 데이터 영구 저장
- 프로그램 재실행 시 데이터 유지

---

## 🧠 Data Structure

- {이름: {phone, address, job}}

---

## 🔄 Workflow

검색 → 선택 → 입력창 자동 채움 → 수정/삭제 → 저장

---

## 💾 Storage

- address.json 파일 사용

---

## ⚙️ How to Run

```bash
pip install flet
python main.py
