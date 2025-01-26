import json
from difflib import SequenceMatcher

# 加载问题库
def load_dataset(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

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

    # 设置匹配阈值，避免误匹配
    if highest_score > 0.6:  # 0.6 是相似度阈值，可根据实际需求调整
        return best_match, highest_score
    else:
        return None, highest_score

# 主程序
def main():
    # 加载问题库
    dataset = load_dataset("qa_dataset.json")

    print("欢迎使用本地问答系统！输入您的问题，输入 'exit' 退出程序。")
    while True:
        user_question = input("\n请输入您的问题: ")
        if user_question.lower() == "exit":
            print("感谢使用，再见！")
            break

        # 查找最佳匹配问题
        best_match, score = find_best_match(user_question, dataset)
        if best_match:
            print(f"\n最相似的问题: {best_match['question']}")
            print(f"答案: {best_match['answer']}")
            print(f"(匹配度: {score:.2f})")
        else:
            print("抱歉，没有找到相关答案，请尝试其他问题。")

if __name__ == "__main__":
    main()