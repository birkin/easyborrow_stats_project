from django.contrib import admin
from django.urls import path
from easyborrow_stats_app import views



urlpatterns = [

    ## primary urls...

    # path( '', views.info, name='root_url' ),

    path( '', views.root, name='root_url' ),

    path( 'info/', views.info, name='info_url' ),
    path( 'stats_api/v2/', views.stats, name='stats_api_v2_url' ),
    path( 'feeds/latest_items/', views.feed, name='feed_url' ),
    path( 'admin/', admin.site.urls ),
    # path( r'^$', RedirectView.as_view(pattern_name='info_url') ),

    ## support urls...

    path( 'version/', views.version, name='version_url' ),
    path( 'error_check/', views.error_check, name='error_check_url' ),
]

