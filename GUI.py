import json
from difflib import SequenceMatcher
import tkinter as tk
from tkinter import messagebox

# 加载问题库
def load_dataset(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到问题库文件！请检查文件路径。")
        return []

# NLP 模糊匹配算法
def find_best_match(user_question, dataset):
    best_match = None
    highest_score = 0

    for item in dataset:
        question = item["question"]
        # 使用 SequenceMatcher 计算相似度
        score = SequenceMatcher(None, user_question, question).ratio()
        if score > highest_score:
            highest_score = score
            best_match = item

    return best_match, highest_score

# 提交问题处理
def ask_question():
    user_question = entry.get().strip()
    if not user_question:
        messagebox.showwarning("提示", "请输入一个问题！")
        return

    best_match, score = find_best_match(user_question, dataset)
    if best_match and score > 0.6:
        result.set(f"最相似的问题: {best_match['question']}\n\n答案: {best_match['answer']}\n\n匹配度: {score:.2f}")
    else:
        result.set("抱歉，没有找到相关答案。")

# 创建主窗口
root = tk.Tk()
root.title("本地问答系统")
root.geometry("500x400")

# 加载问题库
dataset = load_dataset("qa_dataset.json")

# 创建界面布局
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="请输入您的问题:", font=("Arial", 14))
label.pack()

entry = tk.Entry(frame, width=50, font=("Arial", 12))
entry.pack(pady=10)

btn = tk.Button(frame, text="提交问题", command=ask_question, font=("Arial", 12))
btn.pack(pady=5)

result = tk.StringVar()
result_label = tk.Label(frame, textvariable=result, wraplength=450, justify="left", font=("Arial", 12), fg="blue")
result_label.pack(pady=10)

# 运行主循环
root.mainloop()

def save_result():
    if not result.get():
        messagebox.showwarning("提示", "没有内容可保存！")
        return
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(result.get())
    messagebox.showinfo("成功", "结果已保存为 result.txt")

# 添加保存按钮
save_btn = tk.Button(frame, text="保存结果", command=save_result, font=("Arial", 12))
save_btn.pack(pady=5)