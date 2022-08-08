import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori  # 연관분석 알고리즘
from pprint import pprint

dataset = [
    ["사과", "치즈", "생수"],
    ["생수", "호두", "치즈", "고등어"],
    ["수박", "사과", "생수"],
    ["생수", "호두", "치즈", "옥수수"]
]


# 데이터 전처리
# --------------------------------------
# 고등어 사과 생수 수박 옥수수 치즈 호두
#           T    T                T
# --------------------------------------
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df_ary = pd.DataFrame(te_ary, columns=te.columns_)
df = apriori(df_ary, use_colnames=True)
pprint(df)

# --------------------------------
# 결과
# --------------------------------
#    support      itemsets
# 0     0.50          (사과)
# 1     1.00          (생수)
# 2     0.75          (치즈)
# 3     0.50          (호두)
# 4     0.50      (생수, 사과)
# 5     0.75      (치즈, 생수)
# 6     0.50      (생수, 호두)
# 7     0.50      (치즈, 호두)
# 8     0.50  (치즈, 생수, 호두)
# --------------------------------
# support : 연관성 수치
#           표본 중 각 장바구니에서 itemsets를 집을 확률
#           이 값이 작을수록 itemsets의 item간 연관성이 낮다고 볼 수 있다.
