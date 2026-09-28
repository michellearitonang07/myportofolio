from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Project

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Staff Academic Event Rumbel BEM UI",
            description="Menjadi PIC untuk proyek Educator 101 dan SAYONARA.",
            category="volunteer",
        )
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="Website portofolio dengan Django",
            tech_stack="Django, HTML, CSS",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Staff Academic Event Rumbel BEM UI")
        self.assertEqual(self.experience.category, "volunteer")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Volunteer")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_project_model(self):
        self.assertEqual(str(self.project), "Portfolio Website")

    def test_projects_page_with_data(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.tech_stack)

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

class TutorialAuthTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.contrib.auth.models import User
        from django.utils.crypto import get_random_string
        cls.password = get_random_string(24)
        cls.user = User.objects.create_user('reader', password=cls.password)
        cls.owner = User.objects.create_superuser('owner', password=cls.password)
        cls.project = Project.objects.create(title='Project', description='Test', tech_stack='Django')

    def test_registration_hashes_password_without_login_or_privileges(self):
        from django.contrib.auth.models import User
        response = self.client.post('/register/', {
            'username': 'new-reader', 'password1': self.password,
            'password2': self.password,
        }, follow=True)
        self.assertRedirects(response, '/login/')
        self.assertContains(response, 'Akun berhasil dibuat')
        user = User.objects.get(username='new-reader')
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertFalse(user.is_staff or user.is_superuser or user.groups.exists())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_registration_and_login_render_errors(self):
        for path in ['/register/', '/login/']:
            response = self.client.post(path, {})
            self.assertTrue(response.context['form'].errors)
            self.assertContains(response, 'This field is required.')
        response = self.client.post('/register/', {
            'username': 'reader', 'password1': self.password, 'password2': 'different',
        })
        self.assertIn('username', response.context['form'].errors)
        self.assertIn('password2', response.context['form'].errors)
        response = self.client.post('/login/', {'username': 'reader', 'password': 'wrong'})
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_session_cookie_navbar_and_post_logout(self):
        from django.contrib.auth.models import User
        from django.contrib.sessions.models import Session
        response = self.client.get('/')
        self.assertContains(response, 'Belum ada sesi login')
        self.assertContains(response, 'href="/register/"')
        response = self.client.post('/login/', {'username': 'reader', 'password': self.password})
        self.assertRedirects(response, '/')
        self.assertIn('sessionid', response.cookies)
        timestamp = response.cookies['last_login'].value
        self.assertRegex(timestamp, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
        self.assertContains(self.client.get('/'), timestamp)
        for path in ['/experience/', '/projects/']:
            response = self.client.get(path)
            self.assertContains(response, '<span class="nav-user">reader</span>', html=True)
            self.assertContains(response, 'class="logout-form"')
            self.assertNotContains(response, 'href="/register/"')
        self.assertEqual(self.client.get('/logout/').status_code, 405)
        session_key = self.client.session.session_key
        response = self.client.post('/logout/')
        self.assertRedirects(response, '/')
        self.assertEqual(response.cookies['last_login']['max-age'], 0)
        self.assertFalse(Session.objects.filter(session_key=session_key).exists())
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
        self.client.cookies.pop('last_login', None)
        self.assertContains(self.client.get('/'), 'Belum ada sesi login')

    def test_project_permissions_and_controls(self):
        delete_url = reverse('main:delete_project', args=[self.project.pk])
        for path in ['/projects/add/', delete_url]:
            for method in ['get', 'post']:
                self.assertRedirects(getattr(self.client, method)(path), '/login/?next=' + path)
        self.client.force_login(self.user)
        for path in ['/projects/add/', delete_url]:
            for method in ['get', 'post']:
                self.assertEqual(getattr(self.client, method)(path).status_code, 403)
        response = self.client.get('/projects/')
        self.assertNotContains(response, 'href="/projects/add/"')
        self.assertNotContains(response, 'action="' + delete_url + '"')
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get('/projects/add/').status_code, 200)
        response = self.client.post('/projects/add/', {'title': 'New', 'description': 'New', 'tech_stack': 'Python'})
        self.assertRedirects(response, '/projects/')
        self.assertTrue(Project.objects.filter(title='New').exists())
        response = self.client.post('/projects/add/', {})
        self.assertContains(response, 'This field is required.')
        self.client.get(delete_url)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
        response = self.client.post(delete_url)
        self.assertRedirects(response, '/projects/')
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_project_star_and_safe_legacy_api(self):
        url = reverse('main:toggle_star', args=[self.project.pk])
        self.assertRedirects(self.client.post(url), '/login/?next=' + url)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertRedirects(self.client.post(url), '/projects/')
        self.assertEqual(self.project.starred_by.count(), 1)
        self.assertContains(self.client.get('/projects/'), 'Unstar')
        for path in ['/api/projects/', '/json/', f'/json/{self.project.pk}/']:
            fields = self.client.get(path).json()[0]['fields']
            self.assertEqual(fields['starred_by'], [['reader']])
            self.assertEqual(set(fields), {'title', 'description', 'tech_stack', 'project_url', 'starred_by'})
        for path in ['/xml/', f'/xml/{self.project.pk}/']:
            response = self.client.get(path)
            self.assertContains(response, '<natural>reader</natural>')
        self.client.post(url)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_csrf_rejects_missing_tokens_and_accepts_valid_forms(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        for path in ['/login/', '/register/']:
            self.assertContains(client.get(path), 'name="csrfmiddlewaretoken"')
            self.assertEqual(client.post(path, {}).status_code, 403)
        token = client.cookies['csrftoken'].value
        response = client.post('/login/', {'username': 'reader', 'password': self.password,
                                          'csrfmiddlewaretoken': token})
        self.assertRedirects(response, '/')
        star_url = reverse('main:toggle_star', args=[self.project.pk])
        self.assertEqual(client.post(star_url).status_code, 403)
        self.assertEqual(client.post('/logout/').status_code, 403)
        token = client.cookies['csrftoken'].value
        self.assertRedirects(client.post(star_url, {'csrfmiddlewaretoken': token}), '/projects/')
        self.assertRedirects(client.post('/logout/', {'csrfmiddlewaretoken': token}), '/')
        client.force_login(self.owner)
        for path in ['/projects/add/', reverse('main:delete_project', args=[self.project.pk])]:
            self.assertEqual(client.post(path).status_code, 403)

    def test_public_pages_search_and_static_discovery(self):
        from django.contrib.staticfiles import finders
        for path in ['/', '/login/', '/register/', '/experience/', '/projects/', '/api/experience/', '/api/projects/']:
            self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.client.get('/admin/').status_code, 302)
        self.assertIsNotNone(finders.find('css/style.css'))
        self.assertContains(self.client.get('/'), '/static/css/style.css')
        self.assertContains(self.client.get('/projects/?title=Project'), self.project.title)
        self.assertEqual(self.client.get('/api/projects/?title=missing').json(), [])
