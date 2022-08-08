from konlpy.tag import Okt

# Open Korean Text
okt = Okt()

# stem 옵션은 단어의 원형을 반환하는 옵션이다.
result = okt.pos('신한은행은 명실상부 최고의 은행이다.', stem=False)
print(result)
