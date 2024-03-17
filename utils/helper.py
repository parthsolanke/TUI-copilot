from bs4 import BeautifulSoup
import requests
import colorama
import logging
import openai
import time
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.WARNING)

def query_chat_gpt_3_5(
    message_history: list,
    model="gpt-3.5-turbo",
    max_retries=15,
    sleep_time=2
    ) -> str:
    """
    Queries the GPT-3.5 Turbo model with a given message history and returns the response content.

    Args:
        message_history (list): A list of messages exchanged in the conversation.
        model (str, optional): The GPT-3.5 Turbo model to use. Defaults to "gpt-3.5-turbo".
        max_retries (int, optional): The maximum number of retries in case of failure. Defaults to 15.
        sleep_time (int, optional): The sleep time between retries in seconds. Defaults to 2.

    Returns:
        str: The content of the response from the GPT-3.5 Turbo model.

    Raises:
        Exception: If the maximum number of retries is exceeded without a successful response.
    """
    
    DEBUG = True
    retries = 0
    logger = logging.getLogger()
    
    logger.info(f"Message history: {message_history}")
    
    if DEBUG:
        print(colorama.Fore.MAGENTA + colorama.Style.DIM + "Message HIstory: " + str(message_history) + colorama.Style.RESET_ALL)
        
    while retries < max_retries:
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=message_history
            )
            content = response.choices[0].message.content
            if content:
                return content
        except Exception as e:
            logger.warning(f"Error during query_chat_gpt_3_5(): {e}")
            retries += 1
            time.sleep(sleep_time)
    
    raise Exception("Maximum retries exceeded")


def extract_paragraphs(url: str):
    """
    Extracts paragraphs from the given URL.

    Args:
        url (str): The URL to extract paragraphs from.

    Returns:
        str: The extracted paragraphs, separated by two newlines.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs: str = ''

    for paragraph in soup.find_all('p'):
        paragraphs += paragraph.text + '\n\n'
    return paragraphs