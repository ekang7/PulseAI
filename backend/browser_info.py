from mistral_client import Mistral


""" 
Converts raw browser information (screenshot, url, title) into a string that 
represents the browser information to be used by the model.
"""

def transform_browser_info(screenshot, url, title):
    