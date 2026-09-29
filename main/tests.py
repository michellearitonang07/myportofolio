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
        self.assertContains(response, 'id="grid"')
        self.assertNotIn('project_list', response.context)
        data = self.client.get('/api/projects/').json()[0]['fields']
        self.assertEqual(data['title'], self.project.title)
        self.assertEqual(data['description'], self.project.description)
        self.assertEqual(data['tech_stack'], self.project.tech_stack)

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
        data = self.client.get('/api/projects/').json()[0]['fields']
        self.assertTrue(data['is_starred'])
        self.assertEqual(data['star_count'], 1)
        self.assertEqual(data['starred_by_names'], 'reader')
        for path in ['/json/', f'/json/{self.project.pk}/']:
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
        self.assertContains(self.client.get('/projects/?title=Project'), 'value="Project"')
        self.assertEqual(self.client.get('/api/projects/?title=missing').json(), [])


class ExperienceRoleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.contrib.auth.models import Group, User
        cls.reader = User.objects.create_user('visitor')
        cls.editor = User.objects.create_user('editor-member')
        cls.editor.groups.add(Group.objects.create(name='Editor'))
        cls.owner = User.objects.create_superuser('portfolio-owner')
        cls.experience = Experience.objects.create(title='Original', description='Description', category='volunteer')
        cls.payload = {'title': 'Updated', 'description': 'New description', 'category': 'research', 'thumbnail': '', 'ended_at': ''}

    def urls(self):
        return {
            'create': reverse('main:create_experience'),
            'edit': reverse('main:edit_experience', args=[self.experience.pk]),
            'delete': reverse('main:delete_experience', args=[self.experience.pk]),
            'star': reverse('main:toggle_experience_star', args=[self.experience.pk]),
        }

    def test_anonymous_read_and_login_redirects(self):
        self.assertEqual(self.client.get('/experience/').status_code, 200)
        for action, url in self.urls().items():
            methods = ['post'] if action == 'star' else ['get', 'post']
            for method in methods:
                with self.subTest(action=action, method=method):
                    self.assertRedirects(getattr(self.client, method)(url), '/login/?next=' + url)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_reader_and_editor_forbidden_actions_do_not_change_data(self):
        for user, forbidden in [(self.reader, ['create', 'edit', 'delete']), (self.editor, ['create', 'delete'])]:
            self.client.force_login(user)
            self.assertEqual(self.client.get('/experience/').status_code, 200)
            for action in forbidden:
                for method in ['get', 'post']:
                    with self.subTest(user=user.username, action=action, method=method):
                        self.assertEqual(getattr(self.client, method)(self.urls()[action], self.payload).status_code, 403)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, 'Original')
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_and_owner_can_edit_and_validation_preserves_data(self):
        for user in [self.editor, self.owner]:
            self.client.force_login(user)
            url = self.urls()['edit']
            self.assertEqual(self.client.get(url).status_code, 200)
            self.assertRedirects(self.client.post(url, self.payload), '/experience/')
            self.experience.refresh_from_db()
            self.assertEqual(self.experience.title, 'Updated')
            response = self.client.post(url, {})
            self.assertTrue(response.context['form'].errors)
            self.experience.refresh_from_db()
            self.assertEqual(self.experience.title, 'Updated')

    def test_owner_can_create_and_delete_only_on_post(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.urls()['create']).status_code, 200)
        self.assertRedirects(self.client.post(self.urls()['create'], self.payload), '/experience/')
        self.assertEqual(Experience.objects.count(), 2)
        self.client.get(self.urls()['delete'])
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())
        self.assertRedirects(self.client.post(self.urls()['delete']), '/experience/')
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_all_authenticated_roles_can_toggle_without_duplicate_stars(self):
        for user in [self.reader, self.editor, self.owner]:
            self.client.force_login(user)
            self.assertEqual(self.client.get(self.urls()['star']).status_code, 405)
            self.assertRedirects(self.client.post(self.urls()['star']), '/experience/')
            self.assertEqual(self.experience.starred_by.count(), 1)
            self.experience.starred_by.add(user)
            self.assertEqual(self.experience.starred_by.count(), 1)
            self.assertRedirects(self.client.post(self.urls()['star']), '/experience/')
            self.assertEqual(self.experience.starred_by.count(), 0)
        self.experience.starred_by.add(self.reader, self.editor)
        self.assertEqual(self.experience.starred_by.count(), 2)

    def test_group_membership_not_username_or_staff_controls_editor_access(self):
        from django.contrib.auth.models import User
        named_editor = User.objects.create_user('Editor', is_staff=True)
        self.client.force_login(named_editor)
        self.assertEqual(self.client.get(self.urls()['edit']).status_code, 403)
        self.client.force_login(self.editor)
        self.assertEqual(self.client.get(self.urls()['edit']).status_code, 200)
        self.editor.groups.clear()
        self.assertEqual(self.client.get(self.urls()['edit']).status_code, 403)

    def test_editor_has_no_project_owner_permissions(self):
        project = Project.objects.create(title='Keep', description='Test', tech_stack='Python')
        self.client.force_login(self.editor)
        for url in ['/projects/add/', reverse('main:delete_project', args=[project.pk])]:
            self.assertEqual(self.client.get(url).status_code, 403)
            self.assertEqual(self.client.post(url).status_code, 403)
        star = reverse('main:toggle_star', args=[project.pk])
        self.assertRedirects(self.client.post(star), '/projects/')
        self.assertEqual(project.starred_by.count(), 1)
        self.client.post(star)
        self.assertEqual(project.starred_by.count(), 0)

    def test_public_experience_json_uses_usernames_and_preserves_fields(self):
        self.experience.starred_by.add(self.reader)
        for url in ['/api/experience/', f'/api/experience/{self.experience.pk}/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            fields = response.json()[0]['fields']
            self.assertEqual(fields['starred_by'], [['visitor']])
            self.assertEqual(set(fields), {'title', 'description', 'category', 'thumbnail', 'started_at', 'ended_at', 'starred_by'})

    def test_missing_objects_return_404(self):
        import uuid
        self.client.force_login(self.owner)
        for action in ['edit', 'delete', 'star']:
            url = f'/experience/{uuid.uuid4()}/{action}/'
            self.assertEqual(self.client.post(url, self.payload).status_code, 404)

    def test_csrf_required_for_every_experience_mutation(self):
        from django.conf import settings
        from django.test import Client
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', settings.MIDDLEWARE)
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        for url in self.urls().values():
            self.assertEqual(client.post(url, self.payload).status_code, 403)
        response = client.get(self.urls()['edit'])
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        token = client.cookies['csrftoken'].value
        self.assertRedirects(client.post(self.urls()['edit'], {**self.payload, 'csrfmiddlewaretoken': token}), '/experience/')
        self.assertRedirects(client.post(self.urls()['star'], {'csrfmiddlewaretoken': token}), '/experience/')

    def test_template_controls_match_each_role(self):
        for user, can_create, can_edit, can_delete in [
            (None, False, False, False), (self.reader, False, False, False),
            (self.editor, False, True, False), (self.owner, True, True, True),
        ]:
            self.client.logout()
            if user:
                self.client.force_login(user)
            response = self.client.get('/experience/')
            for action, visible in [('create', can_create), ('edit', can_edit), ('delete', can_delete)]:
                with self.subTest(user=user, action=action):
                    markup = ('action' if action == 'delete' else 'href') + '="' + self.urls()[action] + '"'
                    if visible:
                        self.assertContains(response, markup)
                    else:
                        self.assertNotContains(response, markup)
            self.assertContains(response, 'action="' + self.urls()['star'] + '"')
            self.assertContains(response, 'name="csrfmiddlewaretoken"')
            self.assertContains(response, '☆ Star')
            self.assertContains(response, '<span class="star-count">0</span>', html=True)
            if user:
                self.client.post(self.urls()['star'])
                response = self.client.get('/experience/')
                self.assertContains(response, '★ Unstar')
                self.assertContains(response, '<span class="star-count">1</span>', html=True)
                self.assertContains(response, 'aria-pressed="true"')
                self.client.post(self.urls()['star'])
                self.assertContains(self.client.get('/experience/'), '☆ Star')


class ProjectAjaxReadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.contrib.auth.models import User
        cls.reader = User.objects.create_user('ajax-reader')
        cls.other = User.objects.create_user('other-reader')
        cls.project = Project.objects.create(title='Django Portfolio', description='Details', tech_stack='Django')
        cls.project.starred_by.add(cls.reader, cls.other)

    def test_api_star_metadata_depends_on_current_user(self):
        for user, expected in [(None, False), (self.reader, True)]:
            if user:
                self.client.force_login(user)
            response = self.client.get('/api/projects/')
            item = response.json()[0]
            self.assertEqual(item['pk'], str(self.project.pk))
            fields = item['fields']
            self.assertEqual(fields['is_starred'], expected)
            self.assertEqual(fields['star_count'], 2)
            self.assertEqual(set(fields['starred_by_names'].split(', ')), {'ajax-reader', 'other-reader'})
            self.assertEqual(set(fields), {'title', 'description', 'tech_stack', 'project_url', 'star_count', 'is_starred', 'starred_by_names'})
            self.assertIn('no-store', response.headers['Cache-Control'])

    def test_search_is_trimmed_case_insensitive_and_can_be_empty(self):
        self.assertEqual(len(self.client.get('/api/projects/', {'title': ' dJaNgO '}).json()), 1)
        self.assertEqual(self.client.get('/api/projects/', {'title': 'missing'}).json(), [])
        self.assertEqual(len(self.client.get('/api/projects/', {'title': '  '}).json()), 1)

    def test_prefetch_avoids_query_per_project(self):
        from django.contrib.auth.models import AnonymousUser
        from django.test import RequestFactory
        from main.views import get_projects_json
        for number in range(5):
            project = Project.objects.create(title=f'Project {number}', description='Test', tech_stack='Python')
            project.starred_by.add(self.reader)
        request = RequestFactory().get('/api/projects/')
        request.user = AnonymousUser()
        with self.assertNumQueries(2):
            response = get_projects_json(request)
        self.assertEqual(response.status_code, 200)
