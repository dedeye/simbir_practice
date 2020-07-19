from django.urls import path, include
from goods_service import views
from rest_framework.routers import DefaultRouter

app_name = "goods"

# advert_detail = views.Advert.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })


# urlpatterns = [
#     path('', views.api_root),
#     path('advert/<int:pk>',
#          advert_detail,
#          name='advert-detail'),

#     path('advert/',
#          views.Advert.as_view({'post': 'create'}),
#          name='advert-create'),

#     path('advert/brief/<int:pk>',
#          views.AdvertBrief.as_view({'get': 'detail'}),
#          name='advert-brief'),

#     path('advert/brief/',
#          views.AdvertBrief.as_view({'get': 'list'}),
#          name='advert-brief-list'),

# ]
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'advert', views.Advert, )
# router.register(r'advert_brief', views.AdvertBrief)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
