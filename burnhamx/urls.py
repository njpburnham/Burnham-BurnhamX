from django.conf.urls import patterns, include, url
from rest_framework import routers
from api import views as api_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'opportunity', api_views.OpportunityViewSet)
router.register(r'association', api_views.AssociationViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'burnhamx.views.home', name='home'),
    # url(r'^burnhamx/', include('burnhamx.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'/', include('extension.urls')),    

)
