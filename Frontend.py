
import streamlit as st


# Title
st.set_page_config(page_title=" 🤖 Mental Health Chat-Bot", layout="centered")
st.title("🤖 Mental Health Chat-Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat message display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask something...")

# If user inputs a prompt
if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for chatbot response logic
    # Replace with call to your own chatbot model or API
    response = f"Echo: {prompt}"

    # Display chatbot message
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

