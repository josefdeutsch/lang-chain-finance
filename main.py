import os
import numpy as np
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent 

from langchain_openai import ChatOpenAI

from tools.cointegration import calculate_optimal_hedge_ratio2


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')
os.environ["POLYGON_API_KEY"] = os.getenv('POLYGON_API_KEY')

polygon = PolygonAPIWrapper()

polytool = PolygonToolkit.from_polygon_api_wrapper(polygon)

prompt = ChatPromptTemplate.from_messages(
    [
       ("system", "A reliable and exact assistant, capable of utilizing tools to answer questions. If a tool is unavailable, the assistant will notify you accordingly."),
       ("user", "{input}"),
       MessagesPlaceholder("chat_history", optional=True),
       MessagesPlaceholder(variable_name="agent_scratchpad"),
   ]
)

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

tools = [calculate_optimal_hedge_ratio2] + polytool.get_tools()

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
    {
        "chat_history": [
            HumanMessage(content="Retrieve daily aggregate data for the X:ETHUSD ticker (timespan: 1 day) from 2024-06-06 to 2024-07-07 and for the X:BTCUSD ticker (timespan: 1 day) from 2024-06-06 to 2024-07-07.")
        ],
        "input": "Calculate the CADF using closing prices."
    }, {
        "chat_history": [
            HumanMessage(content="")
        ],
        "input": "Analyze the significance of the p-value relative to the 10% threshold in the CADF test to determine if the time series data are cointegrated, based on the stationarity of the residuals."
    }
    
)

