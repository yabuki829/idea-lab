# アイデアの生成や削除修正を行う

from django.conf import settings
from openai import OpenAI
import json
class IdeaManager():
    
    def create_ideas(self,word):

       
        client = OpenAI(api_key=settings.API_KEY)   
        category = "サービス" # 事業,サービス、ゲーム
        idea = word  # ユーザーに入力
        # target = "アイデアを作りたい人" # ユーザーに入力
        count =  1
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a top-tier web service planner, capable of devising original new services, businesses, and ideas."},
            {"role": "user", "content": 
                f"""
                Please provide {count} titles and descriptions for ideas using lateral thinking
                Please consider specializing in {category}
                Please include {idea}
       
                
                以下のように出力してください
                サービスのタイトル(title)そのサービスの詳しい説明(description)をjson形式で日本語で出力してください
                "results":{{"title":"", "description":""}},

                """}
                ],

                response_format={"type": "json_object"}
        )
        
        data = json.loads(completion.choices[0].message.content)
        # TODO: エラーの時の処理を追加する
        return data
    
    