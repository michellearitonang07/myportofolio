"""Tes browser Tugas 5 dengan akun dan database sementara."""
import os
import time
from pathlib import Path
from unittest import skipUnless

from django.contrib.auth.models import Group, User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.crypto import get_random_string

from main.models import Experience


@skipUnless(os.environ.get('RUN_BROWSER_TESTS') == '1', 'Tes browser bersifat opsional')
class ExperienceBrowserTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from selenium import webdriver
        from selenium.common.exceptions import StaleElementReferenceException
        from selenium.webdriver.support.ui import WebDriverWait
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1440,1000')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        try:
            cls.browser = webdriver.Chrome(options=options)
        except Exception:
            super().tearDownClass()
            raise
        cls.wait = WebDriverWait(cls.browser, 10, ignored_exceptions=(StaleElementReferenceException,))

    @classmethod
    def tearDownClass(cls):
        try:
            cls.browser.quit()
        finally:
            super().tearDownClass()

    def setUp(self):
        self.browser.delete_all_cookies()
        self.browser.get_log('browser')
        self.experience = Experience.objects.create(title='Relawan Kampus', description='Kegiatan bersama', category='volunteer')

    def open_page(self, query=''):
        self.browser.get(self.live_server_url + '/experience/' + query)
        self.wait.until(lambda d: d.find_element('id', 'experience-results').get_attribute('aria-busy') == 'false')

    def login(self, role):
        password = get_random_string(24)
        user = User.objects.create_user(f'akun-{role}', password=password, is_superuser=role == 'owner')
        if role == 'editor':
            user.groups.add(Group.objects.get_or_create(name='Editor')[0])
        self.browser.get(self.live_server_url + '/login/')
        self.browser.find_element('name', 'username').send_keys(user.username)
        self.browser.find_element('name', 'password').send_keys(password)
        self.browser.find_element('css selector', '.project-form button[type=submit]').click()
        self.wait.until(lambda d: d.current_url == self.live_server_url + '/')
        return user

    def search(self, query):
        self.browser.execute_script("""
            document.getElementById('experience-search').value = arguments[0];
            document.getElementById('experience-search-form').requestSubmit();
        """, query)

    def assert_no_js_errors(self):
        self.assertEqual([entry for entry in self.browser.get_log('browser') if entry['source'] == 'javascript' and entry['level'] == 'SEVERE'], [])

    def screenshot(self, name):
        directory = os.environ.get('BROWSER_SCREENSHOT_DIR')
        if directory:
            Path(directory).mkdir(parents=True, exist_ok=True)
            self.browser.save_screenshot(str(Path(directory) / name))

    def test_load_search_debounce_without_reload(self):
        Experience.objects.create(title='Penelitian', description='Analisis', category='research')
        self.open_page()
        self.assertEqual(len(self.browser.find_elements('css selector', '#experience-grid article')), 2)
        self.browser.execute_script("""
            window.pageMarker='tetap'; window.calls=[]; window.realFetch=fetch;
            window.fetch=(...args)=>{calls.push(String(args[0])); return realFetch(...args);};
            const input=document.getElementById('experience-search');
            for(const value of ['r','rela','relawan']) {input.value=value; input.dispatchEvent(new Event('input'));}
        """)
        self.assertEqual(self.browser.execute_script('return calls.length'), 0)
        self.wait.until(lambda d: len(d.find_elements('css selector', '#experience-grid article')) == 1)
        self.assertEqual(self.browser.execute_script('return calls.length'), 1)
        self.search('tidak ada')
        self.wait.until(lambda d: d.find_element('id', 'experience-empty').is_displayed())
        self.assertIn('judul tersebut', self.browser.find_element('id', 'experience-empty').text)
        self.search('')
        self.wait.until(lambda d: len(d.find_elements('css selector', '#experience-grid article')) == 2)
        self.assertEqual(self.browser.execute_script('return pageMarker'), 'tetap')
        self.assert_no_js_errors()

    def test_error_retry_malformed_and_stale_responses(self):
        self.open_page()
        self.browser.execute_script('window.realFetch=fetch')
        for response in ['Promise.reject(new TypeError("offline"))',
                         'Promise.resolve({ok:false,status:503})',
                         'Promise.resolve({ok:true,json:async()=>{throw new Error("html")}})',
                         'Promise.resolve({ok:true,json:async()=>[{pk:"salah",fields:{}}]})']:
            self.browser.execute_script('window.fetch=()=> ' + response)
            self.search('')
            self.wait.until(lambda d: d.find_element('id', 'experience-error').is_displayed())
            self.wait.until(lambda d: d.find_element('id', 'toast-title').text == 'Gagal memuat pengalaman')
            self.browser.execute_script('window.fetch=realFetch')
            self.browser.find_element('id', 'retry-experience').click()
            self.wait.until(lambda d: d.find_element('id', 'experience-grid').is_displayed())
        self.browser.execute_script('window.pending=[]; window.fetch=()=>new Promise(resolve=>pending.push(resolve))')
        self.search('lama')
        self.assertTrue(self.browser.find_element('id', 'experience-loading').is_displayed())
        self.search('baru')
        self.browser.execute_script('pending[1]({ok:true,json:async()=>[]})')
        self.wait.until(lambda d: d.find_element('id', 'experience-empty').is_displayed())
        self.browser.execute_script('pending[0]({ok:false,status:500})')
        time.sleep(.2)
        self.assertTrue(self.browser.find_element('id', 'experience-empty').is_displayed())
        self.assert_no_js_errors()

    def test_stored_xss_and_unsafe_thumbnail_are_harmless(self):
        payload = '<img src="x" onerror="alert(\'XSS!\')">'
        self.experience.title = payload
        self.experience.description = payload
        self.experience.category = payload
        self.experience.thumbnail = 'javascript:alert(1)'
        self.experience.save()
        self.open_page()
        self.assertEqual(self.browser.find_element('css selector', '#experience-grid h2').text, payload)
        self.assertEqual(self.browser.find_elements('css selector', '#experience-grid img, #experience-grid script'), [])
        self.assertEqual(self.browser.find_element('css selector', '.experience-category').text, payload.upper())
        self.assert_no_js_errors()

    def test_roles_star_edit_delete_and_authenticated_refresh(self):
        self.open_page()
        self.assertEqual(self.browser.find_elements('css selector', '.experience-edit, .experience-delete-form'), [])
        self.browser.find_element('css selector', '#experience-grid .button-star').click()
        self.wait.until(lambda d: '/login/?next=' in d.current_url)
        for role in ['reader', 'editor', 'owner']:
            self.login(role)
            self.open_page()
            self.assertEqual(bool(self.browser.find_elements('css selector', '.experience-edit')), role != 'reader')
            self.assertEqual(bool(self.browser.find_elements('css selector', '.experience-delete-form')), role == 'owner')
            self.browser.find_element('css selector', '#experience-grid .button-star').click()
            self.wait.until(lambda d: d.find_element('css selector', '#experience-grid .button-star').get_attribute('aria-pressed') == 'true')
            self.search('Kampus')
            self.wait.until(lambda d: d.find_element('id', 'experience-results').get_attribute('aria-busy') == 'false')
            self.assertEqual(self.browser.find_element('css selector', '#experience-grid .star-count').text, '1')
            self.browser.find_element('css selector', '#experience-grid .button-star').click()
            self.wait.until(lambda d: d.find_element('css selector', '#experience-grid .star-count').text == '0')
            if role == 'editor':
                self.browser.find_element('css selector', '.experience-edit').click()
                title = self.browser.find_element('name', 'title')
                title.clear()
                title.send_keys('Relawan Kampus Diperbarui')
                submit = self.browser.find_element('css selector', '.project-form button[type=submit]')
                self.browser.execute_script("arguments[0].scrollIntoView({block:'center',behavior:'instant'})", submit)
                submit.click()
                self.wait.until(lambda d: 'Diperbarui' in d.find_element('css selector', '#experience-grid h2').text)
            if role == 'owner':
                self.browser.find_element('css selector', '.experience-delete-form button').click()
                self.browser.switch_to.alert.dismiss()
                self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())
                self.browser.find_element('css selector', '.experience-delete-form button').click()
                self.browser.switch_to.alert.accept()
                self.wait.until(lambda d: d.find_element('id', 'experience-empty').is_displayed())
                self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())
            self.browser.find_element('css selector', '.logout-form button').click()
            self.wait.until(lambda d: not d.find_elements('css selector', '.nav-user'))
        self.assert_no_js_errors()
