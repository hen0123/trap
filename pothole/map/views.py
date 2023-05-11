from django.shortcuts import render
import folium
from folium import IFrame
import base64

# Create your views here.

def warning(request):

    m = folium.Map(location=[37.488277326728294, 126.98273617518873], zoom_start=16)
    html = '<img src="data:image/jpg;base64,{}" style="width:100%; height:100%;">'.format

    pic1 = base64.b64encode(open('./media/report/map1.jpg', 'rb').read()).decode()
    iframe1 = folium.IFrame(html(pic1), width=400, height=400)
    popup1 = folium.Popup(iframe1, max_width=600)

    pic2 = base64.b64encode(open('./media/report/map2.jpg', 'rb').read()).decode()
    iframe2 = folium.IFrame(html(pic2), width=400, height=400)
    popup2 = folium.Popup(iframe2, max_width=600)

    pic3 = base64.b64encode(open('./media/report/map3.jpg', 'rb').read()).decode()
    iframe3 = folium.IFrame(html(pic3), width=400, height=400)
    popup3 = folium.Popup(iframe3, max_width=600)

    folium.Marker(
        [37.489117001764065, 126.98230178081931], popup=popup1, tooltip="이수역1", icon=folium.Icon(color='red')).add_to(m)

    folium.Marker(
        [37.488745816204464, 126.98250087625844], popup=popup2, tooltip="이수역2", icon=folium.Icon(color='red')).add_to(m)

    folium.Marker(
        [37.48765373707845, 126.98211668958108], popup=popup3, tooltip="이수역3", icon=folium.Icon(color='red')).add_to(m)

    t = m._repr_html_()
    data = {}
    data['map'] = t

    return render(request, 'map/warning.html', data)


