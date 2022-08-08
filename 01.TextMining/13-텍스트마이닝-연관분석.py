# 크롤링
import os
import webbrowser
from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par

# 단어분석
from konlpy.tag import Okt

# 연관분석 import
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori  # 연관분석 알고리즘
from pprint import pprint

# 시각화
import networkx as nx
from pyvis.network import Network

keyword = input("키워드 입력 >> ")
encoded = par.quote(keyword)  # 한글 -> 특수한 문자

page_num = 1
dataset = []
okt = Okt()
while page_num <= 2:
    url = f"https://www.joongang.co.kr/_CP/496?keyword={encoded}&sort%20=&pageItemId=439&page={page_num}"
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline a")
    if len(title) == 0:  # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        title_text = i.text.strip()
        print("제목 :", title_text)
        nouns_list = okt.nouns(title_text)
        tmp = nouns_list[:]
        for j in tmp:
            if len(j) == 1:
                nouns_list.remove(j)
        dataset.append(nouns_list)

    page_num += 1


# 연관분석 시작
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df_ary = pd.DataFrame(te_ary, columns=te.columns_)

# apriori는 support 값이 기본으로 0.5 이상인 것만 출력되게 되어 있음
# min_support 속성을 이용해 최소 속성값 재정의
df = apriori(df_ary, use_colnames=True, min_support=0.02)

# itemsets의 원소가 2개인 데이터만 분류
df["length"] = df["itemsets"].str.len()
df = df[df["length"] == 2]

# 새로운 열 추가 source, target
df["itemsets"] = df["itemsets"].apply(lambda x: list(x))
df["item1"] = df["itemsets"].str[0]
df["item2"] = df["itemsets"].str[1]
pprint(df)

# ------------------------------------
# 시각화 시작
# source: 대상단어
# target: 연관단어
# support: 연관성
G = nx.from_pandas_edgelist(df, source="item1", target="item2", edge_attr="support")
net = Network(height="700px", width="1050px")
net.from_nx(G)
net.show_buttons(filter_=["nodes", "edges", "physics"])
net.show("./network.html")
ap = os.path.abspath("./network.html")
webbrowser.open(ap)
