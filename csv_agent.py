from langchain_experimental.agents import create_csv_agent
from langchain_groq import ChatGroq

def csv_agent_invoker(csv_file_name, user_query, groq_api_key):
    model2 = "gemma2-9b-it"
    llm = ChatGroq(
        model_name=model2,
        api_key=groq_api_key,
        temperature=0.5
    )
    agent = create_csv_agent(llm, csv_file_name, allow_dangerous_code=True, verbose=True)
    output_response = agent.run(user_query)
    return output_response
