from bs4 import BeautifulSoup
import subprocess
import logging
import colorama
import requests
import openai
import time
import re
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")