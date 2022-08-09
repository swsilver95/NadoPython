from pprint import pprint
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# pprint(df.to_string())

# 데이터 불러오기
df = pd.read_csv("./iris.csv")
label = df["variety"]
data = df[["sepal.length", "sepal.width", "petal.length", "petal.width"]]

# 데이터 학습시키기
# model = SVC()  # Support Vector Machine Classifier
# model.fit(data, label)
#
# # 예측시키기
# result = model.predict([
#     [5.2, 7.2, 4.0, 3.0],
#     [5.6, 6.4, 6.2, 2.5],
#     [3.0, 4.2, 5.5, 2.2]
# ])
#
# print(result)


# 분할 검증 모델 실행
train_data, valid_data, train_label, valid_label = train_test_split(data, label)

# 학습시키기
model = SVC()  # Support Vector Machine Classifier
model.fit(train_data, train_label)

# 예측시키기
result = model.predict(valid_data)
# print(result)

# 정확도 확인하기
score = accuracy_score(result, valid_label)
print(f"정확도 : {score*100:.2f}%")
