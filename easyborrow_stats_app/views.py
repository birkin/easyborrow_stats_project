import datetime, json, logging

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from easyborrow_stats_app.lib.stats_helper import Stats_Helper
from easyborrow_stats_app.lib import version_helper




log = logging.getLogger(__name__)
stats_hlpr = Stats_Helper()


# ===========================
# main urls
# ===========================


def info( request ):
    return HttpResponse( 'Hello, world. You\'re at the info page.' )


def stats( request ):
    log.debug( '\n\nstarting stats()' )
    params_valid = stats_hlpr.validate_params( dict(request.GET) )
    assert type( params_valid ) == bool
    if params_valid:
        resp = HttpResponse( 'stats response coming' )
    else:
        resp = HttpResponseBadRequest( 'invalid params' )
    return resp


def feed( request ):
    return HttpResponse( 'feed response coming' )


# ===========================
# support urls
# ===========================


def version( request ):
    """ Returns basic branch and commit data. """
    rq_now = datetime.datetime.now()
    commit = version_helper.get_commit()
    branch = version_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    context = version_helper.make_context( request, rq_now, info_txt )
    output = json.dumps( context, sort_keys=True, indent=2 )
    log.debug( f'output, ``{output}``' )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development).
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    log.debug( f'project_settings.DEBUG, ``{project_settings.DEBUG}``' )
    if project_settings.DEBUG == True:
        raise Exception( 'error-check triggered; admin emailed' )
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )
