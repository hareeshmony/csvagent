import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env (for local development)
load_dotenv()

# Try to get the API key from .env or Streamlit secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", None))

from langchain_groq import ChatGroq
from matplotlib.pyplot import show
import tempfile
import csv_agent, plotter

st.set_page_config(layout="wide")
st.title("🤖📊 CSV Agent Chatbot ")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for chats in st.session_state.chat_history:
    with st.chat_message(chats["role"]):
        st.markdown(chats['content'])
        if chats["role"] == "Assistant":
            if chats['html_content'] != "":
                with st.expander("📈📝 See explanation "):
                    st.components.v1.html(chats['html_content'], height=600, scrolling=True)

st.sidebar.header("📁 Upload an CSV File ")
uploaded_file = st.sidebar.file_uploader("", type=["csv"])
temp_file_path = ''
if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_file_path = tmp_file.name

        st.sidebar.write("📁 File Upload status")
        st.sidebar.code("SUCCESSFUL")
    except Exception as e:
        st.error(f"❌ Error uploading .csv file: {e}")
        st.sidebar.write("📁 File Upload status")
        st.sidebar.code("FAILED")

if user_input := st.chat_input("........"):
    with st.chat_message("User"):
        st.markdown(user_input)
        st.session_state.chat_history.append({"role": "User", "content": user_input})

    if temp_file_path == '':
        with st.chat_message("Assistant"):
            st.markdown("Please upload a .csv file for Q&amp;A")
            st.session_state.chat_history.append({"role": "Assistant", "content": "Please upload a .csv file for Q&amp;A"})
    else:
        # Pass the API key to csv_agent
        csv_agent_response = csv_agent.csv_agent_invoker(temp_file_path, user_input, GROQ_API_KEY)
        html_content, response = plotter.output_formatter(user_input, csv_agent_response)

        with st.chat_message("Assistant"):
            st.markdown(response)
            if html_content != "":
                with st.expander("📈📝 See explanation "):
                    st.components.v1.html(html_content, height=600, scrolling=True)

            st.session_state.chat_history.append({"role": "Assistant", "content": response, "html_content": html_content})

        



# show me a preview of data
# Show me the preview of the file
# What is the Maximum size products available?
# What is the Percentage of Products that are XXL compared to rest?
# Give me list of top 10 stock prices of the companies, along with their company name

# How much percentage of Large & Small items are present? Give me detailed distribuion of each size of products

# How much %of products lie under 700 USD. Compare it with rest.



# model2 = "gemma2-9b-it"

# llm = ChatGroq(
#     model_name=model2,
#     api_key= groq_api_key,
#     temperature=0.7

# )
