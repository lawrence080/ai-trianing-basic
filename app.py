from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os
import api_secrets
import docx2txt
import conversation
import singleDialog

os.environ["OPENAI_API_KEY"] = api_secrets.API_KEY


def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

def chatbot(input_text, conversation:conversation.conversation):
    dialog = singleDialog.singleDialog(person = 'user:'+input_text)
    conversation.addConversation(dialog)
    response = conversation.readconversation(dialog=dialog)
    conversation.addbottocon('bot: '+response.response)
    # return response
    
    # index = GPTSimpleVectorIndex.load_from_disk('index.json')
    # input_text = input_text+settingQuery()
    # print(input_text)
    # response = index.query(input_text, response_mode="compact")
    # return response.response

def storeQuery():
    pass

    


def settingQuery():
    text = input("please enter setting")
    if text == "NO":
        text = 'please answer the question with 100 percent accuracy. please answer the question with 70 percent humor. please talk like cooper'
    return text
# iface = gr.Interface(fn=chatbot,
#                      inputs=gr.components.Textbox(lines=7, label="Enter your text"),
#                      outputs="text",
#                      title="Custom-trained AI Chatbot")

# index = construct_index("doc")
# iface.launch(share=True)

if __name__ == "__main__":
    question = ''
    conv = conversation.conversation()
    while(True):
        question = input("please enter the question ")
        if question == 'n': break
        # construct_index("doc")
        response = chatbot(question,conv)
        # for i in conv.conv:
        #     print(i.person+" ", end='')
        #     print(i.bot)
        # print(response)