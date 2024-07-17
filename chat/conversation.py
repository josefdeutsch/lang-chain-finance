import os
from tempfile import TemporaryDirectory
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_core.runnables.history import RunnableWithMessageHistory
from tempfile import TemporaryDirectory

# Load environment variables from a .env file
load_dotenv()

# Set environment variables
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')
os.environ["POLYGON_API_KEY"] = os.getenv('POLYGON_API_KEY')

working_directory = os.environ.get("CURRENT_WORKING_DIRECTORY")

prompt = ChatPromptTemplate.from_messages(
    [
       ("system", "An exceptionally accurate and precise agent processes all input data and delivers comprehensive results, ensuring no information is omitted. This dependable assistant efficiently uses available tools to answer questions, returning all relevant data, and promptly notifying you if any tool is unavailable."),
       ("user", "{input}"),
       MessagesPlaceholder("chat_history", optional=True),
       MessagesPlaceholder(variable_name="agent_scratchpad"),
   ]
)
# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Create a temporary working directory
#working_directory = TemporaryDirectory()
#working_directory = os.getenv["CURRENT_WORKING_DIRECTORY"]
print(str(working_directory))

# Initialize file management toolkit
filetool = FileManagementToolkit(root_dir=str(working_directory))

# Get tools from Polygon and file management toolkits
tools = filetool.get_tools()

# Create the OpenAI tools agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Initialize the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

memory = ChatMessageHistory(session_id="polygon-api-query-1234")

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)


