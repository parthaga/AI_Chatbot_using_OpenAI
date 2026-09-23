import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
# It automatically picks up the OPENAI_API_KEY environment variable
client = OpenAI()

# Set up the web page title and icon
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 My Custom LLM Chatbot")

# 1. Initialize Chat History in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, friendly AI assistant."}
    ]

# 2. Display existing conversation history (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 3. Handle New User Input
if user_input := st.chat_input("Type your message here..."):
    
    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Append user message to memory
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 4. Generate AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call the LLM API with streaming enabled for a fast feel
            stream = client.chat.completions.create(
                model="gpt-4o-mini",  # Highly cost-effective and capable model
                messages=st.session_state.messages,
                stream=True,
            )
            
            # Render tokens sequentially as they arrive from the API
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
                    
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "Sorry, I encountered an issue processing your request."
            message_placeholder.markdown(full_response)

    # Append assistant response to memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})
