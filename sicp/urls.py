from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sicp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','principal.views.lista_proyectos'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
