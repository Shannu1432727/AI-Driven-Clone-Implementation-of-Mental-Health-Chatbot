import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import threading

st.set_page_config(page_title="My Innovation", layout="centered")

# Title
st.title("🤖 Cloud Implementation on Mental Health Chatbot")

# Project Introduction
st.header("📌 Project Overview")
st.markdown("""
This is a demo of my Python-based project. It uses **AI** and **Speech Recognition** to provide a mental health chatbot experience.
The goal is to **offer a supportive conversational AI that users can interact with via voice or text.**

Below, you can see how the code works in real-time.
""")

# --- SETUP ---

# Initialize Ollama model (e.g., llama3, mistral)
llm = ChatOllama(model="llama3.2")

# Prompt template
prompt = ChatPromptTemplate.from_template(
    "You are a friendly voice assistant. Respond naturally to user inputs. If the user suddenly changes the topic, handle it smoothly. User said: {input}"
)

# Global variables for TTS control
tts_thread = None
stop_tts = False

# Function to run TTS in a separate thread
def speak_text(text):
    global stop_tts
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.say(text)
    engine.runAndWait()
    if stop_tts:
        engine.stop()

# Recognizer for speech input
recognizer = sr.Recognizer()
mic = sr.Microphone()

# --- STREAMLIT UI ---
st.title("🤖 Mental Health Chatbot")
st.info("Speak or type your input.")

# Input method
st.subheader("Choose your input method:")
input_method = st.radio("How would you like to interact?", ["🎤 Speak", "⌨️ Type"], key="input_method")

user_input = ""

# Speech Input
if input_method == "🎤 Speak":
    if st.button("🎙️ Start Talking", key="start_talking_btn"):
        # Stop any ongoing TTS
        if tts_thread and tts_thread.is_alive():
            stop_tts = True
            # Attempt to stop the pyttsx3 engine cleanly
            try:
                engine = pyttsx3.init()
                engine.stop()
            except Exception as e:
                st.warning(f"Could not stop TTS engine cleanly: {e}")

        with st.spinner("Listening..."):
            try:
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
                    user_input = recognizer.recognize_google(audio)
                    st.success(f"You said: {user_input}")
            except sr.UnknownValueError:
                st.error("Sorry, I could not understand the audio. Please try again.")
                st.stop()
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; {e}")
                st.stop()
            except Exception as e: # Catch other potential errors during listening
                st.error(f"An error occurred during speech input: {e}")
                st.stop()

# Text Input
elif input_method == "⌨️ Type":
    user_input = st.text_input("Enter your message:", key="text_input")

# Response Handling
if user_input:
    # LangChain prompt and LLM response
    full_prompt = prompt.invoke({"input": user_input})
    response = llm.invoke(full_prompt)
    st.subheader("🤖 Assistant Response:")
    st.write(response.content)

    # Speak response using TTS
    with st.spinner("Speaking..."):
        stop_tts = False
        tts_thread = threading.Thread(target=speak_text, args=(response.content,))
        tts_thread.start()

    # Feedback section
    if st.button("👎 I didn't like this response", key="dislike_btn"):
        st.warning("Sorry to hear that. Tell me how I can improve or what you really meant.")
        follow_up = st.text_input("Your clarification or follow-up:", key="followup_input")
        if follow_up:
            st.info("Thanks! Let me respond again.")
            full_prompt = prompt.invoke({"input": follow_up})
            response = llm.invoke(full_prompt)
            st.subheader("🔁 Updated Response:")
            st.write(response.content)
            with st.spinner("Speaking updated response..."):
                stop_tts = False
                tts_thread = threading.Thread(target=speak_text, args=(response.content,))
                tts_thread.start()

# --- Your original code continues here, but with corrections and additions ---

# Display the main Python code (This seems to be a general code display section, not specific to the chatbot's internal logic)
st.header("### Chatbot Core Logic Example") # Changed header for clarity
code = '''
# Sample Code - Replace with your own logic
def greet(name):
    return f"Hello, {name}! Welcome to my app."
'''
st.code(code, language='python')

# Interactive Input (This section seems separate from the main chatbot interaction)
st.header("🎮 Try it Out (Simple Greeting)")
name = st.text_input("Enter your name:", key="greeting_name_input") # Changed label
if name:
    st.success(f"Hello, {name}! Welcome to my app.") # Use f-string for dynamic greeting

# Footer
st.markdown("---")
st.caption("Created by Rugada Shanmukha Vardhan")

