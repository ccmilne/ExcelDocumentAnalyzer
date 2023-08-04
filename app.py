import streamlit
import pandas as pd
import os

from langchain.llms import OpenAI
from langchain.agents import create_csv_agent

#API KEY
openai_key = os.getenv("OPENAI_API_KEY")

def csv_agent(file):
    return create_csv_agent(llm=OpenAI(temperature=0), path=file, verbose=False)


#Webpage
streamlit.set_page_config(page_title="Chat with your Excel Document", page_icon=":random:", layout='centered')
streamlit.title('Chat with your Excel Document')

# #Take an input
# txt_input = streamlit.text_area('Enter your text to summarize', '', height=200)
user_file = streamlit.file_uploader("Upload file", type={"csv", "excel"}, accept_multiple_files=False)

if user_file is not None:
    streamlit.write(f"Uploaded Dataset: {os.path(user_file)}")
    if os.path.splitext(user_file.name)[1] == ".csv":
        df = pd.read_csv(user_file)
    elif os.path.splitext(user_file.name)[1] == '.xlsx':
        df = pd.read_excel(user_file)
    streamlit.write(df)
    agent = csv_agent(file=user_file)

else:
    url = "https://www.kaggle.com/datasets/sdolezel/black-friday?resource=download"
    streamlit.write(f"Placeholder Dataset: [Black Friday Sales]({url})")
    df = pd.read_csv('data/test.csv')
    streamlit.write(df)
    agent = csv_agent(file="data/test.csv")

question = streamlit.text_area("Ask the data a question", "", placeholder="Example: How many rows are there?\nExample: What % of the rows contain nulls?")

###Conversational part
with streamlit.form("answer_form", clear_on_submit=True):
    openai_key = streamlit.text_input('OpenAI API Key', type='password', disabled=not question, value=streamlit.secrets['OPENAI_API_KEY'])
    submitted = streamlit.form_submit_button("SUBMIT")

    if submitted and openai_key:
        with streamlit.spinner("Answering ..."):
            response = agent.run(question)
            if response:
                streamlit.write(response)

# #Form to accept input
# result = []
# with streamlit.form('summarize_form', clear_on_submit=True):
#     openai_api_key = streamlit.text_input('OpenAI API Key', type='password', disabled=not txt_input, value=streamlit.secrets['OPENAI_API_KEY'])
#     submitted = streamlit.form_submit_button('SUBMIT')

#     if submitted and openai_api_key.startswith('sk-'):
#         with streamlit.spinner('Summarizing ...'):
#             response = generate_response(txt_input)
#             result.append(response)
#             del openai_api_key

# if len(result):
#     streamlit.write(response)