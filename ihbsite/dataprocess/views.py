from django.shortcuts import render
from django.utils import timezone
from dataprocess import datapro




# Create your views here.
def dashboard(request):
    return render(request, 'dataprocess/dashboard.html')



def statistics(request):

    avg, corr_health, corr_financial, corr = datapro.statistics()

    corr_labels = list(corr.columns)

    corr_table = [
        {
            "label": idx,
            "values": list(corr.loc[idx])
        }
        for idx in corr.index
    ]

    context = {
        "avg_happiness": avg,
        "corr_health": corr_health,
        "corr_financial": corr_financial,

        "updated_at": timezone.now().strftime("%Y-%m-%d"),

        "corr_labels": corr_labels,
        "corr_table": corr_table,

        "heatmap_url": "/static/images/heatmap.png",
    }

    return render(request, "dataprocess/statistics.html", context)





def charts(request):

    datapro.chart_draw()   # 이미지는 저장만

    return render(request, "dataprocess/charts.html", {
        "chart_img": "/static/images/bar_chart.png"
    })



def map_view(request):

    map_path = datapro.map_draw()

    return render(request, "dataprocess/map01.html")


def wordclouds(request):
    return render(request, 'dataprocess/wordclouds.html')