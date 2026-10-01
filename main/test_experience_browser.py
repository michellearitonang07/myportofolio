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

    def open_modal(self, title='Penelitian Baru'):
        self.browser.find_element('class name', 'experience-add-button').click()
        self.wait.until(lambda d: d.switch_to.active_element.get_attribute('name') == 'title')
        for name, value in [('title', title), ('description', 'Kegiatan penelitian bersama')]:
            field = self.browser.find_element('css selector', f'#experience-form [name={name}]')
            field.clear()
            field.send_keys(value)

    def submit_modal(self):
        button = self.browser.find_element('css selector', '#experience-form button[type=submit]')
        self.browser.execute_script("arguments[0].scrollIntoView({block:'center',behavior:'instant'})", button)
        button.click()

    def test_create_modal_refresh_csrf_toast_and_filter_without_reload(self):
        self.login('owner')
        self.open_page('?title=Penelitian')
        self.browser.execute_script("""
            window.pageMarker='tetap'; window.realFetch=fetch; window.postInfo=[];
            window.fetch=async (...args)=>{
                const response=await realFetch(...args);
                if(args[1]?.method==='POST') postInfo.push({status:response.status,csrf:!!args[1].body.get('csrfmiddlewaretoken')});
                return response;
            };
        """)
        self.open_modal()
        self.screenshot('experience-modal-desktop.png')
        self.submit_modal()
        self.wait.until(lambda d: not d.find_element('id', 'add-experience-modal').is_displayed())
        self.wait.until(lambda d: len(d.find_elements('css selector', '#experience-grid article')) == 1)
        self.wait.until(lambda d: d.find_element('id', 'toast-title').text == 'Berhasil')
        self.assertEqual(self.browser.execute_script('return pageMarker'), 'tetap')
        self.assertEqual(self.browser.execute_script('return postInfo'), [{'status': 201, 'csrf': True}])
        self.assertEqual(self.browser.find_element('id', 'experience-search').get_attribute('value'), 'Penelitian')
        self.assertEqual(self.browser.find_element('css selector', '#experience-grid h2').text, 'Penelitian Baru')
        self.assertEqual(self.browser.find_element('css selector', '#experience-form [name=title]').get_attribute('value'), '')
        self.assertEqual(Experience.objects.count(), 2)
        self.open_modal('Tidak sesuai filter')
        self.submit_modal()
        self.wait.until(lambda d: not d.find_element('id', 'add-experience-modal').is_displayed())
        self.wait.until(lambda d: d.find_element('id', 'experience-results').get_attribute('aria-busy') == 'false')
        self.assertEqual(len(self.browser.find_elements('css selector', '#experience-grid article')), 1)
        self.assertEqual(Experience.objects.count(), 3)
        self.assert_no_js_errors()

    def test_modal_validation_preserves_input_and_renders_errors_as_text(self):
        self.login('owner')
        self.open_page()
        payload = '<img src="x" onerror="alert(\'XSS!\')">'
        self.open_modal(payload)
        self.submit_modal()
        self.wait.until(lambda d: d.find_element('id', 'id_title').get_attribute('aria-invalid') == 'true')
        self.assertTrue(self.browser.find_element('id', 'add-experience-modal').is_displayed())
        self.assertEqual(self.browser.find_element('id', 'id_title').get_attribute('value'), payload)
        self.assertIn('tag HTML', self.browser.find_element('id', 'id_title_errors').text)
        self.wait.until(lambda d: 'tag HTML' in d.find_element('id', 'toast-message').text)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(self.browser.find_elements('css selector', '#experience-form img'), [])
        self.browser.execute_script("""
            window.realFetch=fetch;
            window.fetch=async()=>({status:400,json:async()=>({errors:{description:[{message:'<img src=x onerror=alert(1)>'}]}})});
        """)
        self.submit_modal()
        self.wait.until(lambda d: '<img' in d.find_element('id', 'id_description_errors').text)
        self.assertEqual(self.browser.find_elements('css selector', '#experience-form-errors img, #id_description_errors img, #toast-message img'), [])
        self.browser.execute_script('window.fetch=realFetch')
        self.browser.find_element('id', 'id_title').clear()
        self.browser.find_element('id', 'id_title').send_keys('Judul diperbaiki')
        self.submit_modal()
        self.wait.until(lambda d: not d.find_element('id', 'add-experience-modal').is_displayed())
        self.assertEqual(Experience.objects.count(), 2)
        self.assert_no_js_errors()

    def test_duplicate_submit_network_html_and_expired_session(self):
        self.login('owner')
        self.open_page()
        self.open_modal()
        self.browser.execute_script("""
            window.realFetch=fetch; window.postCount=0;
            window.fetch=()=>{postCount++; return new Promise(resolve=>window.finish=resolve);};
            const form=document.getElementById('experience-form');
            form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));
            form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));
        """)
        self.assertEqual(self.browser.execute_script('return postCount'), 1)
        self.assertFalse(self.browser.find_element('css selector', '#experience-form button[type=submit]').is_enabled())
        self.browser.execute_script('finish({status:500,json:async()=>{throw new Error("HTML")}})')
        self.wait.until(lambda d: 'Respons server' in d.find_element('id', 'experience-form-errors').text)
        self.assertTrue(self.browser.find_element('id', 'add-experience-modal').is_displayed())
        self.browser.execute_script('window.fetch=()=>Promise.reject(new TypeError("offline"))')
        self.submit_modal()
        self.wait.until(lambda d: 'Koneksi terputus' in d.find_element('id', 'experience-form-errors').text)
        self.assertEqual(self.browser.find_element('id', 'id_title').get_attribute('value'), 'Penelitian Baru')
        self.browser.execute_script('window.fetch=realFetch')
        self.browser.delete_cookie('sessionid')
        self.submit_modal()
        self.wait.until(lambda d: 'akun yang berhak' in d.find_element('id', 'experience-form-errors').text)
        self.assertEqual(Experience.objects.count(), 1)
        self.assert_no_js_errors()

    def test_modal_keyboard_responsive_and_reduced_motion(self):
        from selenium.webdriver.common.keys import Keys
        self.login('owner')
        for width, height in [(1440, 1000), (768, 1024), (390, 844)]:
            self.browser.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height, 'deviceScaleFactor': 1, 'mobile': False})
            try:
                self.open_page()
                self.assertTrue(self.browser.execute_script('return document.documentElement.scrollWidth <= innerWidth'))
                self.screenshot(f'experience-{width}.png')
                self.open_modal()
                self.assertTrue(self.browser.execute_script("return document.querySelector('main').inert"))
                self.assertTrue(self.browser.execute_script("""
                    const box=document.querySelector('#add-experience-modal .project-form-modal__content').getBoundingClientRect();
                    return box.left >= 0 && box.right <= innerWidth && box.bottom <= innerHeight;
                """))
                self.screenshot(f'experience-modal-{width}.png')
                self.browser.find_element('css selector', '#experience-form button[type=submit]').send_keys(Keys.TAB)
                self.assertIn('project-form-modal__close', self.browser.switch_to.active_element.get_attribute('class'))
                self.browser.switch_to.active_element.send_keys(Keys.SHIFT, Keys.TAB)
                self.assertEqual(self.browser.switch_to.active_element.get_attribute('type'), 'submit')
                self.browser.switch_to.active_element.send_keys(Keys.ESCAPE)
                self.wait.until(lambda d: not d.find_element('id', 'add-experience-modal').is_displayed())
                self.wait.until(lambda d: d.switch_to.active_element.get_attribute('class').endswith('experience-add-button'))
                self.assertFalse(self.browser.execute_script("return document.querySelector('main').inert"))
            finally:
                self.browser.execute_cdp_cmd('Emulation.clearDeviceMetricsOverride', {})
        self.browser.execute_cdp_cmd('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce'}]})
        try:
            self.open_page()
            self.assertEqual(self.browser.execute_script("return getComputedStyle(document.querySelector('.experience-add-button')).transitionDuration"), '0s')
        finally:
            self.browser.execute_cdp_cmd('Emulation.setEmulatedMedia', {'features': []})
        self.assert_no_js_errors()
