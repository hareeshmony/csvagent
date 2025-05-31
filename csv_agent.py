
import os
from langchain_experimental.agents import create_csv_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model1 = "llama3-70b-8192"
model2 = "gemma2-9b-it"
model3 = "llama-3.3-70b-versatile"
model4 = "deepseek-r1-distill-llama-70b"

llm = ChatGroq(
    model_name=model2,
    api_key= groq_api_key,
    temperature=0.5
)

def csv_agent_invoker(csv_file_name, user_query):
    agent        = create_csv_agent(llm, csv_file_name, 
                                    allow_dangerous_code=True, 
                                    verbose=True)

    output_response = agent.run(user_query)
    return output_response
