from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ajax/notification/$', views.user_notification, name='user_notification'),
    url(r'^account/notification/$', views.notification_list, name='user_notification_list'),
]
