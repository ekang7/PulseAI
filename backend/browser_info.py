from mistral_client import Mistral

from clients import mistral, perplexity

""" 
Converts raw browser information (screenshot, url, title) into a string that 
represents the browser information to be used by the model.
"""

def transform_browser_info(screenshot, url, title):
    ...

def info_to_related_topics(browser_info : str) -> mistral.TopicsResponse:
    overall_topic = mistral.get_topic(browser_info)
    related_topic_search = perplexity.get_related_topics(overall_topic.topic)
    related_topics = mistral.get_topics(related_topic_search.answer)

    return related_topics