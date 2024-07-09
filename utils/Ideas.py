# アイデアの生成や削除修正を行う

from django.conf import settings
from openai import OpenAI
import json

import google.generativeai as genai

class IdeaManager():

    def create_ideas(self,word):
        print("Open A")
       
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
    
    def create_ideas_with_gemini(self,word):
        print("Gemini AI")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
            )
        category = "サービス" # 事業,サービス、ゲーム
        idea = word  # ユーザーに入力
        count =  1
        prompt = {f"""
            "You are a top-tier web service planner, capable of devising original new services, businesses, and ideas.
             Please provide {count} titles and descriptions for ideas using lateral thinking
                Please consider specializing in {category}
                Please include {idea}
       
                
                以下のように出力してください
                サービスのタイトル(title)そのサービスの詳しい説明(description)をjson形式で日本語で出力してください
                "results":{{"title":"", "description":""}},
        """}
        
        response = model.generate_content(prompt)
        data = json.loads(response.text)
   
        return data
    
    def create_monetization_with_gemini(self,title,description):
        print("Gemini AI")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
            )
      

        prompt = f"""
            #お願い
            あなたは一流のWebサービスのマネタイズ担当です。マネタイズ方法を出してください。
            # 内容
            タイトル: {title}
            内容: {description}
            この内容のマネタイズ方法を考えてください

            以下のように出力してください
            サービスのマネタイズ方法(description)をjson形式で日本語で出力してください
            "results": {{"description": ""}},
        """
        
        response = model.generate_content(prompt)
        try:
           
            safe_response_text = response.text.encode('unicode_escape').decode('utf-8') 
           
            print(safe_response_text)
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("エラーです")
            print(response.text)
            data = {"error": "Invalid JSON response"}
        
        print(data)
        return data

    
    
# https://qiita.com/NOIZE/items/8420b9c54c185f828c49#%E4%BD%BF%E3%82%8F%E3%82%8C%E3%81%A6%E3%81%84%E3%81%AA%E3%81%84%E7%94%BB%E5%83%8F%E3%81%AE%E5%89%8A%E9%99%A4
    # python manage.py deleteorphanedmedia