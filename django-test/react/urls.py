from django.conf.urls import url
from . import views

app_name = 'notes'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='list'),
    url(r'^comments/$', views.handle_comments, name='comments'),
    url(r'^thinking/$', views.ThinkingView.as_view(), name='thinking')
]
