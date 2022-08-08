from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
from pprint import pprint
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image # pip install pillow

keyword = input("키워드 입력 >> ").rstrip()
encoded = par.quote(keyword)  # 한글 -> 특수한 문자
output_total = ""

page_num = 1
while page_num <= 1:
    url = f"https://www.joongang.co.kr/_CP/496?keyword={encoded}&sort%20=&pageItemId=439&page={page_num}"
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline a")
    if len(title) == 0:  # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        print("제목 :", i.text.strip())
        print("링크 :", i.attrs["href"])
        code_news = req.urlopen(i.attrs["href"])
        soup_news = BeautifulSoup(code_news, "html.parser")
        content = soup_news.select_one("div#article_body")
        result = content.text.replace("\n", " ").strip()
        output_total += result
        print(result)
        print()
    page_num += 1

# 텍스트마이닝 시작
okt = Okt()
nouns_list = okt.nouns(output_total)
# print(nouns_list)

# 불필요한 단어(불용어) 삭제 작업
# 원래는 불용어사전을 제작해서 작업해야 하지만, 간이식으로 한 글자 단어를 삭제

tmp = nouns_list[:]
for i in tmp:
    if len(i) == 1:
        nouns_list.remove(i)
print(nouns_list)


# 단어 빈도수 카운트
# from collections import Counter
count_result = Counter(nouns_list)
print(count_result)


# 엑셀로 추출
# import pandas
df = pd.DataFrame.from_dict(count_result, orient="index", columns=["빈도수"])
df = df.sort_values(by="빈도수", ascending=False)
pprint(df)
df.to_excel("./단어빈도수.xlsx")


# 이미지 불러오기
# import numpy as np
# from PIL import Image
# from wordcloud import ImageColorGenerator
image_array = np.array(Image.open("../logo.png"))
image_color = ImageColorGenerator(image_array)


# 단어구름 만들기
# from wordcloud import WordCloud
wc = WordCloud(mask=image_array, background_color="white", font_path="../NanumMyeongjo.ttf")\
    .generate_from_frequencies(count_result)\
    .recolor(color_func=image_color)


# svg 파일로 이미지 저장하기
wc_svg = wc.to_svg(embed_font=True)
f = open("./wordcloud.svg", "w", encoding="utf-8")
f.write(wc_svg)
f.close()


# 단어구름 그리기
# import matplotlib.pyplot as plt
plt.figure()
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
