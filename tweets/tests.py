from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Tweet 

from rest_framework.test import APIClient
# Create your tests here.

User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='manoj', password='pwd')
        self.user1 = User.objects.create_user(username='manoj1', password='pwd')
        Tweet.objects.create(content='test 1 tweet', user = self.user)
        Tweet.objects.create(content='test 2 tweet', user = self.user)
        Tweet.objects.create(content='test 3 tweet', user = self.user1)
        self.current_count = Tweet.objects.all().count()
    def test_tweet_created(self):
        tweet = Tweet.objects.create(
            content='test 4 tweet', 
            user = self.user
        )
        self.assertEquals(tweet.id, 4)
        self.assertEquals(tweet.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='pwd')
        return client
       
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 3)
    
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"like"})
        self.assertEquals(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEquals(like_count, 1)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"like"})
        response = client.post("/api/tweets/action/", {"id":1, "action":"unlike"})
        self.assertEquals(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEquals(like_count, 0)
    
    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":3, "action":"retweet"})
        self.assertEquals(response.status_code, 201)
        newTweetId = response.json().get("id")
        self.assertNotEquals(2, newTweetId)
    
    def test_tweet_create_api_view(self):
        data = {"content": "Test Tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(self.current_count + 1, response.json().get("id"))

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json().get("id"), 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEquals(response.status_code, 200)
        response = client.delete("/api/tweets/1/delete/")
        self.assertEquals(response.status_code, 404)
        response = client.delete("/api/tweets/3/delete/")
        self.assertEquals(response.status_code, 401)
    
        