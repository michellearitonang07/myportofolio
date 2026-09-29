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

    def seed_project(self, title='Django Portfolio', **kwargs):
        from main.models import Project
        return Project.objects.create(title=title, description=kwargs.get('description', 'A project'),
                                      tech_stack=kwargs.get('tech_stack', 'Django'),
                                      project_url=kwargs.get('project_url', 'https://example.com/'))

    def open_projects(self, query=''):
        self.browser.get(self.live_server_url + '/projects/' + query)
        self.wait.until(lambda d: d.find_element('id', 'project-results').get_attribute('aria-busy') == 'false')

    def assert_no_js_errors(self):
        errors = [entry for entry in self.browser.get_log('browser') if entry['source'] == 'javascript' and entry['level'] == 'SEVERE']
        self.assertEqual(errors, [])

    def test_ajax_load_search_debounce_and_submit_without_reload(self):
        self.seed_project()
        self.seed_project('Other project')
        self.open_projects()
        self.assertEqual(len(self.browser.find_elements('css selector', '#grid article')), 2)
        self.assertEqual(self.browser.find_elements('css selector', '.project-delete-form'), [])
        self.browser.execute_script("""
            window.pageMarker = 'same-document';
            window.projectRequests = [];
            const originalFetch = window.fetch;
            window.fetch = (...args) => {
                projectRequests.push(String(args[0]));
                return originalFetch(...args);
            };
            const input = document.getElementById('search-input');
            for (const value of ['D', 'Dj', 'Django']) {
                input.value = value;
                input.dispatchEvent(new Event('input', {bubbles: true}));
            }
        """)
        self.assertEqual(self.browser.execute_script('return projectRequests.length'), 0)
        self.wait.until(lambda d: len(d.find_elements('css selector', '#grid article')) == 1)
        self.assertEqual(self.browser.execute_script('return projectRequests.length'), 1)
        self.assertIn('title=Django', self.browser.execute_script('return projectRequests[0]'))
        self.browser.execute_script("""
            const input = document.getElementById('search-input');
            input.value = 'missing';
            input.dispatchEvent(new Event('input', {bubbles: true}));
            document.getElementById('project-search-form').requestSubmit();
        """)
        self.wait.until(lambda d: d.find_element('id', 'empty').is_displayed())
        time.sleep(0.4)  # Confirm the cancelled debounce does not send a duplicate request.
        self.assertEqual(self.browser.execute_script('return projectRequests.length'), 2)
        self.assertEqual(self.browser.execute_script('return pageMarker'), 'same-document')
        self.assert_no_js_errors()

    def test_loading_empty_error_retry_and_stale_response(self):
        self.seed_project()
        self.open_projects()
        self.browser.execute_script("""
            window.originalFetch = window.fetch;
            window.fetch = () => Promise.resolve({ok: false, status: 503});
            fetchProjects();
        """)
        self.wait.until(lambda d: d.find_element('id', 'error').is_displayed())
        # The deliberately simulated failure is logged; clear it before checking recovery.
        self.browser.get_log('browser')
        self.browser.execute_script('window.fetch = window.originalFetch')
        self.browser.find_element('id', 'retry-projects').click()
        self.wait.until(lambda d: d.find_element('id', 'grid').is_displayed())
        self.browser.execute_script("""
            window.pendingFetches = [];
            window.fetch = () => new Promise(resolve => pendingFetches.push(resolve));
            fetchProjects('old');
        """)
        self.assertTrue(self.browser.find_element('id', 'loading').is_displayed())
        self.browser.execute_script("""
            fetchProjects('new');
            pendingFetches[1]({ok: true, json: async () => []});
        """)
        self.wait.until(lambda d: d.find_element('id', 'empty').is_displayed())
        self.browser.execute_script("""
            pendingFetches[0]({ok: true, json: async () => [{pk: '00000000-0000-0000-0000-000000000001', fields: {title: 'STALE'}}]});
        """)
        time.sleep(0.2)
        self.assertTrue(self.browser.find_element('id', 'empty').is_displayed())
        self.assertEqual(self.browser.find_elements('css selector', '#grid article'), [])
        self.assert_no_js_errors()

    def test_stored_xss_is_literal_and_unsafe_url_is_omitted(self):
        from django.contrib.auth.models import User
        payload = '<img src="x" onerror="alert(\'XSS!\')">'
        project = self.seed_project(payload, description=payload, tech_stack=payload, project_url='javascript:alert(1)')
        user = User.objects.create_user('" onmouseover="alert(1)')
        project.starred_by.add(user)
        self.open_projects()
        self.assertIn(payload, self.browser.find_element('css selector', '#grid h2').text)
        self.assertEqual(self.browser.find_elements('css selector', '#grid img, #grid script, #grid a'), [])
        button = self.browser.find_element('css selector', '#grid .button-star')
        self.assertEqual(button.get_attribute('title'), 'Dibintangi oleh ' + user.username)
        self.assertIsNone(button.get_attribute('onmouseover'))
        self.assertEqual(button.find_element('class name', 'star-count').text, '1')
        # An unexpected JS alert fails WebDriver commands, so reaching here verifies no execution.
        self.assert_no_js_errors()

    def login_browser(self, superuser=False):
        from django.contrib.auth.models import User
        from django.utils.crypto import get_random_string
        password = get_random_string(24)
        user = User.objects.create_user('browser-owner' if superuser else 'browser-reader',
                                        password=password, is_superuser=superuser, is_staff=superuser)
        self.browser.get(self.live_server_url + '/login/')
        self.browser.find_element('name', 'username').send_keys(user.username)
        self.browser.find_element('name', 'password').send_keys(password)
        self.browser.find_element('css selector', '.project-form button[type=submit]').click()
        self.wait.until(lambda d: d.current_url == self.live_server_url + '/')
        return user

    def test_anonymous_star_redirect_and_authenticated_star_delete(self):
        from main.models import Project
        project = self.seed_project()
        self.open_projects()
        self.browser.find_element('css selector', '#grid .button-star').click()
        self.wait.until(lambda d: '/login/?next=' in d.current_url)
        self.login_browser()
        self.open_projects()
        self.assertEqual(self.browser.find_elements('css selector', '.project-delete-form'), [])
        self.browser.find_element('css selector', '#grid .button-star').click()
        self.wait.until(lambda d: 'Unstar' in d.find_element('css selector', '#grid .button-star').text)
        self.assertEqual(project.starred_by.count(), 1)
        self.browser.find_element('css selector', '#grid .button-star').click()
        self.wait.until(lambda d: d.find_element('css selector', '#grid .star-count').text == '0')
        self.browser.find_element('css selector', '.logout-form button').click()
        self.wait.until(lambda d: not d.find_elements('css selector', '.nav-user'))
        self.login_browser(superuser=True)
        self.open_projects()
        self.browser.find_element('css selector', '.project-delete-form button').click()
        self.browser.switch_to.alert.dismiss()
        self.assertTrue(Project.objects.filter(pk=project.pk).exists())
        self.browser.find_element('css selector', '.project-delete-form button').click()
        self.browser.switch_to.alert.accept()
        self.wait.until(lambda d: d.find_element('id', 'empty').is_displayed())
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())
        self.assert_no_js_errors()

    def test_modal_open_close_keyboard_and_mobile_layout(self):
        from selenium.webdriver.common.keys import Keys
        self.seed_project()
        self.login_browser(superuser=True)
        self.open_projects()
        for selector in ['.project-form-modal__close', '.project-form-modal__actions .button-secondary']:
            self.browser.find_element('class name', 'project-add-button').click()
            self.wait.until(lambda d: d.find_element('id', 'add-project-modal').is_displayed())
            self.wait.until(lambda d: d.switch_to.active_element.get_attribute('name') == 'title')
            self.browser.find_element('css selector', selector).click()
            self.wait.until(lambda d: not d.find_element('id', 'add-project-modal').is_displayed() and not d.execute_script("return document.querySelector('main').inert"))
        self.browser.find_element('class name', 'project-add-button').click()
        self.wait.until(lambda d: d.find_element('id', 'add-project-modal').is_displayed())
        self.browser.find_element('css selector', '#project-form button[type=submit]').send_keys(Keys.TAB)
        self.assertIn('project-form-modal__close', self.browser.switch_to.active_element.get_attribute('class'))
        self.browser.switch_to.active_element.send_keys(Keys.ESCAPE)
        self.wait.until(lambda d: not d.find_element('id', 'add-project-modal').is_displayed() and not d.execute_script("return document.querySelector('main').inert"))
        self.assertFalse(self.browser.execute_script("return document.querySelector('main').inert"))
        self.browser.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 1, 'mobile': True})
        try:
            self.browser.find_element('class name', 'project-add-button').click()
            self.wait.until(lambda d: d.find_element('id', 'add-project-modal').is_displayed())
            self.assertTrue(self.browser.execute_script("""
                const box = document.querySelector('.project-form-modal__content').getBoundingClientRect();
                return box.left >= 0 && box.right <= innerWidth && box.bottom <= innerHeight;
            """))
            self.browser.find_element('css selector', '.project-form-modal__close').click()
        finally:
            self.browser.execute_cdp_cmd('Emulation.clearDeviceMetricsOverride', {})
        self.assert_no_js_errors()
