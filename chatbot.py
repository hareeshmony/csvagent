import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from matplotlib.pyplot import show
import streamlit as st
import tempfile
import os
import csv_agent, plotter

st.set_page_config(layout="wide")

st.title("🤖📊 CSV Agent Chatbot ")
# If the Global variable is not created, create it once.
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Parse through the Global and print the Chat History
for chats in st.session_state.chat_history:
    with st.chat_message(chats["role"]):
        st.markdown(chats['content'])
        if chats["role"]=="Assistant":
            if chats['html_content'] != "":
                with st.expander("📈📝 See explanation "):
                    st.components.v1.html(chats['html_content'], height=600, scrolling=True)



st.sidebar.header("📁 Upload an CSV File ")
uploaded_file = st.sidebar.file_uploader("", type=["csv"])
temp_file_path = ''
if uploaded_file is not None:
    try:
        # Save to a temporary file to get a file path
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
    # Print User Input
    with st.chat_message("User"):
        st.markdown(user_input)
        # Store the User input in Streamlit Global
        st.session_state.chat_history.append({"role":"User", "content": user_input})

    #################################### Agent invoking ########################################################
    if temp_file_path == '':
        with st.chat_message("Assistant"):
            st.markdown("Please upload a .csv file for Q&A")
            st.session_state.chat_history.append({"role":"Assistant", "content": "Please upload a .csv file for Q&A"})
    else:
        csv_agent_response      = csv_agent.csv_agent_invoker(temp_file_path, user_input)
        html_content, response  = plotter.output_formatter(user_input, csv_agent_response)
        
        # Print Agent Response
        with st.chat_message("Assistant"):
            st.markdown(response)
            if html_content != "":
                with st.expander("📈📝 See explanation "):
                    st.components.v1.html(html_content, height=600, scrolling=True)
            
            # Store the AI Response in Streamlit Global
            st.session_state.chat_history.append({"role":"Assistant", "content": response, "html_content":html_content})
        



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