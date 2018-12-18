from django.urls import path
from . import views

urlpatterns =[
    path('IOT',views.IOT_data, name='IOT_data'),
    path('about',views.about,name='about')
]