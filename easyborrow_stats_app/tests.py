import json, logging

from django.test import TestCase
from easyborrow_stats_app.lib.stats_helper import Validator


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class ClientTest( TestCase ):
    """ Checks urls. """

    def test_stats_missing_params(self):
        """ Checks `/stats_api/v2/` with missing params. """
        response = self.client.get( '/stats_api/v2/' )
        self.assertEqual( 400, response.status_code )  # HttpResponseBadRequest()
        resp_dct = json.loads( response.content )
        self.assertEqual(
            'example url: http://127.0.0.1/stats_api/v2/?start_date=2010-01-20&end_date=2010-01-30',  # true for runserver _client_ test (no port)
            resp_dct['response']['message']
            )

    def test_stats_good_params(self):
        """ Checks `/stats_api/v2/` with good params. """
        response = self.client.get( '/stats_api/v2/?start_date=2010-01-20&end_date=2010-01-30' )
        self.assertEqual( 200, response.status_code )

    def test_feed(self):
        """ Checks `/feeds/latest_items/`. """
        response = self.client.get( '/feeds/latest_items/' )
        self.assertEqual( 200, response.status_code )


class ValidatorTest( TestCase ):
    """ Checks stats_helper.py """

    def setUp(self):
        self.validator = Validator()

    def test_params_valid__no_params(self):
        """ Checks params handling; no params sent. """
        params = {}
        self.assertEqual( False, self.validator.validate_params( params ) )
        self.assertEqual( '', self.validator.start_date )
        self.assertEqual( '', self.validator.end_date )

    def test_params_valid__good_params_but_invalid_date(self):
        """ Checks params handling; no params sent. """
        params = { 'start_date': 'foo', 'end_date': 'bar' }
        self.assertEqual( False, self.validator.validate_params( params ) )
        self.assertEqual( '', self.validator.start_date )
        self.assertEqual( '', self.validator.end_date )

    def test_params_valid__good_params_and_out_of_order_dates(self):
        """ Checks params handling; no params sent. """
        params = { 'start_date': '2020-01-30', 'end_date': '2020-01-20' }
        self.assertEqual( False, self.validator.validate_params( params ) )
        self.assertEqual( '', self.validator.start_date )
        self.assertEqual( '', self.validator.end_date )

    def test_params_valid__good_params_and_good_dates(self):
        """ Checks params handling; no params sent. """
        params = { 'start_date': '2020-01-20', 'end_date': '2020-01-30' }
        self.assertEqual( True, self.validator.validate_params( params ) )
        self.assertEqual( '2020-01-20', self.validator.start_date )
        self.assertEqual( '2020-01-30', self.validator.end_date )
