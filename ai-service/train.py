import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

print("开始训练模型...")

# 1. 加载数据
# 使用 encoding='ISO-8859-1' 来避免编码错误
data = pd.read_csv('IMDB Dataset.csv', encoding='ISO-8859-1')
print("数据加载完毕。")

# 为了快速训练，我们可以只用一部分数据
# 如果你的电脑性能好，可以把下面这行注释掉，使用全部5万条数据
data = data.sample(n=10000, random_state=42)

# 2. 数据预处理
# 将 sentiment 列的 'positive' 和 'negative' 转换成 1 和 0
data['sentiment'] = data['sentiment'].apply(lambda x: 1 if x == 'positive' else 0)
X = data['review']
y = data['sentiment']
print("数据预处理完毕。")

# 3. 特征工程：将文本转换为TF-IDF向量
# TF-IDF是一种将文本转换为数字向量的常用方法，模型只能理解数字
vectorizer = TfidfVectorizer(max_features=5000) # 只取最重要的5000个词
X_vectorized = vectorizer.fit_transform(X)
print("文本向量化完毕。")

# 4. 训练模型
model = LogisticRegression()
model.fit(X_vectorized, y)
print("模型训练完毕。")

# 5. 保存模型和向量化工具
# 这一步至关重要！我们必须保存vectorizer，因为预测时需要用同样的方式转换新文本
joblib.dump(model, 'sentiment_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("模型和向量化工具已保存！训练脚本执行完毕。")