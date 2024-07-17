import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory

# Load environment variables
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

# Define the prompt template
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

# Initialize chat history
memory = ChatMessageHistory(session_id="polygon-api-query")

# Create a temporary working directory
working_directory = TemporaryDirectory()
# Initialize the FileManagementToolkit with the working directory
tools = FileManagementToolkit(
    root_dir=str(working_directory.name),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Initialize the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Wrap the agent with chat history
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Example invocations
agent_with_chat_history.invoke(
    {"input": "Hello, I am John Doe. I am 32 years old"},
    config={"configurable": {"session_id": "polygon-api-query"}}
)

agent_with_chat_history.invoke(
    {"input": "Tell me how old John Doe is."},
    config={"configurable": {"session_id": "polygon-api-query"}}
)

agent_with_chat_history.invoke(
    {"input": "Write file: john_doe.csv"},
    config={"configurable": {"session_id": "polygon-api-query"}}
)

response = agent_with_chat_history.invoke(
    {"input": "Read file: john_doe.csv"},
    config={"configurable": {"session_id": "polygon-api-query"}}
)

print(response)
