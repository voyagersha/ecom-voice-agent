# an e-commerce voice agent to navigate websites when a url is provided. voice agent succinctly summarizes the website and helps users navigate it similar to an in-person sales agent in retail

import time
import speech_recognition as sr
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import html2text
import pyttsx3
from openai import OpenAI
import os

# Set OpenAI API key using environment variable
client = OpenAI(
    api_key="yourkey")

# Initialize the text-to-speech engine
def init_tts():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    return engine

def speak_text(engine, text):
    engine.say(text)
    engine.runAndWait()

# Setting up Selenium to open Chrome Browser
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # Ensure correct Chrome path
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to get user input via voice
def get_user_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your request...")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            print(f"User said: {user_input}")
            return user_input.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""

# Extract website content and convert to Markdown
def extract_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    converter = html2text.HTML2Text()
    converter.ignore_links = False  # Keep links
    markdown = converter.handle(str(soup))
    return markdown

# Summarize website content to remove noise and provide a concise summary
def summarize_content(content):
    lines = content.splitlines()
    summary = []
    heading_count = 0
    max_headings = 5  # Limit number of headings to avoid overwhelming user

    for line in lines:
        if line.strip():
            # Extract relevant headings only and avoid URLs and excessive content
            if line.startswith("#") and heading_count < max_headings:
                summary.append(line.strip())
                heading_count += 1
            elif heading_count >= max_headings:
                break
    if not summary:
        summary.append("This page contains various sections such as products, categories, and information.")
    return " ".join(summary)

# Function to understand the user's intent using OpenAI API
def classify_intent(user_input):
    prompt = f"The user said: \"{user_input}\". What does the user want to do? Please classify the intent into one of these categories: 'navigate_back', 'navigate_home', 'search', 'navigate_link', or 'unknown'. Provide a brief explanation of what action to take."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=50, temperature=0.5
        )
        intent_response = response.choices[0].message.content.strip().lower()
        if "navigate_back" in intent_response:
            return "navigate_back"
        elif "navigate_home" in intent_response:
            return "navigate_home"
        elif "search" in intent_response:
            return "search"
        elif "navigate_link" in intent_response:
            return "navigate_link"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "unknown"

def navigate_website(driver, engine, url):
    # Go to the provided URL
    driver.get(url)
    time.sleep(3)

    # Extract and summarize website content
    extracted_content = extract_website_content(url)
    summarized_content = summarize_content(extracted_content)

    # Provide a quick summary of the landing page
    speak_text(engine, "Here is a brief summary of what is available on this page.")
    print(summarized_content)  # Optional: Print for reference
    speak_text(engine, summarized_content)

    # Wait for user input
    while True:
        user_request = get_user_input()
        if user_request:
            intent = classify_intent(user_request)

            if intent == "navigate_back":
                speak_text(engine, "Navigating back to the previous page.")
                driver.back()
            elif intent == "navigate_home":
                speak_text(engine, "Navigating back to the home page.")
                driver.get(url)
            elif intent == "search":
                speak_text(engine, f"Searching based on your request for {user_request}.")
                search_keywords = user_request.replace("search for", "").strip().split()
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    link_text = link.text.lower()
                    if all(keyword in link_text for keyword in search_keywords):
                        link.click()
                        time.sleep(3)
                        speak_text(engine, f"You are now in the section related to {user_request}. How else can I assist you?")
                        break
                else:
                    speak_text(engine, "I couldn't find a direct link matching your request. Could you please try again or provide more details?")
            elif intent == "navigate_link":
                speak_text(engine, f"Navigating based on your request for {user_request}.")
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    link_text = link.text.lower()
                    if all(keyword in link_text for keyword in user_request.split()):
                        link.click()
                        time.sleep(3)
                        speak_text(engine, f"You are now in the section related to {user_request}. How else can I assist you?")
                        break
                else:
                    speak_text(engine, "I couldn't find a direct link matching your request. Could you please try again or provide more details?")
            else:
                speak_text(engine, "I'm not sure how to assist with that request. Could you try asking in a different way?")
        else:
            speak_text(engine, "I didn't understand. Please try asking again.")

if __name__ == "__main__":
    # Initialize TTS engine
    tts_engine = init_tts()

    # Setup the Chrome WebDriver
    driver = setup_driver()
    
    try:
        # Start navigating the website
        navigate_website(driver, tts_engine, "https://www.livingspaces.com")
    finally:
        # Clean up and close the driver
        driver.quit()
