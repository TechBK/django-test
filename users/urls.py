from django.conf.urls import url
from .views import LogInView, LogOutView, SignInView, DetailView

app_name = 'users'

urlpatterns = [
    url(r'^profile/$', DetailView.as_view(), name='detail'),
    url(r'^signin/$', SignInView.as_view(), name='signin'),
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
]
