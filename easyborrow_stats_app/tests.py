import logging

from django.test import TestCase
from easyborrow_stats_app.lib.stats_helper import Stats_Helper


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class ClientTest( TestCase ):
    """ Checks urls. """

    def test_stats_missing_params(self):
        """ Checks `/stats_api/v2/`. """
        response = self.client.get( '/stats_api/v2/' )
        self.assertEqual( 400, response.status_code )  # HttpResponseBadRequest()


class StatsHelperTest( TestCase ):
    """ Checks stats_helper.py """

    def setUp(self):
        self.stats_hlpr = Stats_Helper()

    def test_params_valid__no_params(self):
        """ Checks params handling; no params sent. """
        params = {}
        self.assertEqual( False, self.stats_hlpr.validate_params( params ) )
        self.assertEqual( '', self.stats_hlpr.start_date )
        self.assertEqual( '', self.stats_hlpr.end_date )

    def test_params_valid__good_params_but_invalid_date(self):
        """ Checks params handling; no params sent. """
        params = { 'start_date': 'foo', 'end_date': 'bar' }
        self.assertEqual( False, self.stats_hlpr.validate_params( params ) )
        self.assertEqual( '', self.stats_hlpr.start_date )
        self.assertEqual( '', self.stats_hlpr.end_date )

    def test_params_valid__good_params_and_out_of_order_dates(self):
        """ Checks params handling; no params sent. """
        params = { 'start_date': '2020-01-30', 'end_date': '2020-01-20' }
        self.assertEqual( False, self.stats_hlpr.validate_params( params ) )
        self.assertEqual( '', self.stats_hlpr.start_date )
        self.assertEqual( '', self.stats_hlpr.end_date )

    def test_params_valid__good_params_and_good_dates(self):
        """ Checks params handling; no params sent. """
        params = { 'start_date': '2020-01-20', 'end_date': '2020-01-30' }
        self.assertEqual( True, self.stats_hlpr.validate_params( params ) )
        self.assertEqual( '2020-01-20', self.stats_hlpr.start_date )
        self.assertEqual( '2020-01-30', self.stats_hlpr.end_date )
