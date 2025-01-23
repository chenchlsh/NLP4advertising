import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 加载已保存的模型和分词器
model_path = "/Users/chenchlsh/project1/saved model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# 获取用户输入的问题
question = sys.argv[1]

# 编码输入并生成答案
input_ids = tokenizer.encode(question, return_tensors="pt")
outputs = model.generate(input_ids)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

# 打印答案（供 Node.js 使用）
print(answer)