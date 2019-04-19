#coding:utf-8
import requests
import json
API_KEY = '449cf351eef849fba309367fbd0312f8'
API = 'http://openapi.tuling123.com/openapi/api/v2'

def geta(question):
    req ={
	"reqType":0,
    "perception": {
        "inputText": {
            "text": question
        },
        "inputImage": {
            "url": "imageUrl"
        },
        "selfInfo": {
            "location": {
                "city": "周口",
                "province": "周口",
                "street": "文昌大道"
            }
        }
    },
    "userInfo": {
        "apiKey": API_KEY,
        "userId": "123"
    }
}

    response = requests.post(API,data = json.dumps(req))
    ans = json.loads(response.text)
    return '*'+ans['results'][0]['values']['text']

if __name__ == '__main__':
    print geta('wocao')