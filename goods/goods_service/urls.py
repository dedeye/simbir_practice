from django.urls import path
from goods_service import views

app_name = "goods"

advert_detail = views.Advert.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('advert/<int:pk>', advert_detail),
    path('advert', views.Advert.as_view({'post': 'create'})),
    path('advertBrief/<int:pk>', views.AdvertBrief.as_view({'get': 'detail'})),
    path('advertBrief', views.AdvertBrief.as_view({'get': 'list'})),

]
