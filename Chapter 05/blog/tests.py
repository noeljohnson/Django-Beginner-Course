from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse
# Create your tests here.

class BlogTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.user = get_user_model().objects.create_user(
      username = "test_user",
      email = "test@email.com",
      password = "secret"
    )

    cls.post = Post.objects.create(
      title = "A good title",
      body = "A nice body",
      author = cls.user
    )

  def test_post_model(self):
    self.assertEqual(self.post.title, "A good title")
    self.assertEqual(self.post.body, "A nice body")
    self.assertEqual(self.post.author.username, "test_user")
    self.assertEqual(str(self.post), "A good title")
    self.assertEqual(self.post.get_absolute_url(), "/post/1")

  def test_url_at_correct_location_list_view(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)

  def test_url_at_correct_location_detail_view(self):
    response = self.client.get("/post/1")
    self.assertEqual(response.status_code, 200)

  def test_post_list_view(self):
    response = self.client.get(reverse("home"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "A nice body")
    self.assertTemplateUsed(response, "home.html")

  def test_post_detail_view(self):
    response = self.client.get(reverse("post_detail", kwargs={"pk":self.post.pk}))
    no_response = self.client.get("/post/1000/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(no_response.status_code, 404)
    self.assertContains(response, "A good title")
    self.assertTemplateUsed(response, "post_detail.html")
