from clients import mistral, perplexity
from db.vector_store import add_documents, query_documents
""" 
Converts raw browser information (screenshot, url, title) into a string that 
represents the browser information to be used by the model.
"""

def call_passive_perplexity(browser_info : str) -> None:
    overall_topic = mistral.get_topic(browser_info)
    related_topic_search = perplexity.get_related_topics(overall_topic.topic)
    related_topics_info = mistral.get_topics(related_topic_search.answer)

    documents = [f"Here is information about {topic.name}.\n" + topic.topic_information for topic in related_topics_info.topics]
    metadata = [{"topic" : topic.name} for topic in related_topics_info.topics]

    # Only add up to 3 additional items
    add_documents(documents[:min(len(documents),4)], metadata[:min(len(documents),4)])

def call_active_perplexity(question : str) -> None:
    topic = mistral.get_topic(question)
    db_results = query_documents(topic.topic, 3, "default_collection")

    related_topic_search = perplexity.get_related_topics_with_other_topics(topic.topic, [metadata["topic"] for metadata in db_results["metadatas"]])
    related_topics_info = mistral.get_topics(related_topic_search.answer)

    print(related_topics_info.topics)
    documents = [f"Here is information about {topic.name}.\n" + topic.topic_information for topic in related_topics_info.topics]
    metadata = [{"topic" : topic.name} for topic in related_topics_info.topics]

    # Only add up to 3 additional items
    print(documents[0], metadata[0])
    add_documents(documents[:min(len(documents),4)], metadata[:min(len(documents),4)])


call_passive_perplexity("Google is a conglomerate specializing in technology.")
call_active_perplexity("What is a search engine?")

print(query_documents("Search Engine", 10)["metadatas"])