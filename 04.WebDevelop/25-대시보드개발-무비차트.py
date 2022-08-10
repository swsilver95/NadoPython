import urllib.request as req
import webbrowser
from bs4 import BeautifulSoup
import streamlit as st

st.title("무비차트")


code = req.urlopen("http://www.cgv.co.kr/movies/")
soup = BeautifulSoup(code, "html.parser")
title = soup.select("div.sect-movie-chart strong.title")
img = soup.select("div.sect-movie-chart span.thumb-image > img")
URL = "http://www.cgv.co.kr"
buttons = soup.select("a.link-reservation")
for i in range(len(title)):
    st.write(f"**{i + 1}위** : {title[i].text}")
    st.image(img[i].attrs["src"], width=200)
    reservation_url = URL + buttons[i].attrs["href"]
    if st.button("예매하기", key=f"button{i}"):
        webbrowser.open(reservation_url)
