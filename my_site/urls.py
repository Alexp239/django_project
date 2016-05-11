"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from traveler import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/$', views.main, name="Main"),
    url(r'^dialogs/$', views.dialogs, name="Dialogs"),
    url(r'^messages/(?P<to_person_id>\d+)/$', views.messages, name="Messages"),
    url(r'^profile/(?P<person_id>\d+)/$', views.profile, name="Profile"),
    url(r'^city/(?P<city_id>\d+)/(?P<trips_page>\d+)/(?P<comments_page>\d+)/$', views.city),
    url(r'^countries/(?P<page>\d+)/$', views.countries),
    url(r'^country/(?P<country_id>\d+)/(?P<page>\d+)/$', views.country),
    url(r'^registration/', views.registration),
    url(r'^login/', views.user_login),
    url(r'^logout/', views.user_logout),
    url(r'^update_like_city/(?P<object_id>\d+)/$', views.update_like_city),
    url(r'^update_like_country/(?P<object_id>\d+)/$', views.update_like_country, name="UpdateLikeCountry"),
    url(r'^update_add_cities/(?P<city_id>\d+)/$', views.update_add_cities),
    url(r'^update_trip_persons/(?P<trip_id>\d+)/$', views.update_trip_persons),
    url(r'^update_like_person/(?P<object_id>\d+)/$', views.update_like_person),
    url(r'^add_message/(?P<person_id>\d+)/$', views.add_message),
    url(r'^add_comment/(?P<city_id>\d+)/(?P<comment>\d+)/$', views.add_comment),
    url(r'^add_comment/(?P<city_id>\d+)/$', views.add_comment),
    url(r'^add_tag_country/(?P<country_id>\d+)/$', views.add_tag_country),
    url(r'^add_tag_city/(?P<city_id>\d+)/$', views.add_tag_city),
    url(r'^add_tag_person/(?P<person_id>\d+)/$', views.add_tag_person),
    url(r'^add_tag_trip/(?P<trip_id>\d+)/$', views.add_tag_trip),
    url(r'^add_trip/(?P<city_id>\d+)/$', views.add_trip)
    ]
