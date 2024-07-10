from django.test import TestCase
from .models import Monetization
from utils.Ideas import IdeaManager
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()

class MonetizeTests(TestCase):

    def setUp(self):
        self.manager = IdeaManager()
        self.user = User.objects.create_user(
            uid='testuid',
            email='testuser@example.com',
            name='Test User',
            password='testpass'
        )
        self.user.is_active = True
        
        
    def test_OpenAIでアイデアの自動生成が成功しているかどうか(self):
        word = "アイデアの自動生成"
        data = self.manager.create_ideas(word)
        self.assertIn('results', data)
        self.assertIn('title', data['results'])
        self.assertIn('description', data['results'])

    def test_Geminiでアイデアの自動生成が成功しているかどうか(self):
        word = "アイデアの自動生成"
        data = self.manager.create_ideas_with_gemini(word)
        self.assertIn('results', data)
        self.assertIn('title', data['results'])
        self.assertIn('description', data['results'])

    def test_マネタイズの自動生成が成功しているかどうか(self):
        data = self.manager.create_monetization_with_gemini(
            title="運動仲間マッチングサービス『FUN MOVE』",
            description="趣味やレベル、目標別に運動仲間を探せるマッチングサービスです。アプリを通じて、同じ趣味を持つ仲間を見つけ、一緒に運動を楽しめるイベントやグループトレーニングなどを企画できます。運動のモチベーション維持をサポートし、楽しく健康的なライフスタイルを促進します。")
        
        if self.assertIn('results', data):
            self.assertIn('description', data['results'])
       

       