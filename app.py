# coding:utf8
import aiml

import sys
reload(sys)
import json
from QA.Tools.tuling import geta
from flask import Flask, render_template, request
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer

from QA.QACrawler import baike
from QA.Tools import Html_Tools as QAT
from QA.Tools import TextProcess as T#文字处理
from QA.QACrawler import search_summary

# 初始化jb分词器
T.jieba_initialize()
 # 切换到语料库所在工作目录
mybot = aiml.Kernel()

# if os.path.isfile("bot_brain.brn"):
#     mybot.bootstrap(brainFile="bot_brain.brn")
# else:
#
#     mybot.saveBrain("bot_brain.brn")


# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/std-startup.xml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tuling.xml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/test.xml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "QA/resources/bye.aiml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "QA/resources/tools.aiml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "QA/resources/bad.aiml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "QA/resources/funny.aiml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "QA/resources/OrdinaryQuestion.aiml")
# mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "QA/resources/Common conversation.aiml")
#mybot.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
mybot.learn(r'QA/resources/std-startup.xml')
mybot.learn(r'QA/resources/bye.aiml')
mybot.learn(r'QA/resources/tools.aiml')
mybot.learn(r'QA/resources/bad.aiml')
mybot.learn(r'QA/resources/funny.aiml')
mybot.learn(r'QA/resources/OrdinaryQuestion.aiml')
mybot.learn(r'QA/resources/Common conversation.aiml')
mybot.learn(r'QA/resources/shopping.aiml')
app = Flask(__name__)

@app.route('/api/<question>')
def hello_world(question):
    return 'hello'

@app.route("/test")
def ws():
    user_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    while 1:
        msg =user_socket.receive()
        question = json.loads(msg)
        q = question['data']['mine']['content']
        msg =q
        input_message = str(msg).encode('utf-8')
        if len(input_message) > 60:
            answer =  mybot.respond("句子长度过长")
            # continue
        elif input_message.strip() == '':
            answer = mybot.respond("无话可说")
            # continue

        # print input_message
        message = T.wordSegment(input_message)
        # 去标点
        # print 'word Seg:'+ message
        # print '词性：'
        words = T.postag(input_message)

        if message == 'q':
            exit()
        else:
            response = mybot.respond(message)  # 在AIML数据集里寻找答案

            print "======="
            if response[0] == '#':
                print response + 'mark'

            else:
               answer =  response

            print "======="

            if response == "":
                ans = mybot.respond('找不到答案')
                answer = ans
            # 百科搜索
            elif response[0] == '#' or len(response) < 1:
                # 匹配百科
                if response.__contains__("searchbaike"):
                    print "searchbaike"
                    print response
                    res = response.split(':')
                    # 实体
                    entity = str(res[1]).replace(" ", "")
                    # 属性
                    attr = str(res[2]).replace(" ", "")
                    print entity + '<---->' + attr

                    ans = baike.query(entity, attr)

                    # 如果命中答案
                    if type(ans) == list:
                        answer = '回答：' + QAT.ptranswer(ans, False)
                        # continue
                    elif ans.decode('utf-8').__contains__(u'::找不到'):
                        # 百度摘要+Bing摘要
                        print "通用搜索"
                        answer = search_summary.kwquery(input_message)

                # 匹配不到模版，通用查询
                elif response.__contains__("NoMatchingTemplate"):
                    print "NoMatchingTemplate"
                    ans = search_summary.kwquery(input_message)

                if len(ans) == 0:
                    ans = mybot.respond('找不到答案')
                    answer = '回答：' + ans
                elif len(ans) > 1:
                    print "不确定候选答案"
                    answer = ans[0]
                    print 'Eric: '
                    for a in ans:
                        print a.encode("utf-8")
                else:
                    answer = '回答：' + ans[0].encode("utf-8")



            # 匹配模版
            else:
                answer = '回答：' + response

        s = '展开全部'

        if (type(answer).__name__ == 'list') or '唔... 怎么回答...' or '唔... 主人没有教我怎么回答'in answer or '天气' in msg:
            answer = geta(msg)
        else:
            print answer
            if s in str(answer):
                print answer
                answer = str(answer).replace('\n', '').replace('展开全部', "").split('已赞过')[0]
                print  'OS' +answer
        print user_socket,msg

        res =answer
        a = {
            "username": "客服姐姐",
            "avatar": "https://robot.rszhang.top/images/icon/nv/0.jpg",
            "id": "-2",  # //消息的来源ID（如果是私聊，则是用户id，如果是群聊，则是群组id）
            "type": "friend",  # //聊天窗口来源类型，从发送消息传递的to里面获取
            "content": res,  # //消息内容
            "cid": 0,  # //消息id，可不传。除非你要对消息进行一些操作（如撤回）
            "mine": True,  # //是否我发送的消息，如果为true，则会显示在右方
            "fromid": "100000",  # /消息的发送者id（比如群组中的某个消息发送者），可用于自动解决浏览器多窗口时的一些问题
            "timestamp": 1467475443306,  # //服务端时间戳毫秒数。注意：如果你返回的是标准的 unix 时间戳，记得要 *1000
        }

        user_socket.send(json.dumps(a))


@app.route('/chat/')
def chat():
    return render_template('webchat.html')


if __name__ == '__main__':
    ip = '0.0.0.0'
    # http_serv = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    # http_serv.serve_forever()
    http_serv = WSGIServer((ip.encode('utf8'),5000),app,handler_class=WebSocketHandler)
    http_serv.serve_forever()