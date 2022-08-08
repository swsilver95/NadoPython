score = int(input('점수를 입력해 주세요: '))

credit = ''
if score >= 90:
    credit = 'A'
elif score >= 80:
    credit = 'B'
elif score >= 70:
    credit = 'C'
else:
    credit = 'D'

print('학점: ' + credit)
