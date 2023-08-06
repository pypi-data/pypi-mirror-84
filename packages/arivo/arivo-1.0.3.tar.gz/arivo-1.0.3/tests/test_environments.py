from unittest import TestCase

import arivo


class TestEnvironments(TestCase):
    def test_production_is_default(self):
        initial_api_url = "" + arivo.api_url
        arivo.use_production()
        self.assertEqual(initial_api_url, arivo.api_url)

    def test_switch_between_production_and_staging(self):
        initial_api_url = "" + arivo.api_url
        arivo.use_staging()
        self.assertNotEqual(initial_api_url, arivo.api_url)

        arivo.use_production()
        self.assertEqual(initial_api_url, arivo.api_url)
