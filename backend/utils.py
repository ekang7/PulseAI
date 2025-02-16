from clients import mistral, perplexity
from typing import List
import asyncio

""" 
Converts raw browser information (screenshot, url, title) into a string that 
represents the browser information to be used by the model.
"""

def transform_browser_info(screenshot, url, title):
    ...

async def info_to_related_topics(browser_info : str) -> List[str]:
    overall_topic = mistral.get_topic(browser_info)
    related_topic_search = perplexity.get_related_topics(overall_topic.topic)
    related_topics = mistral.get_topics(related_topic_search.answer)

    related_topic_prompts = ["Tell me a bit about " + t.name + "." for t in related_topics.topics]
    results = await perplexity.get_multiple_search_responses(related_topic_prompts)

    return results