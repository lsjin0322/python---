# 8
import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("스크롤 가능한 Text")
root.geometry("500x400")

tk.Label(root, text="스크롤 가능한 텍스트: ", font=("맑은 고딕", 12, "bold")).pack(pady=5)

# 스크롤바가 있는 Text 위젯
text_area = scrolledtext.ScrolledText(
    root,
    height=15,
    width=60,
    font=("맑은 고딕", 11),
    wrap=tk.WORD
)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)



# 많은 양의 텍스트 추가 
for i in range(100):
     text_area.insert( tk.END, f"이것은 {i+1}번째 줄입니다.스크롤해서 아래 내용을 확인해보세요!\n")
                      
root.mainloop()

# 9
import tkinter as tk

root = tk.Tk()
root.title("Text 조작 기능")
root.geometry("600x400")

# Text 위젯
text_widget = tk.Text(root, height=15, width=60, font=("맑은 고딕", 11))
text_widget.pack(padx=10, pady=10)

# 초기 텍스트 
text_widget.insert(tk.END, "이 텍스트를 편집해보세요.\n선택하고 복사, 붙여넣기, 삭제 등의 기능을 사용할 수 있습니다.")

# 버튼 프레임
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

def get_text():
     content = text_widget.get(1.0, tk.END)
     print("전체 텍스트: ",content)
def clear_text():
     text_widget.delete(1.0, tk.END)

def insert_text():
     text_widget.insert(tk.END, "\n새로운 텍스트가 추가되었습니다.")

tk.Button(button_frame, text="텍스트 가져오기", command=get_text).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="모두 지우기", command=insert_text).pack(side=tk.LEFT, padx=5)

root.mainloop()