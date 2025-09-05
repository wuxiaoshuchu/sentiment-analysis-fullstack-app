from flask import Flask, request, jsonify
import joblib

# 1. 初始化Flask App
app = Flask(__name__)

# 2. 在App启动时，预先加载模型和向量化工具
# 这样可以避免每次请求都重新加载，提高效率
print("正在加载模型...")
model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
print("模型加载完毕。")

# 3. 定义API的路由和处理函数
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    # 检查请求中是否包含JSON数据
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400

    # 获取JSON数据
    data = request.get_json()
    text_to_analyze = data.get('text', '')

    if not text_to_analyze:
        return jsonify({"error": "JSON中缺少'text'字段"}), 400

    # 使用加载好的vectorizer转换文本
    vectorized_text = vectorizer.transform([text_to_analyze])

    # 使用加载好的model进行预测
    prediction = model.predict(vectorized_text)

    # 将预测结果（0或1）转换为人类可读的标签
    sentiment = 'Positive' if prediction[0] == 1 else 'Negative'

    # 返回JSON格式的响应
    return jsonify({"sentiment": sentiment})

# 4. 启动Flask App
if __name__ == '__main__':
    # debug=True 模式可以在你修改代码后自动重启服务，方便开发
    app.run(host='0.0.0.0', port=5000, debug=True)