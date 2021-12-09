import datetime, json, logging, pprint
from django.urls import reverse

log = logging.getLogger(__name__)


class Prepper():
    """ Prepares data. """

    def __init__( self ):
        pass

    def make_data( self, start_param, end_param ):
        ## get processed history entries
        ## get history-entry counts by service-name
        ## get requests entries
        ## get relevant request-entry counts
        data = {}
        log.debug( f'data, ``{pprint.pformat(data)}``' )
        return data

    ## end Prepper()



class Validator():
    """ Checks params & handles bad request. """

    def __init__( self ):
        self.start_date = ''
        self.end_date = ''

    def validate_params( self, params ):
        """ Checks for proper parameters & updates dates
            Called by views.stats() """
        log.debug( f'starting validate_request()' )
        assert type(params) == dict
        params_valid = False
        if 'start_date' in params.keys() and 'end_date' in params.keys():
            if self.good_date( params['start_date'] ) and self.good_date( params['end_date'] ):
                if self.date_order_ok( params['start_date'], params['end_date'] ):
                    self.start_date = params['start_date']
                    self.end_date = params['end_date']
                    params_valid = True
        log.debug( f'params_valid, ``{params_valid}``' )
        return params_valid

    def good_date( self, submitted_param ):
        """ Checks for valid date.
            Called by validate_params() """
        assert type(submitted_param) == list, type(submitted_param)
        submitted_date = submitted_param[0]
        assert type(submitted_date) == str, type(submitted_date)
        is_good_date = False
        try:
            datetime_obj = datetime.datetime.strptime( submitted_date, '%Y-%m-%d' )
            assert type(datetime_obj) == datetime.datetime
            is_good_date = True
        except:
            log.exception( 'problem with date; processing continues' )
        log.debug( f'is_good_date, ``{is_good_date}``' )
        return is_good_date

    def date_order_ok( self, start_param, end_param ):
        """ Ensures start-date is less than end-date.
            Called by validate_params() """
        assert type(start_param) == list
        assert type(end_param) == list
        start_str = start_param[0]
        end_str = end_param[0]
        assert type(start_str) == str
        assert type(end_str) == str
        order_ok = False
        start_dt_obj = datetime.datetime.strptime( start_str, '%Y-%m-%d' )
        end_dt_obj = datetime.datetime.strptime( end_str, '%Y-%m-%d' )
        if start_dt_obj <= end_dt_obj:
            order_ok = True
        log.debug( f'order_ok, ``{order_ok}``' )
        return order_ok

    def build_bad_param_message( self, request_now_time, scheme, host, path, querystring ):
        """ Builds helpful bad-param text.
            Called by views.stats() """
        log.debug( f'scheme, ``{scheme}``; host, ``{host}``; path, ``{path}``; querystring, ``{querystring}``' )
        log.debug( f'reverse("stats_api_v2_url"), ``{reverse("stats_api_v2_url")}``' )
        assert type(request_now_time) == datetime.datetime
        assert type(scheme) == str, type(scheme)
        assert type(host) == str, type(host)
        assert type(path) == str, type(path)
        assert type(querystring) == str, type(querystring)
        if querystring:
            submitted_url = f'{scheme}://{host}{path}?{querystring}'
        else:
            submitted_url = f'{scheme}://{host}{path}'
        log.debug( f'submitted_url, ``{submitted_url}``' )
        data = {
            'request': {
                'url': submitted_url,
                'timestamp': str( request_now_time )
            },
            'response': {
                'status': '400 / Bad Request',
                'message': f'example url: {scheme}://{host}{path}?start_date=2010-01-20&end_date=2010-01-30',
                'timetaken': str( datetime.datetime.now() - request_now_time )
            }
        }
        jsn = json.dumps( data, sort_keys=True, indent=2 )
        log.debug( f'jsn, ``{jsn}``' )
        return jsn

    ## end class Validator()
