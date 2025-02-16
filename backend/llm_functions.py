from typing import List, Dict, Any
from mistral_client import get_completion

def summarize_results_with_mistral(results: List[Dict[Any, Any]]) -> str:
    """
    Summarize a list of database results using Mistral AI.
    
    Args:
        results: List of dictionary results from the database
        
    Returns:
        str: Summarized response from Mistral
    """
    # Create a structured prompt from the results
    formatted_results = "\n".join([str(result) for result in results])
    
    system_prompt = """
    <system_prompt>
    You are a highly capable Large Language Model whose primary goal is to summarize information in a concise, accurate, and contextually aware way.

    You will receive:
    1. A list of search results (RAG) from a knowledge base, with each entry corresponding to information from a web page that a user has visited.

    <your_task>
        - Summarize and synthesize the information from the provided search results, focusing on important details and accuracy.
        - Provide a section with a brief overview and a section with more details.
    </your_task>

    <guidelines>
        - Do not invent facts or details not found in the search results.
        - Maintain important nuances. If multiple search results provide contradictory information, include the contradiction or uncertainty.
        - Present the answer clearly and in a helpful format.
    </guidelines>

    </system_prompt>
    """
    
    user_prompt = f"""
    <relevant_search_results>
    Summarize these:
    {formatted_results}
    </relevant_search_results>
    """
    
    # Get completion from Mistral
    response = get_completion(system_prompt, user_prompt)
    
    # Parse and return the response
    return response.choices[0].message.content

test_dict = test_results = [
    {
        "source": "Stack Overflow",
        "url": "https://stackoverflow.com/q/123456",
        "content": "If you're running into a TypeError in Python when using pandas, it's likely that your DataFrame contains mixed types. You can use df.dtypes to check the data types of each column. Try converting them explicitly using df['col_name'] = df['col_name'].astype(str)."
    },
    {
        "source": "Official Pandas Documentation",
        "url": "https://pandas.pydata.org/docs/user_guide/missing_data.html",
        "content": "Pandas provides multiple ways to handle missing data, including fillna(), dropna(), and interpolation methods. Use df.fillna(value) to replace missing values with a specified value, or use df.dropna() to remove rows with missing data."
    },
    {
        "source": "GitHub Issues",
        "url": "https://github.com/pandas-dev/pandas/issues/54321",
        "content": "Users have reported that recent changes in pandas v1.5 may cause compatibility issues when using older versions of numpy. The recommended fix is to upgrade numpy to the latest stable release using pip install --upgrade numpy."
    }
]

print(summarize_results_with_mistral(test_dict))