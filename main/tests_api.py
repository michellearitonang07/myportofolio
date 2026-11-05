import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password"
        )
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django"
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project",
            "description": "A useful app",
            "tech_stack": "Python",
            "project_url": "https://example.com/",
            "project_image_url": "https://example.com/image.jpg",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertIn("project_image_url", response.data[0])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.project.starred_by.add(self.visitor)
        self.client.force_authenticate(user=self.visitor)
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
        self.assertTrue(response.data[0]["is_starred"])
        self.assertEqual(response.data[0]["starred_by_names"], "visitor")

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(
            self.client.get(url).status_code, status.HTTP_404_NOT_FOUND
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(
                self.client.post(self.list_url, self.payload, format="json").status_code,
                status.HTTP_403_FORBIDDEN,
            )
            self.assertEqual(
                self.client.patch(
                    self.detail_url, {"title": "Changed"}, format="json"
                ).status_code,
                status.HTTP_403_FORBIDDEN,
            )
            self.assertEqual(
                self.client.delete(self.detail_url).status_code,
                status.HTTP_403_FORBIDDEN,
            )
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
            ({"project_image_url": "javascript:alert(1)"}, "project_image_url"),
        ]:
            response = self.client.post(
                self.list_url, {**self.payload, **changes}, format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url, {"title": "Changed"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(
            self.detail_url, {"title": "Incomplete"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(
            self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN
        )
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "id": forged_id,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(
            self.client.patch(
                self.detail_url, {"title": "Changed"}, format="json"
            ).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.post(self.detail_url, self.payload, format="json").status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="experience-owner", password="test-password"
        )
        self.visitor = User.objects.create_user(
            username="experience-reader", password="test-password"
        )
        self.editor = User.objects.create_user(
            username="experience-editor", password="test-password"
        )
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.experience = Experience.objects.create(
            title="Research role", description="Built a project", category="research"
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail", args=[self.experience.id]
        )
        self.star_url = reverse(
            "api:experience-star", args=[self.experience.id]
        )
        self.payload = {
            "title": "Community role",
            "description": "Organized a learning program",
            "category": "volunteer",
            "thumbnail": "https://example.com/experience.jpg",
            "ended_at": None,
        }

    def database_snapshot(self):
        experiences = tuple(
            Experience.objects.order_by("pk").values_list(
                "pk", "title", "description", "category", "thumbnail", "ended_at"
            )
        )
        stars = tuple(
            Experience.starred_by.through.objects.order_by(
                "experience_id", "user_id"
            ).values_list("experience_id", "user_id")
        )
        return experiences, stars

    def test_public_experience_list_detail_and_search(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertEqual(response.data[0]["category_label"], "Penelitian")
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(
            self.client.get(self.detail_url).status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            len(self.client.get(self.list_url, {"title": "RESEARCH"}).data), 1
        )
        self.assertEqual(
            self.client.get(self.list_url, {"title": " research "}).data[0]["id"],
            str(self.experience.id),
        )
        self.assertEqual(
            self.client.get(self.list_url, {"title": "missing"}).data, []
        )
        self.experience.delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_serializer_fields_are_explicit_and_star_data_is_computed(self):
        self.experience.starred_by.add(self.visitor)
        expected_fields = {
            "id", "title", "description", "category", "category_label", "thumbnail",
            "started_at", "ended_at", "is_ongoing", "star_count", "is_starred",
            "starred_by_names",
        }
        for user, starred in (
            (None, False),
            (self.visitor, True),
            (self.editor, False),
            (self.owner, False),
        ):
            self.client.force_authenticate(user=user)
            response = self.client.get(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(set(response.data), expected_fields)
            self.assertEqual(response.data["star_count"], 1)
            self.assertEqual(response.data["is_starred"], starred)
            self.assertEqual(response.data["starred_by_names"], self.visitor.username)
            self.assertFalse({"email", "password", "password_hash"}.intersection(response.data))

    def test_guest_and_regular_user_cannot_mutate_and_database_stays_unchanged(self):
        requests = (
            ("post", self.list_url, self.payload),
            ("put", self.detail_url, self.payload),
            ("patch", self.detail_url, {"title": "Not allowed"}),
            ("delete", self.detail_url, None),
        )
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            for method, url, payload in requests:
                before = self.database_snapshot()
                request = getattr(self.client, method)
                response = request(url) if payload is None else request(url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertEqual(self.database_snapshot(), before)

    def test_staff_without_editor_group_cannot_update(self):
        self.visitor.is_staff = True
        self.visitor.save(update_fields=["is_staff"])
        self.client.force_authenticate(user=self.visitor)
        before = self.database_snapshot()
        response = self.client.patch(
            self.detail_url, {"title": "Staff is not Editor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.database_snapshot(), before)

    def test_editor_can_put_and_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, self.payload["title"])
        self.assertEqual(self.experience.category, self.payload["category"])

        response = self.client.patch(
            self.detail_url, {"title": "Updated by Editor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated by Editor")

        before = self.database_snapshot()
        response = self.client.patch(
            self.detail_url, {"description": "<p></p>"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.database_snapshot(), before)

        for method, url, payload in (
            ("post", self.list_url, self.payload),
            ("delete", self.detail_url, None),
        ):
            before = self.database_snapshot()
            request = getattr(self.client, method)
            response = request(url, payload, format="json") if payload else request(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.database_snapshot(), before)

    def test_superuser_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_id = response.data["id"]
        created_url = reverse("api:experience-detail", args=[created_id])

        response = self.client.put(
            created_url,
            {**self.payload, "title": "Owner full update"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Owner full update")
        response = self.client.patch(
            created_url, {"description": "Owner partial update"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Owner partial update")

        response = self.client.delete(created_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=created_id).exists())

    def test_experience_star_requires_login_and_toggles(self):
        before = self.database_snapshot()
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.database_snapshot(), before)
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])
            self.assertEqual(response.data["star_count"], 1)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertFalse(response.data["is_starred"])
            self.assertEqual(response.data["star_count"], 0)

    def test_validation_strips_text_and_rejects_empty_or_invalid_values(self):
        self.client.force_authenticate(user=self.owner)
        invalid_values = (
            ({"title": " "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"title": "x" * 256}, "title"),
            ({"description": "<p></p>"}, "description"),
            ({"description": "<script></script>"}, "description"),
            ({"category": "not-a-category"}, "category"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"ended_at": "not-a-datetime"}, "ended_at"),
        )
        for changes, field in invalid_values:
            with self.subTest(field=field, value=changes[field]):
                before = self.database_snapshot()
                response = self.client.post(
                    self.list_url, {**self.payload, **changes}, format="json"
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
                self.assertEqual(self.database_snapshot(), before)

        response = self.client.post(
            self.list_url,
            {**self.payload, "title": "<b>Community</b>", "description": "<p>Service</p>"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Community")
        self.assertEqual(response.data["description"], "Service")

    def test_read_only_and_computed_fields_ignore_client_values(self):
        self.client.force_authenticate(user=self.owner)
        submitted_id = str(uuid.uuid4())
        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "id": submitted_id,
                "started_at": "2000-01-01T00:00:00Z",
                "is_ongoing": False,
                "category_label": "Fake category",
                "star_count": 999,
                "is_starred": True,
                "starred_by_names": "attacker",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], submitted_id)
        self.assertTrue(response.data["is_ongoing"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        created = Experience.objects.get(pk=response.data["id"])
        self.assertGreater(created.started_at.year, 2000)

        response = self.client.patch(
            self.detail_url,
            {"title": "Updated", "star_count": 100, "is_starred": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_csrf_protects_session_authenticated_experience_updates(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            client.login(username="experience-editor", password="test-password")
        )
        client.get(reverse("main:show_experience"))
        token = client.cookies["csrftoken"].value
        before = self.database_snapshot()

        response = client.patch(
            self.detail_url, {"title": "Missing CSRF"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.database_snapshot(), before)

        response = client.patch(
            self.detail_url,
            {"title": "CSRF accepted"},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "CSRF accepted")

    def test_missing_experience_and_unsupported_methods(self):
        missing_url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing_url).status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
