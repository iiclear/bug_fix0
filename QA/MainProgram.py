#coding:utf-8
import aiml
import os, sys

from QA.QACrawler import baike
from QA.Tools import Html_Tools as QAT
from QA.Tools import TextProcess as T#文字处理
from QACrawler import search_summary

def run(question):
    # 初始化jb分词器
    T.jieba_initialize()

    # 切换到语料库所在工作目录
    mybot_path = './'
    os.chdir(mybot_path)


    mybot = aiml.Kernel()
    if os.path.isfile("bot_brain.brn"):
        mybot.bootstrap(brainFile="bot_brain.brn")
    else:
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/std-startup.xml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tuling.xml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/test.xml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bye.aiml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tools.aiml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bad.aiml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/funny.aiml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/OrdinaryQuestion.aiml")
        mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/Common conversation.aiml")
        #mybot.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        mybot.saveBrain("bot_brain.brn")



    # 载入百科属性列表

    print '''
    Eric：你好，我是问答机器人。╭(╯^╰)╮
       '''

    input_message = question

    if len(input_message) > 60:
        return mybot.respond("句子长度过长")
        #continue
    elif input_message.strip() == '':
        return mybot.respond("无话可说")
        #continue

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
            print response+'mark'

        else:
            return response

        print "======="

        if response == "":
            ans = mybot.respond('找不到答案')
            print 'Eric：' + ans
        # 百科搜索
        elif response[0] == '#'or len(response)<1:
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
                    return '回答：' + QAT.ptranswer(ans, False)
                    #continue
                elif ans.decode('utf-8').__contains__(u'::找不到'):
                    # 百度摘要+Bing摘要
                    print "通用搜索"
                    ans = search_summary.kwquery(input_message)

            # 匹配不到模版，通用查询
            elif response.__contains__("NoMatchingTemplate"):
                print "NoMatchingTemplate"
                ans = search_summary.kwquery(input_message)

            if len(ans) == 0:
                ans = mybot.respond('找不到答案')
                return '回答：' + ans
            elif len(ans) > 1:
                print "不确定候选答案"
                return ans
                print 'Eric: '
                for a in ans:
                    print a.encode("utf-8")
            else:
                return '回答：' + ans[0].encode("utf-8")



        # 匹配模版
        else:
            return '回答：' + response
