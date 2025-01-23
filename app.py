from flask import Flask, request, jsonify
from transformers import pipeline
import json

app = Flask(__name__)

# 加载预训练模型（这里使用 transformers 提供的模型）
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# 加载问题集（context）
with open('qa_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# 定义 API 路由
@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    question = data.get('question', '')

    # 将所有 context 合并为一个大文本（简单实现）
    context = " ".join([item['answer'] for item in dataset])

    # 使用模型回答问题
    result = qa_pipeline(question=question, context=context)

    return jsonify({"question": question, "answer": result['answer']})


if __name__ == '__main__':
    app.run(port=5000)