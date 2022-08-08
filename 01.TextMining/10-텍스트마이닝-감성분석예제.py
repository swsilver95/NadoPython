import sentiment_module

test_sentence = "정신 좀 차리세요."
result = sentiment_module.sentiment_predict(test_sentence)

if result >= 0.5:
    print(f"{result * 100:.2f}% 확률로 긍정입니다.")
else:
    print(f"{100 - result * 100:.2f}% 확률로 부정입니다.")
