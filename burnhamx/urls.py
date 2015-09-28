from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest_framework_bulk.routes import BulkRouter
from api import views as api_views
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# router = routers.DefaultRouter()
router = BulkRouter()
router.register(r'opportunity', api_views.OpportunityViewSet)
router.register(r'association', api_views.AssociationViewSet)
router.register(r'users', api_views.UsersViewSet)
router.register(r'permissions', api_views.PermissionsViewSet)




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
    url(r'^extension', include('extension.urls')),    

)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )