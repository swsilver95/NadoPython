from sklearn.datasets import load_iris
import streamlit as st
from sklearn.svm import SVC

iris = load_iris()
data = iris["data"]
label = iris["target"]

model = SVC()
model.fit(data, label)

st.write("# 붓꽃 품종 예측")

st.sidebar.title("Features")
value1 = st.sidebar.slider(label="Sepal length (cm)", min_value=0.0, max_value=8.0, value=5.2)
value2 = st.sidebar.slider(label="Sepal width (cm)", min_value=0.0, max_value=8.0, value=3.2)
value3 = st.sidebar.slider(label="Petal length (cm)", min_value=0.0, max_value=8.0, value=4.2)
value4 = st.sidebar.slider(label="Petal width (cm)", min_value=0.0, max_value=8.0, value=1.2)
if st.sidebar.button("품종 예측!"):
    result = model.predict([[value1, value2, value3, value4]])
    if result == 0:
        st.image("https://upload.wikimedia.org/wikipedia/commons/a/a7/Irissetosa1.jpg")
        st.write("# Setosa")
    elif result == 1:
        st.image("https://daylily-phlox.eu/wp-content/uploads/2016/08/Iris-versicolor-1.jpg")
        st.write("# Versicolor")
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Iris_virginica_2.jpg/1200px-Iris_virginica_2.jpg")
        st.write("# Verginica")
