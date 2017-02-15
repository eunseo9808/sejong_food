from django.conf.urls import patterns, include, url
from django.contrib import admin
from food.views import *
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sejongfood.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^save_all/$', save_all,name="save_all"),
    url(r'^save_student_data/$', save_student_data, name='save_student_data'),
    url(r'^save_skyrounge_data/$', save_skyrounge_data, name='save_skyrounge_data'),
    url(r'^save_woojung_data/$', save_woojung_data, name='save_woojung_data'),
    url(r'^save_kunja_data/$', save_kunja_data, name='save_kunja_data'),
    url(r'^get_student_data/$', get_student_data,name='get_student_data'),
    url(r'^get_skyrounge_data/$', get_skyrounge_data,name='get_skyrounge_data'),
    url(r'^get_woojung_data/$', get_woojung_data,name='get_woojung_data'),
    url(r'^get_kunja_data/$', get_kunja_data,name='get_kunja_data'),
)
