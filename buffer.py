import os
import numpy as np
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent 
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from tools.cointegration import calculate_optimal_hedge_ratio
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

prompt = ChatPromptTemplate.from_messages(
    [
       ("system", "An exceptionally accurate and precise agent processes all input data and delivers comprehensive results, ensuring no information is omitted. This dependable assistant efficiently uses available tools to answer questions, returning all relevant data, and promptly notifying you if any tool is unavailable."),
       ("user", "{input}"),
       MessagesPlaceholder("chat_history", optional=True),
       MessagesPlaceholder(variable_name="agent_scratchpad"),
   ]
)

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

root = os.getcwd()
#working_directory = TemporaryDirectory()

# Initialize the FileManagementToolkit with the working directory
filetool = FileManagementToolkit(root_dir=root)

polygon = PolygonAPIWrapper()

polytool = PolygonToolkit.from_polygon_api_wrapper(polygon)

memory = ChatMessageHistory(session_id="polygon-api-query")

tools = [calculate_optimal_hedge_ratio] + polytool.get_tools() + filetool.get_tools()

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)


#agent_with_chat_history.invoke(
#   {"input": "Retrieve the aggregate closing price data for the X:ETHUSD and X:BTCUSD tickers from June 6, 2024, to July 7, 2024. For each ticker, compile a list containing the open, close, high, low, and volume data for the specified date range. Create two separate CSV files to store this information: one file for the BTC data and another file for the ETH data."},
#    config={"configurable": {"session_id": "<foo>"}},
#)

agent_with_chat_history.invoke(
    {"input": "Perform CADF Test by reading BTCUSD and ETHUSD data on the close prices from the .csv files."},
    config={"configurable": {"session_id": "<foo>"}},
)


