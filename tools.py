#coding:utf8
import requests
from bs4 import BeautifulSoup
import itchat
from QA.Tools.tuling import geta
from QA.MainProgram import run

def getreplay(question):
    url = 'http://47.101.221.48:5000/api/'+question
    response = requests.get(url)
    web_data = BeautifulSoup(response.text,"lxml")
    ans = web_data.select('body')
    return str(ans[0].get_text()).replace('回答：','').replace('\n','').strip()

@itchat.msg_register(itchat.content.TEXT)
def reply_msg(msg):
    if msg['Content'] == u'你好':
        itchat.send_msg(msg['User']['NickName'] + "你好啊！我是百科机器人", msg['FromUserName'])

    answer = getreplay(msg['Content'])
    itchat.send_msg('@'+msg['User']['NickName'] +' '+ str(answer), msg['FromUserName'])

def web_bot(question):
    answers = " "
    s = '展开全部'
    ans =" "
    answer = run(str(question).encode('utf-8'))
    print type(answer),'webbot1'
    if (type(answer).__name__ == 'list') or '唔... 怎么回答...' in answer or '天气' in question:
        answer = geta(question)
        return answer
    else:
        print answer,'webbot2'
        if s in str(answer):
            print answer
            answer = str(answer).replace('\n', '').replace('展开全部', "").split('已赞过')[0]
            print answer + '666'
            answer = str(answer).replace('回答：', '').replace('\n', '').strip()
            print answer, 'webbot3'
        return answer




if __name__ == '__main__':
    itchat.auto_login()
    itchat.run()