from flask import Flask, jsonify, request,redirect,url_for,render_template
import openai

app = Flask(__name__)

# 设置 OpenAI API 密钥和模型 ID
openai.api_key = "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"
model = "text-davinci-002"

# 十个占卜类别
categories = [
    "爱情",
    "职业",
    "健康",
    "财务",
    "家庭",
    "友谊",
    "旅游",
    "教育",
    "精神",
    "个人发展",
]


# 定义 GPT 模型生成文本的函数
def generate_text(prompt):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()


# 定义占卜模型，输入一个问题、自述和占卜类别，输出占卜结果
def predict(category, question, description):
    # 使用 GPT 模型生成占卜结果
    prompt = f"以 {category} 为背景，回答以下问题：{question}。以下是您的自述：{description}。"
    prediction = generate_text(prompt)

    # 解析占卜结果，返回仅包含占卜结果的部分
    prediction = prediction.split("\n")[-1].split("。")[0].strip()

    return prediction
@app.route("/", methods=["GET", "POST"])
def index():
    # 如果是 POST 请求，则从表单中获取用户输入并重定向到占卜结果页面
    if request.method == "POST":
        category = request.form.get("category")
        return redirect(url_for("prediction", category=category))

    # 如果是 GET 请求，则渲染 HTML 模板
    return render_template("index.html", categories=categories)

@app.route("/predict", methods=["POST"])
def handle_prediction():
    # 解析 POST 请求的数据
    data = request.get_json()
    category = data.get("category")
    question = data.get("question")
    description = data.get("description")

    # 进行占卜
    prediction = predict(category, question, description)

    # 返回占卜结果
    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    app.run(debug=True)
