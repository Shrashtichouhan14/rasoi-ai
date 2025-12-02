from django.urls import path
from . import views

urlpatterns = [
    # The home page
    path('', views.index, name='index'),
    
    # The endpoint our JavaScript will talk to
    path('api/chat', views.chat_api, name='chat_api'),
    path('api/clear', views.clear_session, name='clear_session'),
]