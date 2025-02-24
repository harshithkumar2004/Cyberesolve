import os
import time
import streamlit as st
import google.generativeai as genai

# Streamlit Page Configuration
st.set_page_config(page_title="Cyberesolve", layout="centered")

# Hide hamburger menu and footer (UI optimization)
def hide_hamburger_menu():
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

hide_hamburger_menu()

# Header Section with logo
st.image("cyber.png", use_container_width=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini API
def initialize_genai(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Error initializing the Gemini API model: {str(e)}")
        st.stop()

# Load Gemini Model
genai_model = initialize_genai(api_key=os.getenv("GOOGLE_API_KEY"))  # Replace YOUR_API_KEY with actual API key

# Display Chat History
def display_chat_history():
    for message in st.session_state.messages:
        if message.get("role") == "user":
            st.chat_message("user").write(message.get("content"))
        else:
            st.chat_message("assistant").write(message.get("content"))

# Simulate typing effect for a better user experience
def typing_effect(response):
    full_response = "⚠ *Be specific about the topic while you query* \n\n\n"
    message_placeholder = st.empty()

    if response and hasattr(response, 'text'):
        for chunk in response.text:
            full_response += chunk
            time.sleep(0.02)  # Adjust typing speed
            message_placeholder.markdown(full_response + " |", unsafe_allow_html=True)
    else:
        st.error("Invalid response format.")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't process your question at the moment. Please try again later."})

    return full_response

# User Input Handling
def handle_user_input():
    input_prompt = st.chat_input("Ask a legal question...")

    if input_prompt:
        st.session_state.messages.append({"role": "user", "content": input_prompt})

        with st.spinner("Thinking......."):
            try:
                result = genai_model.generate_content(input_prompt)
                response = result if result else {"text": "Sorry, I couldn't process your question. Please try again."}

                st.session_state.messages.append({"role": "assistant", "content": response.text or "Sorry, I couldn't process your question. Please try again."})

                typing_effect(response)

            except Exception as e:
                st.error(f"Sorry, I couldn't process your question at the moment. Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't process your question at the moment. Please try again later."})

# Reset Button
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
