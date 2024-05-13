from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from openai import OpenAI
import json


def index(request):
    client = OpenAI(api_key=settings.API_KEY)   
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
                {"role": "system", "content": "あなたは一流のWebサービスの企画担当で、独創的で、まだ誰も思いついていないような、新しいサービスのアイデア考えることができます。"},
                {"role": "user", "content": 
                """
               アイデアのタイトルと説明を水平思考で考え2つ出してください。
                # カテゴリ
                Webサービス

                # 情報
                ・ターゲット：アイデアを考えている人
                ・満たしたいニーズ：アイデアを考えるのを手助けしたい

                以下のように出力してください
                サービスのタイトル(title)そのサービスの詳しい説明やアイデア(explain)をjson形式で出力してください
                "results":[{title:"",explain:""},{title:"",explain:""}]

                """}
                
            ],
            response_format={"type": "json_object"}
    )


    data = json.loads(completion.choices[0].message.content)

# 各サービスのタイトルと説明を出力
    for service in data['results']:
        print(f"タイトル: {service['title']}")
        print(f"説明: {service['explain']}\n")
   
    return HttpResponse(completion.choices[0].message.content)



     