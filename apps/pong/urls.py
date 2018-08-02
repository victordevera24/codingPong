from django.conf.urls import url
from . import views

  
urlpatterns = [
    url(r'^$', views.index),
    url(r'process$', views.process), 
    url(r'login$', views.login),
    url(r'dashboard$', views.success),
    url(r'add/(?P<id>\d+)$', views.add),
    url(r'remove$', views.remove),
    url(r'accept/(?P<id>\d+)$', views.accept),
    url(r'gameon/(?P<id>\d+)$', views.gameon),
    url(r'ranking/(?P<win>\d+)/(?P<loss>\d+)$', views.ranking),
    url(r'leaderboard$', views.leaderboard),
    url(r'ninjas$', views.ninjas),
    url(r'ninja/(?P<id>\d+)$', views.profile),
    url(r'post_message/(?P<id>\d+)$', views.post_message),
    url(r'update/(?P<id>\d+)$', views.update),
]