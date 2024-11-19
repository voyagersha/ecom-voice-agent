E-Commerce Voice Agent

An interactive voice agent that navigates e-commerce websites when a URL is provided. The voice agent succinctly summarizes the website content and helps users navigate it, acting similarly to an in-person sales assistant in retail. Built with Python, Selenium, Speech Recognition, and OpenAI, this project aims to provide users with a seamless voice-based browsing experience.

Features

Voice Interaction: Users interact with the agent using voice commands, and the agent responds with relevant information and navigational actions.

Intelligent Summarization: The agent uses OpenAI's GPT model to summarize website content concisely, making it easier for users to understand what is available on the page.

Voice-Guided Navigation: The agent listens to user commands and navigates to relevant sections of the website, like "Go back," "Search for sofas," or "Navigate to home."

Project Structure

Web Scraping and Navigation: Uses Selenium to navigate e-commerce websites and extract data.

Speech Recognition: Implements speech_recognition library to capture user requests.

Text-to-Speech: Uses pyttsx3 for generating voice responses from the agent.

OpenAI Integration: Uses GPT-3.5 to help understand user requests and provide meaningful navigational actions.

Setup Instructions

Follow these steps to set up and run the voice agent locally using Cursor IDE.

Prerequisites

Ensure you have the following installed before proceeding:

Python 3.8+

Google Chrome Browser

ChromeDriver for Selenium (automatically managed via webdriver_manager)

You also need an API key from OpenAI to interact with GPT-3.5. Store this key as an environment variable named OPENAI_API_KEY.

1. Set Up Python Environment

Create a Virtual Environment:

Open your terminal in the Cursor IDE and run:

python -m venv venv

This will create a virtual environment named venv in your project folder.

Activate the Virtual Environment:

On Windows:

venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Upgrade pip:

pip install --upgrade pip

2. Install Required Packages

Run the following command to install the required dependencies:

pip install -r requirements.txt

Create a requirements.txt file with the following dependencies:

openai
requests
selenium
beautifulsoup4
html2text
pyttsx3
speechrecognition
webdriver_manager

3. Set Up Environment Variables

You will need to provide your OpenAI API key as an environment variable. In the Cursor IDE, create a .env file and add the following:

OPENAI_API_KEY=your_openai_api_key_here

Replace your_openai_api_key_here with your actual API key.

4. Run the Script

After setting up the environment and dependencies, run the script using the following command:

python ecom-voice-agent.py

The agent will load up the browser, navigate to the specified e-commerce site (in this example, https://www.livingspaces.com), and provide voice-based interaction.

How to Use

Once you run the script, the agent will load the provided URL and provide a very brief summary of the landing page.

You will then be prompted to use your voice to make requests such as:

"I want to buy a sofa"

"Navigate back"

"Go to the home page"

The agent will interpret your request and act accordingly, making the experience akin to interacting with a sales agent in a retail store.

Notes

Voice Commands: The agent might need clear and concise commands to work efficiently. If it doesn't understand, it will prompt you to try again.

Environment Path: Ensure that Chrome binary is set up properly in the code for macOS/Linux (/Applications/Google Chrome.app/Contents/MacOS/Google Chrome). Adjust the path if your Chrome installation differs.

Troubleshooting

Microphone Issues: Ensure your microphone is properly set up and accessible for the script to use.

API Key Issues: Double-check that your OpenAI API key is correct and accessible as an environment variable.

Browser Issues: ChromeDriver version mismatches can cause issues. The script uses webdriver_manager to automatically handle this, but keep your browser updated.

Contributing

Contributions are welcome! If you have ideas for improving the project, feel free to submit a pull request.