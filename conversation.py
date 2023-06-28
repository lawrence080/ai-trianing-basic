from typing import Any
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os
import api_secrets
import docx2txt
import singleDialog

class conversation:
    conv = ['']


    
    def __init__(self) :
        self.conv = []

    def getConversation(self):
        return self.conv

    def addbottocon(self, botstring):
        self.conv[len(self.conv)-1].bot = botstring

    def addConversation(self,dialog:singleDialog.singleDialog):
        self.conv.append(dialog)
        return self.conv

    def readconversation(self, dialog:singleDialog.singleDialog):
        totalConversation = ''
        for i in self.conv:
            totalConversation = totalConversation + '\n'+i.person + '\n'+i.bot
        totalConversation = totalConversation + '. you are bot, and I am user. reply user\'s message'
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        response = index.query(totalConversation, response_mode="compact")
        # print(totalConversation)
        print(response)
        return response


    def getArr(self):
        return self.conv
    



    
