from bs4 import BeautifulSoup
import urllib.request as req
import sentiment_module
from pyecharts import Bar3D, Pie
import webbrowser
import os

print("========= 영화 감성 분석 프로그램 ============")
code = req.urlopen("https://movie.naver.com/movie/sdb/rank/rmovie.naver")
soup = BeautifulSoup(code, "html.parser")
title = soup.select("div.tit3 > a")[:10]
print("<< 현재 상영중인 영화 순위 >>")
num = 1
for i in title:
    print(f"({num}) {i.text}")
    num += 1
print("========================================")
menu = int(input("감성 분석 진행할 영화 선택 >> "))
print("========================================")
print(f"[알림] <{title[menu-1].text}> 영화의 리뷰에 대해 감성 분석을 실시합니다.")
print("========================================")
selected_movie = title[menu-1]
movie_code = selected_movie.attrs["href"].replace("/movie/bi/mi/basic.naver?code=", "")

page_num = 1
sentiment_result = {
    "매우 긍정": 0,
    "긍정": 0,
    "중립": 0,
    "부정": 0,
    "매우 부정": 0,
}
while True:
    url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page_num}"
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    comment = soup.select("div.score_reple > p > span:nth-child(2)")
    for i in comment:
        user_review = i.text.strip()
        if user_review == "스포일러가 포함된 감상평입니다. 감상평 보기":
            continue
        if user_review == "":
            continue
        print(user_review)
        score = sentiment_module.sentiment_predict(user_review)
        if score >= 0.5:
            print(f"{score * 100:.2f}% 확률로 긍정입니다.")
        else:
            print(f"{100 - score * 100:.2f}% 확률로 부정입니다.")

        # Count
        if score >= 0.8:
            sentiment_result["매우 긍정"] += 1
        elif score >= 0.6:
            sentiment_result["긍정"] += 1
        elif score >= 0.4:
            sentiment_result["중립"] += 1
        elif score >= 0.2:
            sentiment_result["부정"] += 1
        else:
            sentiment_result["매우 부정"] += 1

        print("---------------------------------------------------------------")
    if page_num == 10:
        break
    page_num += 1

# https://pyecharts.readthedocs.io/projects/pyecharts-en/zh/latest/en-us/charts_base/


# Pyecharts

bar3d = Bar3D("감성분석결과", width=1200, height=600)

# x축 lable
x_axis = [
    "매우긍정",
    "긍정",
    "중립",
    "부정",
    "매우부정"
]

# y축 레이블
y_axis = [

]

# 데이터 [x, y, h]
data = [
    [0, 0, sentiment_result.get("매우 긍정")],
    [0, 1, sentiment_result.get("긍정")],
    [0, 2, sentiment_result.get("중립")],
    [0, 3, sentiment_result.get("부정")],
    [0, 4, sentiment_result.get("매우 부정")]
]

# 데이터 범위
min_value = min(list(sentiment_result.values()))
max_value = max(list(sentiment_result.values()))

# 색상 범주
range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
               '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']

range_color.reverse()

# plot
bar3d.add("", x_axis, y_axis, [[d[1], d[0], d[2]] for d in data],
          is_visualmap=True, visual_range=[min_value, max_value], visual_range_color=range_color,
          grid3d_width=200, grid3d_depth=20, grid3d_shading="lambert")

bar3d.render("./bar.html")

# html 파일 자동 열기
# import webbrowser
# import os
ap = os.path.abspath("./bar.html")
webbrowser.open(ap)

# ------------------------------------------------------------------------------------

# Pie Graph
# from pyecharts import Pie
attr = [
    "매우긍정",
    "긍정",
    "중립",
    "부정",
    "매우부정"
]

v1 = [
    sentiment_result.get("매우 긍정"),
    sentiment_result.get("긍정"),
    sentiment_result.get("중립"),
    sentiment_result.get("부정"),
    sentiment_result.get("매우 부정"),
]

pie = Pie("감성분석결과", title_pos='center')

pie.add("", attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True,
        legend_orient='vertical', legend_pos='left')
pie.render("./pie.html")
ap = os.path.abspath("./pie.html")
webbrowser.open(ap)
