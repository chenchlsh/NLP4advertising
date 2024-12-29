import torch
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(torch.__version__)

import json

# 加载 JSON 文件
with open('qa_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)


# JSON 数据结构如下：
# [
#   {"question": "问题1", "answer": "答案1"},
#   {"question": "问题2", "answer": "答案2"}
# ]

questions = [item['question'] for item in dataset]
answers = [item['answer'] for item in dataset]


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 加载预训练模型和分词器
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

# 将问题和答案进行编码
inputs = tokenizer(questions, padding=True, truncation=True, return_tensors="pt")
labels = tokenizer(answers, padding=True, truncation=True, return_tensors="pt")

# 查看编码结果
print("Inputs:", inputs)
print("Labels:", labels)

from transformers import Trainer, TrainingArguments

# 定义训练参数
training_args = TrainingArguments(
    output_dir="./results",          # 输出目录
    evaluation_strategy="epoch",     # 评估策略
    remove_unused_columns=False,     # 保留数据集中的所有列
    num_train_epochs=3,              # 训练的轮数
    per_device_train_batch_size=8,   # 每个设备上的批量大小
    save_steps=10,                   # 每隔多少步保存一次模型
    save_total_limit=2,              # 最多保存多少个检查点
)

# 将数据整理为数据集格式
from datasets import Dataset
data = {"input_text": questions, "output_text": answers}
dataset = Dataset.from_dict(data)

# 定义训练器
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# 开始训练
trainer.train()

# 输入一个问题进行测试
question = "高考如何选择志愿？"
input_ids = tokenizer.encode(question, return_tensors="pt")

# 生成答案
outputs = model.generate(input_ids)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Generated Answer:", answer)

# 训练完成后保存模型
import os

# 保存路径
save_path = "/Users/chenchlsh/project1/saved model"
os.makedirs(save_path, exist_ok=True)

# 保存模型和分词器
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"Model and tokenizer saved to {save_path}")
