# https://pyecharts.readthedocs.io/projects/pyecharts-en/zh/latest/en-us/charts_base/

from pyecharts import Bar3D
import webbrowser
import os


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

# 데이터 (x, y, h)
data = [
        [0, 0, 35], [0, 1, 80], [0, 2, 15], [0, 3, 20], [0, 4, 1]
]

# 색상 범주
range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
               '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']

range_color.reverse()

bar3d.add("", x_axis, y_axis, [[d[1], d[0], d[2]] for d in data],
          is_visualmap=True, visual_range=[0, 100], visual_range_color=range_color,
          grid3d_width=200, grid3d_depth=20, grid3d_shading="lambert")

bar3d.render("./bar.html")

# html 파일 자동 열기
# import webbrowser
# import os
ap = os.path.abspath("./bar.html")
webbrowser.open(ap)
