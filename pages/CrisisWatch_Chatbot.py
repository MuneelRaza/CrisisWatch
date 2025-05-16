import streamlit as st
from langchain_core.messages import HumanMessage
from agent.crisis_agent import crisis_agent


st.set_page_config(page_title="Crisis Agent Chatbot", page_icon="🕊️")

st.title("🕊️ Crisis Analysis Chatbot")


if "agent" not in st.session_state:
    st.session_state.agent = crisis_agent()


if "history" not in st.session_state:
    st.session_state.history = []


def add_message(user_msg, bot_msg):
    st.session_state.history.append((user_msg, bot_msg))


def run_agent(user_input):
    agent = st.session_state.agent
    config = {"configurable": {"thread_id": "streamlit"}}

    with st.spinner("Agent is thinking..."):
        response = agent.invoke(
            {
                "messages": [HumanMessage(content=user_input)]
            },
            config
        )
    bot_msg = response["messages"][-1].content
    return bot_msg


with st.form("input_form", clear_on_submit=True):
    user_input = st.text_input("Ask about a crisis or situation:")
    submitted = st.form_submit_button("Send")


if submitted and user_input.strip():
    bot_response = run_agent(user_input.strip())
    add_message(user_input.strip(), bot_response)


for user_msg, bot_msg in st.session_state.history:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Agent:** {bot_msg}")
    st.markdown("---")
