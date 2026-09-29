"""Opt-in Selenium checks on a temporary Django test database, never local data.

RUN_BROWSER_TESTS=1 python manage.py test main.test_browser --noinput
Requires locally installed Chrome and the optional selenium package.
"""
import os
import time
from unittest import skipUnless

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


@skipUnless(os.environ.get('RUN_BROWSER_TESTS') == '1', 'Opt-in Selenium browser suite')
class ProjectBrowserTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1440,1000')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})
        try:
            cls.browser = webdriver.Chrome(options=options)
        except Exception:
            super().tearDownClass()
            raise
        cls.wait = WebDriverWait(cls.browser, 10)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.browser.quit()
        finally:
            super().tearDownClass()

    def setUp(self):
        self.browser.delete_all_cookies()
        self.browser.get_log('browser')

    def test_toast_repeated_calls_types_text_and_auto_hide(self):
        self.browser.get(self.live_server_url + '/')
        self.browser.execute_script("showToast('<b>Judul</b>', '<img src=x onerror=alert(1)>', 'success')")
        self.assertTrue(self.browser.execute_script("return document.getElementById('toast-component').matches(':popover-open')"))
        self.wait.until(lambda d: d.find_element('id', 'toast-title').text == '<b>Judul</b>')
        self.assertEqual(self.browser.find_elements('css selector', '#toast-component img, #toast-component b'), [])
        self.wait.until(lambda d: not d.execute_script("return document.getElementById('toast-component').matches(':popover-open')"))
        # A toast arriving during the exit animation must cancel the old hide timer.
        self.browser.execute_script("showToast('First', 'Old', 'error', 20)")
        self.wait.until(lambda d: 'toast-hidden' in d.find_element('id', 'toast-component').get_attribute('class'))
        self.browser.execute_script("showToast('Second', 'Current', 'success', 1000)")
        time.sleep(0.4)
        self.assertTrue(self.browser.execute_script("return document.getElementById('toast-component').matches(':popover-open')"))
        self.assertIn('toast-success', self.browser.find_element('id', 'toast-component').get_attribute('class'))
        self.assertNotIn('toast-error', self.browser.find_element('id', 'toast-component').get_attribute('class'))
        self.browser.execute_script("showToast('Normal', 'Current', 'unknown', 20)")
        self.assertIn('toast-normal', self.browser.find_element('id', 'toast-component').get_attribute('class'))
        self.wait.until(lambda d: not d.execute_script("return document.getElementById('toast-component').matches(':popover-open')"))
        self.browser.execute_script("document.getElementById('toast-component').remove(); showToast('Missing', 'Safe')")
        errors = [entry for entry in self.browser.get_log('browser') if entry['source'] == 'javascript' and entry['level'] == 'SEVERE']
        self.assertEqual(errors, [])
