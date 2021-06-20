
from django.urls import path
from . import views

app_name = 'app1'
urlpatterns = [

    path('', views.home, name = 'home' ),
    #path('submit_review', views.submit_review ,name="submit_review"),
    #path('home', views.home, name = 'home' )
    
        
    
]