import json
from flask import Flask, request
import os
from bs4 import BeautifulSoup
import requests
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import openai

from response_model import ResponseModel, response_model_from_dict

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    text = str(request.args.get('input'))
    char_count = len(text)
    data = {'input': text, 'characters': char_count}
    return getData2(text);
    return 'HELLO...'
def getData2(url = "https://docs.flutter.dev/development/data-and-backend/state-mgmt/ephemeral-vs-app"):
    # url = "https://docs.flutter.dev/development/data-and-backend/state-mgmt/ephemeral-vs-app"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    summ_per = summarize(soup.text, ratio = 0.5)
    # soup.text
    openai.api_key = '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'
    try:
        response = openai.Completion.create(
            engine = 'text-davinci-003',
            max_tokens = 1024,
            n=1,
            stop = None,
            temperature = 0.3,
            prompt = "Create a summary for the given text: {0} in 200 words. Please also format the text and re-phrase it.".format(summ_per)
        # prompt= "Provide Major Points from the given text: {0}. Please give response point wise add \\n after each point".format(summ_per)
        )
        print(response);
        # Parse JSON response into a dictionary
        response_dict = response

        # Instantiate a ResponseModel object
        response_model = response_model_from_dict(response_dict)

        # Access the text attribute of the first choice
        first_choice_text = response_model.choices[0].text

        return(first_choice_text)  

    except Exception as e:
        return str(e)
    # return response.get('choices').
def getData():
    os.environ['OPENAI_API_KEY'] = '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'
    print(os.getenv('OPENAI_API_KEY'))


    url = "https://docs.flutter.dev/development/data-and-backend/state-mgmt/ephemeral-vs-app"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    soup.text

    content = []
    for item in soup.findAll('p'):
        content.append(item.text.strip())


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100
    )
    texts = text_splitter.split_text(' '.join(content))
    docs = [Document(page_content=t) for t in texts]


    llm = OpenAI(temperature=0, openai_api_key=os.environ.get('API_KEY'))
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    summary = chain.run(docs)

    summ_per = summarize(soup.text, ratio = 0.5)

    # print('1...')
    # openai.api_key = os.environ.get('API_KEY')

    # response = openai.Completion.create(
    #     engine = 'text-davinci-003',
    # prompt="What this web page convey message, Summarize this text below: \n {0}".format(summ_per)
    # )
    # print(response)
    return summ_per
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 3010)