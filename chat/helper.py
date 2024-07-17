from langchain_core.runnables.history import RunnableWithMessageHistory

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",

    agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

agent_with_chat_history.invoke(
   {"input": "Retrieve the aggregate closing price data for the X:ETHUSD and X:BTCUSD tickers from June 6, 2024, to July 7, 2024. For each ticker, compile a list containing the open, close, high, low, and volume data for the specified date range. Create two separate CSV files to store this information: one file for the BTC data and another file for the ETH data."},
    config={"configurable": {"session_id": "<foo>"}},
)

# Initialize chat message history
memory = ChatMessageHistory(session_id="polygon-api-query")