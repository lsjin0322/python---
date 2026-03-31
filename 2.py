# 1
# src/chapter2/01_basic_window.py
import tkinter as tk

# 1단계: 기본 창 만들기 
root = tk.Tk() # 새로운 창을 만듭니다
root.title('내 첫번째 GUI 프로그램') # 창 제목 설정
root.geometry("300x200") # 창 크기 설정 (가로x세로)

# 2단계: 창 보여주기 (창을 띄우기 위해 필수)
root.mainloop()

# 2
# src/chapter2/01_basic_window.py
import tkinter as tk

root = tk.Tk()

# 창 설정 옵션들
# 제목
root.title("창 설정 연습")
# 크기
root.geometry("300x200")
# 가로만 크기 조절 가능
root.resizable(True,False)         
# 최소 크기
root.minsize(200, 100)
# 최대 크기
root.maxsize(800,600)
# 배경색
root.configure(bg="lightblue")

root.mainloop()

# 3
import tkinter as tk

root = tk.Tk()
root.title("Label 연습")
root.geometry("500x400")
root.configure(bg="white")

# 기본 라벨
basic_label = tk.Label(root, text="안녕하세요! 이것은 기본 라벨입니다.")
basic_label.pack(pady=10)

# 스타일이 적용된 라벨
styled_label = tk.Label(
    root,
    text="예쁘게 꾸민 라벨",
    font=("맑은 고딕",16, "bold"),     # 폰트 설정
    fg="blue",                                    # 글자색
    bg="lightyellow",                        # 배경색
    width=20,                                    # 너비 (글자 수)
    height=2                                      # 높이 (줄 수)
)
styled_label.pack(pady=10)

# 여러 줄 라벨
multiline_label = tk.Label(
    root,
    text="여러 줄로 된 라벨입니다./n두 번째 줄 /n세 번째 줄",
    font=("맑은 고딕", 12),
    justify=tk.LEFT,                               # 텍스트 정렬
    bg="lightgreen"
)
multiline_label.pack(pady=10)

# 동적으로 변하는 라벨
dynamic_var = tk.StringVar()
dynamic_var.set("변경 가능한 텍스트")

dynamic_label = tk.Label(
    root,
    textvariable=dynamic_var,           # StringVar 사용
    font=("맑은 고딕", 14),
    fg="red"
)
dynamic_label.pack(pady=10)

# 텍스트를 변경하는 버튼
def change_text():
    import random
    texts = ["안녕하세요!", "Hello!", "Bonjour!", "Hallo!"]
    dynamic_var.set(random.choice(texts))

change_button = tk.Button(root, text="텍스트 변경", command=change_text)
change_button.pack(pady=10)

root.mainloop()

# 4
import tkinter as tk

root = tk.Tk()
root.title("Entry 기본 사용법")
root.geometry("400x200")

# 기본 입력창 
tk.Label(root, text="이름을 입력하세요:", font=("맑은 고딕",12)).pack(pady=10)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

# 입력값 가져오기 
def show_input() :
    user_input = name_entry.get()    # Entry에서 텍스트 가져오기 
    result_label.config(text=f"입력하신 내용: {user_input}")

tk.Button(root, text="입력값 확인", command=show_input).pack(pady=10)

result_label = tk.Label(root, text="", font=("맑은 고딕", 11), fg="blue")
result_label.pack()

root.mainloop()


# 5
import tkinter as tk

root = tk.Tk()
root.title("Entry 다양한 스타일")
root.geometry("500x300")

# 일반 텍스트 입력창
tk.Label(root, text="이름:", font=("맑은 고딕", 12)).pack(pady=5)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

# 비밀번호 입력창 (별도로 숨김)
tk.Label(root, text="비밀번호:", font=("맑은 고딕", 12)).pack(pady=5)
password_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30, show="*")
password_entry.pack(pady=5)

# 읽기 전용 입력창 
tk.Label(root,text="읽기 전용:", font=("맑은 고딕", 12)).pack(pady=5)
readonly_entry = tk.Entry(root, font=("맑은 고딕", 12),width=30, state="readonly")
readonly_entry.insert(0, "이 텍스트는 수정할 수 없습니다.")
readonly_entry.pack(pady=5)

root.mainloop()

# 6
import tkinter as tk
import tkinter.messagebox as msgbox

root = tk.Tk()
root.title("Entry 입력값 검증")
root.geometry("500x400")

# 입력 필드들
tk.Label(root, text="이름:", font=("맑은 고딕", 12)).pack(pady=5)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

tk.Label(root, text="나이 (숫자만):", font=("맑은 고딕", 12)).pack(pady=5)
age_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
age_entry.pack(pady=5)

# 입력값 처리 함수 
def process_input():
    name = name_entry.get()
    age = age_entry.get()

    # 입력값 검증
    if not name:
        msgbox.showwarning("입력 오류", "이름을 입력해주세요!")
        return
    
    if age and not age.isdigit():
        msgbox.showerror("입력 오류", "나이는 숫자만 입력해주세요!")
        return
    
    # 결과 표시 
    result = f"안녕하세요, {name}님!"
    if age:
        result += f"\n나이: {age}세"
        msgbox.showinfo("입력 결과", result)

# 버튼과 기능
tk.Button(root, text="입력 처리", command=process_input,
              font=("맑은 고딕", 12), bg="lightgreen").pack(pady=10)

def clear_all(): 
    name_entry.delete(0, tk.END)  # Entry 내용 지우기 
    age_entry.delete(0, tk.END)

tk.Button(root, text="모두 지우기", command=clear_all,
          font=("맑은 고딕", 12), bg="lightcoral").pack(pady=5)

# Enter 키로 입력처리 
root.bind('<Return>', lambda event: process_input())

root.mainloop()

# 7
import tkinter as tk

root = tk.Tk()
root.title("Text 기본 사용법")
root.geometry("500x300")

tk.Label(root, text=" 여러 줄 텍스트 입력:", font=("맑은 고딕", 12,"bold")).pack(pady=5)

# 기본 Text 위젯
text_widget = tk.Text(
    root,
    height=10,
    width=50,
    font=("맑은 고딕", 11),
    wrap=tk.WORD,                          # 단어 단위로 줄바꿈
    bg="lightyellow"   
)
text_widget.pack(pady=10)

# 초기 텍스트 넣기 
text_widget.insert(tk.END, "여기에 여러 줄의 텍스를 입력할 수 있습니다.\n")
text_widget.insert(tk.END, "Enter를 눌러서 줄을 바꿀 수 있습니다.\n")
text_widget.insert(tk.END, "Text 위젯은 긴 문서 작성에 적합합니다. ")


root.mainloop()