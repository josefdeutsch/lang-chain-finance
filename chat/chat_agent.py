import os
import threading
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from chat.cointegration import calculate_optimal_hedge_ratio
from chat.hurstexponent import calculate_hurst_exponent
from chat.desc import explain_hurst_exponent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.retry import RunnableRetry
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory


class SingletonMeta(type):
    """
    A thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

    def reset_instance(cls):
        """
        Reset the singleton instance.
        """
        with cls._lock:
            if cls in cls._instances:
                del cls._instances[cls]


class ChatAgent(metaclass=SingletonMeta):
    """
    A singleton class to manage agent invocation.
    """

    def __init__(self):
        """
        Initialize the ChatAgent instance.
        """
        self._initialize_environment()
        self._initialize_components()

    def _initialize_environment(self):
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
        os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
        os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

        self.working_directory = os.environ.get("CURRENT_WORKING_DIRECTORY")

    def _initialize_components(self):
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
        self.memory = ChatMessageHistory(session_id="polygon-api-query")

        # Create a temporary working directory
        # self.working_directory = TemporaryDirectory()

        # Initialize the FileManagementToolkit with the working directory
        filetool = FileManagementToolkit(
            root_dir=str(self.working_directory),
            selected_tools=["read_file", "write_file", "list_directory"],
        )

        tools = [calculate_optimal_hedge_ratio, 
                 calculate_hurst_exponent, 
                 explain_hurst_exponent] + filetool.get_tools()
        
        # Create the agent
        agent = create_openai_tools_agent(llm, tools, prompt)

        # Initialize the agent executor
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Wrap the agent with chat history
        self.agent_with_chat_history = RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        #self.agent_with_chat_history_retries = RunnableRetry(
        #    bound= self.agent_with_chat_history,
        #   retry_exception_types=(ValueError,),
        #   max_attempt_number=2,
        #   wait_exponential_jitter=True
        # )

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the class.
        """
        return cls()

    def invoke(self, input_data, config):
        """
        Invoke the agent with the given input data and configuration.

        Args:
            input_data (dict): The input data for the agent.
            config (dict): The configuration for the agent.

        Returns:
            dict: The response from the agent.
        """
        try:
            response = self.agent_with_chat_history.invoke(input_data, config)
            return response
        except Exception as e:
            # Log the exception here as needed
            raise RuntimeError(f"Failed to invoke the agent: {e}") from e

    def cleanup(self):
        """
        Cleanup resources used by the ChatAgent.
        """
        # Add any resource cleanup code here, such as closing files or database connections
        # For example, if using TemporaryDirectory:
        if isinstance(self.working_directory, TemporaryDirectory):
            self.working_directory.cleanup()
        # Cleanup any other resources if needed
