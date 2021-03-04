from django.contrib import admin
from django.urls import path
from easyborrow_stats_app import views


urlpatterns = [

    ## primary urls...

    path( 'info/', views.info, name='info_url' ),
    path( 'stats_api/v2/', views.stats, name='stats_api_v2_url' ),
    path( 'feeds/latest_items/', views.feed, name='feed_url' ),
    path('admin/', admin.site.urls),  ## enabled by default, but disabled here as a reminder that django can be very lightweight

    ## support urls...

    path( 'version/', views.version, name='version_url' ),
    path( 'error_check/', views.error_check, name='error_check_url' ),
]

