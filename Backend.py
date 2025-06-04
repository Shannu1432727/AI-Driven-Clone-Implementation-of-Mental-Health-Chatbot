import speech_recognition as sr
import win32com.client as wincl
import ollama
import time
import random # For varied human-like phrases

# --- Configuration ---
OLLAMA_MODEL = "llama3.2"  # Replace with the Ollama model you've pulled (e.g., "llama2", "mistral")
TEMPERATURE = 0.7          # Adjust for creativity (higher) or predictability (lower)

# --- Initialize Speech Recognition and Text-to-Speech ---
r = sr.Recognizer()
try:
    speaker = wincl.Dispatch("SAPI.SpVoice")
except Exception as e:
    print(f"Error initializing text-to-speech: {e}")
    print("Please ensure 'pywin32' is installed and SAPI is configured correctly.")
    speaker = None # Set speaker to None if initialization fails

# --- Human-like listening prompts ---
listening_prompts = [
    "I'm here, ready to listen...",
    "Please tell me what's on your mind.",
    "I'm listening closely...",
    "Go ahead, I'm all ears.",
    "I'm ready when you are.",
    "What would you like to talk about?"
]

# --- Human-like processing prompts ---
processing_prompts = [
    "Just a moment, let me think about that...",
    "Understood, processing...",
    "Let me consider that for a moment...",
    "Taking that in...",
    "Hmm, reflecting on your words..."
]

def speak(text):
    """Converts text to speech using SAPI."""
    print(f"Assistant: {text}")
    if speaker: # Only speak if speaker was initialized successfully
        speaker.Speak(text)
    else:
        print("(Text-to-speech is unavailable)")

def listen():
    """Listens for audio input from the microphone and converts it to text."""
    with sr.Microphone() as source:
        print(random.choice(listening_prompts))
        # Significantly reduced adjustment duration for faster start
        r.adjust_for_ambient_noise(source, duration=0.2)
        try:
            # Crucial for capturing full sentences; 8 seconds is a good balance
            audio = r.listen(source, phrase_time_limit=8)
            print(random.choice(processing_prompts))
            text = r.recognize_google(audio) # Using Google Web Speech API for recognition
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't quite catch that. Could you please repeat?")
            speak("I didn't quite catch that. Could you please repeat?")
            return ""
        except sr.RequestError as e:
            print(f"I'm having trouble with my listening service right now. Please check your internet connection. Error: {e}")
            speak("I'm having trouble with my listening service right now. Please check your internet connection.")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred during listening: {e}")
            speak("An unexpected error occurred while I was trying to listen. Could you try again?")
            return ""

def get_ollama_response(messages):
    """Sends prompt and conversation history to Ollama and returns the response."""
    try:
        # Ensures a complete response is waited for (non-streaming)
        response = ollama.chat(model=OLLAMA_MODEL, messages=messages, options={'temperature': TEMPERATURE}, stream=False)
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"Ollama API Error: {e}")
        return "It seems there was an issue with the Ollama model. Please check the server logs."
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return "I'm really sorry, but I'm having trouble connecting to the language model right now. Please make sure your Ollama server is running and try again."

def main():
    print("Welcome to your Emotional Support Assistant.")
    print("Say 'exit' or 'quit' anytime you're ready to end our chat.")

    # Initialize conversation history with the system message once
    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are a compassionate, empathetic, and supportive AI assistant designed to listen "
                "and provide understanding. Focus on active listening, validation of feelings, and "
                "offering gentle encouragement. Avoid giving direct advice unless specifically asked. "
                "Your goal is to create a safe space for the user to express themselves. "
                "Use warm, reassuring, and thoughtful language. Respond as a supportive friend."
            )
        }
    ]

    initial_greeting = "Hello there. I'm here to listen, whatever you're going through. How are you feeling right now?"
    speak(initial_greeting)

    while True:
        user_input = listen()

        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            speak("Thank you for sharing with me. Remember, you're not alone. Take care.")
            break

        if user_input:
            # Append user message to history
            conversation_history.append({"role": "user", "content": user_input})

            # Record start time for response calculation
            start_time = time.time()

            response = get_ollama_response(conversation_history)
            speak(response)

            # Record end time and print response duration
            end_time = time.time()
            print(f"Response time: {end_time - start_time:.2f} seconds")

            # Append assistant response to history
            conversation_history.append({"role": "assistant", "content": response})

        # No time.sleep here for maximum speed.
        # If SAPI speaking overlaps with the next "listening prompt" print, it's generally fine.

if __name__ == "__main__":
    main()