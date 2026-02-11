import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from django.conf import settings
from matplotlib import font_manager, rc
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "..", "static", "images")
os.makedirs(IMG_DIR, exist_ok=True)

font_path = "C:/Windows/Fonts/malgun.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc("font", family=font)


def statistics():

    df = pd.read_excel("static/files/행복지수(2021).xlsx")

    target_cols = [
        "행복지수", "건강상태", "재정상태",
        "친지_친구와의 관계", "가정생활", "사회생활"
    ]

    data = df[target_cols]

    avg_happiness = data["행복지수"].mean()

    corr = data.corr(numeric_only=True)

    corr_happy_health = corr.loc["행복지수", "건강상태"]
    corr_happy_financial = corr.loc["행복지수", "재정상태"]

    # Heatmap 저장
    plt.figure(figsize=(12, 6))
    sns.heatmap(corr, annot=True, cmap="GnBu", vmin=0.6, vmax=1.0)
    heatmap_path = os.path.join(IMG_DIR, "heatmap.png")
    plt.savefig(heatmap_path, dpi=200, bbox_inches="tight")
    plt.close()

    return (
        round(avg_happiness, 2),
        round(corr_happy_health, 2),
        round(corr_happy_financial, 2),
        corr
    )


def chart_draw():

    df = pd.read_excel("static/files/행정구역_시군구_별__성별_인구수.xlsx")


    data = df[df["gugun"] == "소계"]

    chart_df = data[["sido", "total"]].copy()


    chart_df = chart_df.sort_values("total", ascending=False)

    plt.figure(figsize=(14, 6))
    sns.barplot(data=chart_df, x="sido", y="total")

    plt.xticks(rotation=45)
    plt.title("광역시도 총 인구수", fontsize=14)

    save_path = os.path.join(settings.STATICFILES_DIRS[0], "images", "bar_chart.png")
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()

    return chart_df





def map_draw():
    # 1. 행정구역 인구수 데이터 로드
    df = pd.read_excel("static/files/행정구역_시군구_별__성별_인구수.xlsx")

    # 2. 전처리: 공백제거, total > 0, '소계'만 사용 (시도 단위 합계)
    df["gugun"] = df["gugun"].apply(lambda v: v.strip())
    df1 = df.loc[df["total"] > 0, :]
    df_sido = df1.loc[df1["gugun"] == "소계", :].copy()

    # 3. 지도 생성 (전국 중심)
    m = folium.Map(location=[37.559819, 126.96389], zoom_start=7)

    # 4. 시도 경계 geojson 로드
    geojson_path = os.path.join("static", "files", "ctprvn.json")
    with open(geojson_path, "r", encoding="utf-8") as f:
        sido_geo = json.load(f)

    # 경계선 추가 (옵션)
    folium.GeoJson(sido_geo, name="시도").add_to(m)

    # 5. 시도별 인구수 choropleth
    folium.Choropleth(
        geo_data=sido_geo,
        data=df_sido,
        columns=["sido", "total"],
        key_on="properties.CTP_KOR_NM",
        fill_color="RdYlGn",
        fill_opacity=0.6,
        line_opacity=0.2,
        legend_name="시도별 총 인구수",
    ).add_to(m)

    # 6. 저장 위치 (templates/dataprocess/map01.html)
    save_path = os.path.join(BASE_DIR, "templates", "dataprocess", "map01.html")
    m.save(save_path)

    return save_path