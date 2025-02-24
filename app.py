import os
import time
import streamlit as st
import mistralai
from mistralai.client import MistralClient

# Streamlit Page Configuration
st.set_page_config(page_title="Cyberesolve", layout="centered")

# Hide Streamlit UI elements (hamburger menu and footer)
def hide_hamburger_menu():
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

hide_hamburger_menu()

# Header Section with Logo
st.image("cyber.png", use_container_width=True)

# Initialize session states for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Mistral API Client
def initialize_mistral(api_key):
    try:
        return MistralClient(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing the Mistral API model: {str(e)}")
        st.stop()

# Load Mistral Model
mistral_client = initialize_mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Display Chat History
def display_chat_history():
    for message in st.session_state.messages:
        if message.get("role") == "user":
            st.chat_message("user").write(message.get("content"))
        else:
            st.chat_message("assistant").write(message.get("content"))

# Simulate typing effect for better user experience
def typing_effect(response_text):
    full_response = "⚠ *Be specific about the topic while you query* \n\n\n"
    message_placeholder = st.empty()

    for chunk in response_text:
        full_response += chunk
        time.sleep(0.02)  # Adjust typing speed
        message_placeholder.markdown(full_response + " |", unsafe_allow_html=True)

    return full_response

# Handle User Input
def handle_user_input():
    input_prompt = st.chat_input("Ask a legal question...")

    if input_prompt:
        st.session_state.messages.append({"role": "user", "content": input_prompt})

        with st.spinner("Thinking......."):
            try:
                response = mistral_client.chat(
                    model="mistral-tiny",
                    messages=[{"role": "user", "content": input_prompt}]
                )
                
                response_text = response.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't process your question.")
                
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                typing_effect(response_text)

            except Exception as e:
                st.error(f"Sorry, I couldn't process your question at the moment. Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't process your question at the moment. Please try again later."})

# Reset Button to Clear Chat
def reset_chat():
    if st.button('🗑 Reset Chat'):
        st.session_state.messages = []
        st.experimental_rerun()

# Main Function to Control Flow
def main():
    display_chat_history()
    handle_user_input()
    reset_chat()

# Run the main function
if __name__ == "__main__":
    main()
