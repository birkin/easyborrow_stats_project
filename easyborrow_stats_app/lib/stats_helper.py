import datetime, logging


log = logging.getLogger(__name__)


class Stats_Helper():

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

    def good_date( self, submitted_date ):
        """ Checks for valid date.
            Called by validate_params() """
        assert type(submitted_date) == str
        is_good_date = False
        try:
            datetime_obj = datetime.datetime.strptime( submitted_date, '%Y-%m-%d' )
            assert type(datetime_obj) == datetime.datetime
            is_good_date = True
        except:
            log.exception( 'problem with date; processing continues' )
        log.debug( f'is_good_date, ``{is_good_date}``' )
        return is_good_date

    def date_order_ok( self, start_str, end_str ):
        """ Ensures start-date is less than end-date.
            Called by validate_params() """
        assert type(start_str) == str
        assert type(end_str) == str
        order_ok = False
        start_dt_obj = datetime.datetime.strptime( start_str, '%Y-%m-%d' )
        end_dt_obj = datetime.datetime.strptime( end_str, '%Y-%m-%d' )
        if start_dt_obj <= end_dt_obj:
            order_ok = True
        log.debug( f'order_ok, ``{order_ok}``' )
        return order_ok


# date_time_str = '2018-06-29 08:15:27.243860'
# date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')


    # if u'start_date' not in get_params or u'end_date' not in get_params:  # not valid
    #   url = u'%s://%s%s' % ( http_scheme, server_name, request_uri )
    #   data = {
    #     u'request': { u'url': url },
    #     u'response': {
    #       u'status': u'400 / Bad Request',
    #       u'message': u'example url: http://%s/easyborrow/stats_api/v2/?start_date=2010-01-20&end_date=2010-01-30' % server_name,
    #       }
    #     }
    #   self.output = json.dumps( data, sort_keys=True, indent=2 )
    #   return False
    # else:  # is valid
    #   if u'detail' in get_params:
    #     self.detail = get_params[u'detail']
    #   self.date_start = u'%s 00:00:00' % get_params[u'start_date']
    #   self.date_end = u'%s 23:59:59' % get_params[u'end_date']
    #   return True
