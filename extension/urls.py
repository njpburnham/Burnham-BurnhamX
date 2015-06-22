from django.conf.urls import patterns, include, url

urlpatterns = patterns('extension.views',   
    url(r'/thanks', 'thanks'),
    url(r'/associate/(?P<thread_id>\w+)/(?P<message_id>\w+)/', 'associate'),
    url(r'/bulkassociate/(?P<thread_ids>\w+)/$', 'bulk_associate'),
    url(r'/unassociate/', 'unassociate'),
    url(r'/pastAssociation/', 'past_association'),
    url(r'/future/', 'future')
)  
