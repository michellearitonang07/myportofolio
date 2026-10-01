"""Pengujian Tugas 5 memakai database tes, bukan data portofolio lokal."""
from django.contrib.auth.models import Group, User, AnonymousUser
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from main.models import Experience
from main.views import get_experiences_ajax


class ExperienceAjaxTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create_user('pembaca-ajax')
        cls.editor = User.objects.create_user('editor-ajax')
        cls.editor.groups.add(Group.objects.create(name='Editor'))
        cls.owner = User.objects.create_superuser('pemilik-ajax')
        cls.experience = Experience.objects.create(title='Relawan Kampus', description='Kegiatan bersama', category='volunteer')
        cls.experience.starred_by.add(cls.reader, cls.editor)
        cls.payload = {'title': 'Pengalaman baru', 'description': 'Deskripsi baru', 'category': 'research', 'thumbnail': '', 'ended_at': ''}
        cls.read_url = reverse('main:get_experiences_ajax')
        cls.create_url = reverse('main:create_experience_ajax')

    def test_public_contract_and_star_status_for_all_roles(self):
        for user in [None, self.reader, self.editor, self.owner]:
            self.client.logout()
            if user:
                self.client.force_login(user)
            response = self.client.get(self.read_url)
            self.assertEqual(response.status_code, 200)
            self.assertIn('no-store', response.headers['Cache-Control'])
            item = response.json()[0]
            self.assertEqual(item['pk'], str(self.experience.pk))
            fields = item['fields']
            self.assertEqual(set(fields), {'title', 'description', 'category', 'category_label', 'thumbnail', 'started_at', 'ended_at', 'is_ongoing', 'star_count', 'is_starred'})
            self.assertEqual(fields['star_count'], 2)
            self.assertEqual(fields['is_starred'], user in [self.reader, self.editor])
            self.assertEqual(fields['category_label'], 'Relawan')
            self.assertTrue(fields['is_ongoing'])
            self.assertIsNone(fields['ended_at'])
            self.assertNotContains(response, self.reader.username)
        self.experience.ended_at = timezone.now()
        self.experience.save()
        fields = self.client.get(self.read_url).json()[0]['fields']
        self.assertFalse(fields['is_ongoing'])
        self.assertEqual(fields['ended_at'], self.experience.ended_at.isoformat())

    def test_search_is_trimmed_case_insensitive_and_empty_safe(self):
        for query, count in [(' kAmPuS ', 1), ('   ', 1), ('tidak ada', 0)]:
            self.assertEqual(len(self.client.get(self.read_url, {'title': query}).json()), count)
        Experience.objects.all().delete()
        self.assertEqual(self.client.get(self.read_url).json(), [])

    def test_star_metadata_has_no_query_per_card(self):
        for number in range(5):
            Experience.objects.create(title=str(number), description='Tes')
        request = RequestFactory().get(self.read_url)
        for user in [AnonymousUser(), self.reader]:
            request.user = user
            with self.assertNumQueries(1):
                self.assertEqual(get_experiences_ajax(request).status_code, 200)

    def test_create_permissions_and_methods(self):
        for user in [None, self.reader, self.editor, self.owner]:
            self.client.logout()
            if user:
                self.client.force_login(user)
            self.assertEqual(self.client.get(self.create_url).status_code, 405)
            before = Experience.objects.count()
            response = self.client.post(self.create_url, self.payload)
            allowed = user == self.owner
            self.assertEqual(response.status_code, 201 if allowed else 403)
            self.assertEqual(Experience.objects.count(), before + int(allowed))
            self.assertIn('message', response.json())
            if allowed:
                self.assertEqual(Experience.objects.get(pk=response.json()['pk']).title, self.payload['title'])

    def test_invalid_input_and_xss_return_indonesian_field_errors(self):
        self.client.force_login(self.owner)
        cases = [('title', ''), ('title', ' '), ('title', 'x' * 256),
                 ('title', '<img src="x" onerror="alert(\'XSS!\')">'),
                 ('description', '<p></p>'), ('category', 'invalid'),
                 ('thumbnail', 'javascript:alert(1)'), ('thumbnail', 'ftp://example.com/x'),
                 ('thumbnail', 'data:text/html,<script>alert(1)</script>'), ('ended_at', 'bukan tanggal')]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                response = self.client.post(self.create_url, {**self.payload, field: value})
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json()['errors'])
                self.assertNotIn('This field is required', response.content.decode())
                self.assertNotIn('Enter a valid', response.content.decode())
        self.assertEqual(Experience.objects.count(), 1)

    def test_sanitization_is_shared_with_legacy_create_and_editor_edit(self):
        clean_payload = {**self.payload, 'title': ' <b>Judul</b> ', 'description': '<p>Isi</p>'}
        self.client.force_login(self.owner)
        for url, status in [(self.create_url, 201), (reverse('main:create_experience'), 302)]:
            response = self.client.post(url, clean_payload)
            self.assertEqual(response.status_code, status)
        self.client.force_login(self.editor)
        response = self.client.post(reverse('main:edit_experience', args=[self.experience.pk]), clean_payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Experience.objects.filter(title='Judul', description='Isi').count(), 3)

    def test_csrf_is_required_and_masked_form_token_is_valid(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        response = client.get(reverse('main:create_experience'))
        self.assertEqual(client.post(self.create_url, self.payload).status_code, 403)
        self.assertEqual(client.post(self.create_url, self.payload, HTTP_X_CSRFTOKEN='invalid').status_code, 403)
        from django.middleware.csrf import get_token
        token = get_token(response.wsgi_request)
        response = client.post(self.create_url, {**self.payload, 'csrfmiddlewaretoken': token})
        self.assertEqual(response.status_code, 201)

    def test_legacy_endpoints_keep_serializer_fields(self):
        for url in ['/api/experience/', f'/api/experience/{self.experience.pk}/']:
            item = self.client.get(url).json()[0]
            self.assertEqual(item['model'], 'main.experience')
            self.assertEqual(item['fields']['starred_by'], [[self.reader.username], [self.editor.username]])
            self.assertNotIn('star_count', item['fields'])

    def test_page_is_a_shell_and_modal_matches_creation_permissions(self):
        for user in [None, self.reader, self.editor, self.owner]:
            self.client.logout()
            if user:
                self.client.force_login(user)
            response = self.client.get('/experience/')
            self.assertNotIn('experience_list', response.context)
            self.assertNotContains(response, self.experience.title)
            self.assertContains(response, 'id="experience-grid"')
            if user == self.owner:
                self.assertContains(response, 'id="add-experience-modal"')
                self.assertContains(response, 'action="/experience/add/"')
                self.assertContains(response, 'id="experience-form"')
            else:
                self.assertNotContains(response, 'id="add-experience-modal"')
                self.assertNotContains(response, 'id="experience-form"')
