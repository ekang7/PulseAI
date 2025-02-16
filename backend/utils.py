from clients import mistral, perplexity
from db.vector_store import add_documents, query_documents
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def call_passive_perplexity(browser_info : str) -> None:
    overall_topic = mistral.get_topic(browser_info)
    related_topic_search = perplexity.get_related_topics(overall_topic.topic)
    related_topics_info = mistral.get_topics(related_topic_search.answer)

    documents = [f"Here is information about {topic.name}.\n" + topic.topic_information for topic in related_topics_info.topics]
    metadata = [{"topic" : topic.name} for topic in related_topics_info.topics]

    documents[0] = f"Here is information about {overall_topic.topic}.\n" + browser_info
    metadata[0] = {"topic" : overall_topic.topic}

    # log the topics of the addtional seraches
    logger.info(f"Found some extra information on the following topics: {', '.join([topic.name for topic in related_topics_info.topics])}")

    # Only add up to 3 additional items
    add_documents(documents[:min(len(documents),4)], metadata[:min(len(documents),4)])

def call_active_perplexity(question : str) -> None:
    topic = mistral.get_topic(question)
    db_results = query_documents(topic.topic, 3)

    related_topic_search = perplexity.get_related_topics_with_other_topics(topic.topic, [metadata["topic"] for metadata in db_results["metadatas"]])
    related_topics_info = mistral.get_topics(related_topic_search.answer)

    documents = [f"Here is information about {topic.name}.\n" + topic.topic_information for topic in related_topics_info.topics]
    metadata = [{"topic" : topic.name} for topic in related_topics_info.topics]

    logger.info(f"Found some extra information on the following topics: {', '.join([topic.name for topic in related_topics_info.topics])}")

    # Only add up to 3 additional items
    add_documents(documents[:min(len(documents),4)], metadata[:min(len(documents),4)])