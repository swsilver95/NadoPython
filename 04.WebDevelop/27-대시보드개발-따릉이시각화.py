from pprint import pprint
import pandas as pd
import streamlit as st
import requests
import json
import pydeck as pdk

bike_dict = {
    "rackTotCnt": [],
    "stationName": [],
    "parkingBikeTotCnt": [],
    "shared": [],
    "latitude": [],
    "longitude": []
}

api_key = "757766614b74616c374a46696a55"
num = 0
while True:
    data = requests.get(f"http://openapi.seoul.go.kr:8088/{api_key}/json/bikeList/{1000*num + 1}/{1000*num+1000}/")
    result = json.loads(data.text) # json --> 딕셔너리
    for row in result["rentBikeStatus"]["row"]:
        bike_dict["rackTotCnt"].append(int(row["rackTotCnt"]))
        bike_dict["stationName"].append(row["stationName"])
        bike_dict["parkingBikeTotCnt"].append(int(row["parkingBikeTotCnt"]))
        bike_dict["shared"].append(int(row["shared"]))
        bike_dict["latitude"].append(float(row["stationLatitude"]))
        bike_dict["longitude"].append(float(row["stationLongitude"]))
    if result["rentBikeStatus"]["list_total_count"] != 1000:
        break
    num += 1


# pprint(bike_dict)
df = pd.DataFrame(bike_dict)

st.title("따릉이 실시간 정보")
st.dataframe(df)

# 따릉이 실시간 정보 시각화 (Pydeck)
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["longitude", "latitude"],
    get_radius="60*shared/100",
    get_fill_color="[255-shared, 220, 255-shared]",
    pickable=True
)
lat_center = df["latitude"].mean()
lon_center = df["longitude"].mean()

st.write("## Map")
initial_view = pdk.ViewState(latitude=lat_center, longitude=lon_center, zoom=10)
my_map = pdk.Deck(layers=[layer],
                  initial_view_state=initial_view,
                  tooltip={
                      "html": "정류장 : {stationName}</br>현재 주차 대수 : {parkingBikeTotCnt}",
                      "style": "color: white;"
                  },
                  map_style="dark")
st.pydeck_chart(my_map)

