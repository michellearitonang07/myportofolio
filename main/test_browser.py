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

    def open_create_form(self, title='Django Created', project_url='https://example.com/'):
        self.browser.find_element('class name', 'project-add-button').click()
        self.wait.until(lambda d: d.switch_to.active_element.get_attribute('name') == 'title')
        for name, value in {'title': title, 'description': 'A new project', 'tech_stack': 'Django', 'project_url': project_url}.items():
            field = self.browser.find_element('css selector', f'#project-form [name="{name}"]')
            field.clear()
            field.send_keys(value)

    def screenshot(self, filename):
        from pathlib import Path
        directory = os.environ.get('BROWSER_SCREENSHOT_DIR')
        if directory:
            Path(directory).mkdir(parents=True, exist_ok=True)
            self.browser.save_screenshot(str(Path(directory) / filename))

    def test_ajax_create_network_csrf_toast_and_filter_without_reload(self):
        import json
        from main.models import Project
        self.seed_project('Other project')
        self.login_browser(superuser=True)
        self.open_projects('?title=Django')
        self.assertTrue(self.browser.find_element('id', 'empty').is_displayed())
        self.browser.execute_script("window.pageMarker = 'same-document'")
        self.open_create_form()
        self.screenshot('modal-desktop.png')
        self.browser.get_log('performance')
        self.browser.find_element('css selector', '#project-form button[type=submit]').click()
        self.wait.until(lambda d: not d.find_element('id', 'add-project-modal').is_displayed())
        self.wait.until(lambda d: len(d.find_elements('css selector', '#grid article')) == 1)
        self.wait.until(lambda d: d.find_element('id', 'toast-title').text == 'Berhasil')
        self.assertEqual(self.browser.execute_script('return pageMarker'), 'same-document')
        self.assertEqual(self.browser.find_element('id', 'search-input').get_attribute('value'), 'Django')
        self.assertEqual(self.browser.find_element('css selector', '#grid h2').text, 'Django Created')
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(self.browser.find_element('css selector', '#project-form [name=title]').get_attribute('value'), '')
        events = [json.loads(entry['message'])['message'] for entry in self.browser.get_log('performance')]
        requests = [event['params']['request'] for event in events if event['method'] == 'Network.requestWillBeSent']
        responses = [event['params']['response'] for event in events if event['method'] == 'Network.responseReceived']
        self.assertTrue(any(request['method'] == 'POST' and '/projects/add-ajax/' in request['url'] and
                            any(key.lower() == 'x-csrftoken' and bool(value) for key, value in request['headers'].items())
                            for request in requests))
        self.assertTrue(any('/projects/add-ajax/' in response['url'] and response['status'] == 201 for response in responses))
        self.assertTrue(any('/api/projects/?title=Django' in response['url'] and response['status'] == 200 for response in responses))
        self.screenshot('projects-success.png')
        # A created item that does not match the filter must not appear in the filtered grid.
        self.open_create_form(title='Unrelated created')
        self.browser.find_element('css selector', '#project-form button[type=submit]').click()
        self.wait.until(lambda d: not d.find_element('id', 'add-project-modal').is_displayed())
        self.wait.until(lambda d: d.find_element('id', 'project-results').get_attribute('aria-busy') == 'false')
        self.assertEqual(len(self.browser.find_elements('css selector', '#grid article')), 1)
        self.assertEqual(Project.objects.count(), 3)
        self.assert_no_js_errors()

    def test_invalid_ajax_create_keeps_modal_and_displays_server_errors(self):
        import json
        from main.models import Project
        self.login_browser(superuser=True)
        self.open_projects()
        self.open_create_form(title='   ')
        self.browser.get_log('performance')
        self.browser.find_element('css selector', '#project-form button[type=submit]').click()
        self.wait.until(lambda d: d.find_element('id', 'toast-title').text == 'Gagal menambahkan proyek')
        self.assertTrue(self.browser.find_element('id', 'add-project-modal').is_displayed())
        self.assertEqual(Project.objects.count(), 0)
        self.assertTrue(self.browser.find_element('css selector', '#project-form button[type=submit]').is_enabled())
        events = [json.loads(entry['message'])['message'] for entry in self.browser.get_log('performance')]
        self.assertTrue(any(event['method'] == 'Network.responseReceived' and
                            event['params']['response']['status'] == 400 for event in events))
        for title, url, expected in [
            ('Valid title', 'javascript:alert(1)', 'Enter a valid URL.'),
            ('<img src="x" onerror="alert(\'XSS!\')">', 'https://example.com/', 'Nama proyek tidak boleh'),
        ]:
            for name, value in [('title', title), ('project_url', url)]:
                field = self.browser.find_element('css selector', f'#project-form [name={name}]')
                field.clear()
                field.send_keys(value)
            self.browser.find_element('css selector', '#project-form button[type=submit]').click()
            self.wait.until(lambda d: expected in d.find_element('id', 'toast-message').text)
            self.assertEqual(Project.objects.count(), 0)
        self.screenshot('modal-validation.png')
        self.browser.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 1, 'mobile': True})
        try:
            self.screenshot('modal-mobile.png')
        finally:
            self.browser.execute_cdp_cmd('Emulation.clearDeviceMetricsOverride', {})
        self.assert_no_js_errors()

    def test_create_handles_duplicate_submit_html_error_offline_and_expired_session(self):
        from main.models import Project
        self.login_browser(superuser=True)
        self.open_projects()
        self.open_create_form()
        self.browser.execute_script("""
            window.originalFetch = window.fetch;
            window.createRequestCount = 0;
            window.fetch = () => { createRequestCount++; return new Promise(resolve => {window.resolveCreate = resolve;}); };
            document.getElementById('project-form').requestSubmit();
            document.getElementById('project-form').requestSubmit();
        """)
        self.assertEqual(self.browser.execute_script('return createRequestCount'), 1)
        self.assertFalse(self.browser.find_element('css selector', '#project-form button[type=submit]').is_enabled())
        self.browser.execute_script("resolveCreate({ok: false, status: 403, json: async () => {throw new Error('HTML response');}})")
        self.wait.until(lambda d: 'status 403' in d.find_element('id', 'toast-message').text)
        self.assertTrue(self.browser.find_element('css selector', '#project-form button[type=submit]').is_enabled())
        self.browser.execute_script("window.fetch = () => Promise.reject(new TypeError('Simulated offline'))")
        self.browser.find_element('css selector', '#project-form button[type=submit]').click()
        self.wait.until(lambda d: 'Tidak dapat terhubung' in d.find_element('id', 'toast-message').text)
        self.assertTrue(self.browser.find_element('css selector', '#project-form button[type=submit]').is_enabled())
        self.browser.execute_script('window.fetch = window.originalFetch')
        self.browser.delete_cookie('sessionid')
        self.browser.find_element('css selector', '#project-form button[type=submit]').click()
        self.wait.until(lambda d: 'Hanya pemilik' in d.find_element('id', 'toast-message').text)
        self.assertTrue(self.browser.find_element('id', 'add-project-modal').is_displayed())
        self.assertEqual(Project.objects.count(), 0)
        self.assert_no_js_errors()

    def test_editorial_pages_and_natural_photo_ratios_at_responsive_sizes(self):
        from pathlib import Path
        screenshot_dir = os.environ.get('BROWSER_SCREENSHOT_DIR')
        self.seed_project()
        for width, height in [(1440, 1000), (768, 1024), (390, 844)]:
            self.browser.set_window_size(width, height)
            self.browser.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height, 'deviceScaleFactor': 1, 'mobile': False})
            self.assertEqual(self.browser.execute_script('return innerWidth'), width)
            for route in ['/', '/experience/', '/projects/', '/login/', '/register/']:
                self.browser.get(self.live_server_url + route)
                if route == '/projects/':
                    self.wait.until(lambda d: d.find_element('id', 'project-results').get_attribute('aria-busy') == 'false')
                self.assertTrue(self.browser.execute_script('return document.documentElement.scrollWidth <= innerWidth'), (width, route))
                if route == '/':
                    photos = self.browser.find_elements('css selector', '.memory-image img')
                    self.assertEqual(len(photos), 11)
                    for photo in photos:
                        self.browser.execute_script("arguments[0].scrollIntoView({block:'center',behavior:'instant'})", photo)
                        self.wait.until(lambda d: d.execute_script('return arguments[0].complete && arguments[0].naturalWidth > 0', photo))
                        ratios = self.browser.execute_script('return [arguments[0].clientWidth / arguments[0].clientHeight, arguments[0].naturalWidth / arguments[0].naturalHeight]', photo)
                        self.assertAlmostEqual(*ratios, delta=.01)
                    if screenshot_dir:
                        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
                        self.browser.execute_script("document.getElementById('life').scrollIntoView({behavior:'instant'})")
                        self.browser.execute_async_script("const done=arguments[arguments.length-1]; Promise.all([...document.querySelectorAll('.memory-image img')].map(img=>img.decode())).then(()=>requestAnimationFrame(()=>requestAnimationFrame(done)))")
                        time.sleep(.2)  # Let Chrome paint decoded lazy images after scrolling.
                        self.browser.save_screenshot(str(Path(screenshot_dir) / f'gallery-{width}.png'))
                    self.browser.execute_script('window.scrollTo({top:0,behavior:"instant"})')
                if screenshot_dir:
                    Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
                    self.browser.save_screenshot(str(Path(screenshot_dir) / f'{route.strip("/") or "home"}-{width}.png'))
                self.assert_no_js_errors()
        self.browser.execute_cdp_cmd('Emulation.clearDeviceMetricsOverride', {})
        self.browser.set_window_size(1440, 1000)
