const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const natural = require("natural"); // NLP 库

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件配置
app.use(cors());
app.use(bodyParser.json());

// 示例数据库（用于回答高考相关问题）
const database = {
  "XX大学录取分数线": "XX大学在2023年的录取分数线是500分。",
  "某专业就业率": "某专业的就业率高达95%。",
  "XX大学学费": "XX大学的年学费为15000元。",
  "某专业课程": "该专业的主要课程包括数学、物理和编程。",
};

// 初始化自然语言处理（NLP）工具
const tokenizer = new natural.WordTokenizer();
const JaroWinklerDistance = natural.JaroWinklerDistance; // 用于模糊匹配的算法

// 简单的意图分类
function classifyIntent(question) {
  if (question.includes("分数线") || question.includes("多少分")) {
    return "录取分数线";
  } else if (question.includes("就业率") || question.includes("毕业生")) {
    return "就业率";
  } else if (question.includes("学费") || question.includes("费用")) {
    return "学费";
  } else if (question.includes("课程") || question.includes("专业")) {
    return "课程";
  } else {
    return null;
  }
}

// 简单的模糊匹配算法，返回匹配度最高的答案
function findBestMatch(question) {
  const keys = Object.keys(database);
  const matches = keys.map((key) => ({
    key,
    score: JaroWinklerDistance(key, question), // 计算相似度
  }));
  matches.sort((a, b) => b.score - a.score); // 按照匹配度排序
  return matches[0].score > 0.7 ? matches[0].key : null; // 匹配度大于 0.7 才算有效
}

// 处理用户问题并返回答案
app.post("/api/ask", (req, res) => {
  const { question } = req.body;

  if (!question || question.trim() === "") {
    return res.status(400).json({ answer: "问题不能为空，请重新输入。" });
  }

  // 1. 进行意图分类
  const intent = classifyIntent(question);

  // 2. 如果能识别出意图，进行相应的回答
  if (intent) {
    // 基于意图进行回答
    switch (intent) {
      case "录取分数线":
        return res.json({ answer: database["XX大学录取分数线"] });
      case "就业率":
        return res.json({ answer: database["某专业就业率"] });
      case "学费":
        return res.json({ answer: database["XX大学学费"] });
      case "课程":
        return res.json({ answer: database["某专业课程"] });
      default:
        return res.json({ answer: "对不起，无法识别该问题。" });
    }
  } else {
    // 3. 如果没有识别到意图，尝试模糊匹配问题
    const bestMatch = findBestMatch(question);
    if (bestMatch) {
      res.json({ answer: database[bestMatch] });
    } else {
      res.json({ answer: "很抱歉，未能找到相关答案。" });
    }
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器正在运行：http://localhost:${PORT}`);
});
