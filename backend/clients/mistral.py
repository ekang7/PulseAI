from pydantic import BaseModel
from mistralai import Mistral
from dotenv import load_dotenv
import os
from typing import List
import simplejson as json

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "ministral-8b-latest"

client = Mistral(api_key=MISTRAL_API_KEY)

class TopicResponse(BaseModel):
    topic : str

def get_topic(text : str) -> TopicResponse | None:
    """
    Return the topic of the text. Differs from get_summary by only stating the topic, not in full sentences.
    """
    global client
    
    
    chat_response = client.chat.parse(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": "Return the topic of the user's statement. This should be a term or phrase, not a complete sentence."
            },
            {
                "role": "user", 
                "content": "## Mean Squared Error (MSE) Explained\n\nMean Squared Error (MSE) is a statistical measure used to evaluate the accuracy of an estimator or a predictive model. It quantifies the average squared difference between the estimated values (predictions) and the actual values (observations).\n\n### Calculation\n\nThe formula for MSE is:\n\n\\[ \\text{MSE} = \\frac{1}{n} \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2 \\]\n\nWhere:\n- \\( n \\) is the number of observations.\n- \\( y_i \\) is the actual observed value.\n- \\( \\hat{y}_i \\) is the predicted value.\n- The summation runs over all observations.\n\n### Interpretation\n\n- **Positive Values**: MSE is always non-negative, with lower values indicating better model performance. An MSE of zero implies perfect predictions, which is rarely achievable in practice[1][2].\n- **Sensitivity to Outliers**: Because errors are squared, larger errors have a disproportionately large impact on the MSE, making it sensitive to outliers[5].\n- **Units**: The units of MSE are the square of the units of the original data, which can make interpretation less intuitive compared to other metrics like Root Mean Squared Error (RMSE)[2].\n\n### Applications\n\n- **Model Evaluation**: In regression analysis and machine learning, MSE is used to assess how well a model predicts outcomes by comparing predicted values against actual data[5].\n- **Comparative Analysis**: MSE allows for comparing different models or estimators. A lower MSE indicates a model that better fits the data[4].\n- **Optimization**: In algorithms like gradient descent, minimizing MSE helps in finding optimal model parameters[1].\n\n### Limitations\n\n- **Scale Dependency**: The magnitude of MSE depends on the scale of the target variable, making it difficult to compare across different datasets without normalization.\n- **Bias and Variance Trade-off**: MSE incorporates both variance and bias components of an estimator, which can complicate its interpretation when analyzing model performance[1][3]."
            },
            {
                "role": "assistant",
                "content": "Mean Squared Error (MSE)"
            },
            {
                "role": "user",
                "content": "## Alan Turing\'s Role in Computer Science\n\nAlan Turing is widely regarded as one of the founding figures of computer science, with several key contributions that have had a lasting impact on the field.\n\n### **The Turing Machine**\n\n- In 1936, Turing introduced the concept of the Turing Machine in his paper 'On Computable Numbers, with an Application to the Entscheidungsproblem.' This theoretical machine laid the groundwork for modern computing by providing a formalization of the concepts of algorithm and computation[3][9]. The Turing Machine is a simple abstract device that manipulates symbols on a strip of tape according to a set of rules. It is capable of simulating the logic of any computer algorithm, making it a fundamental model for understanding computation[4].\n\n### **Cryptanalysis and World War II**\n\n- During World War II, Turing played a crucial role in breaking German ciphers, particularly those encrypted by the Enigma machine. He developed an electromechanical device known as the Bombe, which significantly enhanced the Allies\' ability to decode Enigma-encrypted messages[2][4]. His work at Bletchley Park was pivotal in deciphering German naval communications, contributing to the Allied victory in the Battle of the Atlantic[5].\n\n### **The Turing Test**\n\n- In 1950, Turing proposed what is now known as the Turing Test in his paper 'Computing Machinery and Intelligence.' The test was designed to assess a machine\'s ability to exhibit intelligent behavior indistinguishable from that of a human. This concept has been foundational in artificial intelligence research and continues to influence discussions about machine intelligence today[1][7].\n\n### **Legacy**\n\n- Beyond these contributions, Turing\'s work on computability theory and his proof of the Halting Problem have been instrumental in shaping theoretical computer science[4]. Despite facing significant personal challenges and discrimination during his lifetime, Turing\'s innovations continue to influence modern technology and computing."
            },
            {
                "role": "assistant",
                "content": "Alan Turing's Role in Computer Science"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        response_format=TopicResponse,
        temperature=0
    )
    try:
        output = json.loads(chat_response.choices[0].message.content)
        return TopicResponse(**output)
    except Exception as e:
        print(e)
        return None


class Topic(BaseModel):
    name : str
    topic_information : str
class TopicsResponse(BaseModel):
    topics : List["Topic"]

def get_topics(text : str) -> TopicsResponse | None:
    """
    Return multiple topics from a text.
    """
    global client
    
    
    chat_response = client.chat.parse(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": "Return the key topics of the user's statement. Topic names should be descriptive and not abbreviations; they should be interpretable when taken out of context. For example, text about Shakespeare that talks about his birth should have topic name \"Shakespeare's Birth\" instead of just \"Birth\". Topic information should be the information pertaining to each topic."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        response_format=TopicsResponse,
        temperature=0
    )
    try:
        output = json.loads(chat_response.choices[0].message.content)
        return TopicsResponse(**output)
    except:
        return None

def get_summary(text : str) -> str:
    """
    Returns a summary of the text using Mistral
    """
    chat_response = client.chat.complete(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": "Your job is to summarize the user's input, focusing on key details, concepts, and methods."
            },
            {
                "role": "user", 
                "content": text
            },
        ],
        temperature=0
    )
    try:
        output = chat_response.choices[0].message.content
        return output
    except Exception as e:
        raise e

if __name__ == "__main__":
    print(get_topic(": Here's an overview of Stanford University and adjacent topics in a bulleted list format:\\\\- **History and Founding**: Stanford University was founded in 1885 by Leland and Jane Stanford in memory of their son, Leland Stanford Jr. It officially opened in 1891 as a coeducational and non-denominational institution[1][3].\\\\- **Academic Programs**: The university is organized into seven schools, including the School of Engineering, School of Humanities and Sciences, and the Graduate School of Business. It offers a wide range of undergraduate and graduate programs, with a strong emphasis on research and interdisciplinary studies[2][4].\\\\- **Research and Innovation**: Stanford is classified as an R1: Doctoral Universities – Very high research activity institution. It is home to numerous research centers and institutes, such as the SLAC National Accelerator Laboratory and the Hoover Institution. The university's research expenditure is substantial, contributing to its reputation as a hub for innovation[1][5].\\\\- **Campus Life**: The campus spans 8,180 acres, featuring a mix of historical and modern architecture. Students have access to over 650 student organizations, a vibrant athletic scene, and a residential housing system designed to foster community[2][5].\\\\- **Silicon Valley Connection**: Stanford's proximity to Silicon Valley has fostered a culture of entrepreneurship and innovation. The university's research park, established in 1951, is credited with helping to spur the development of Silicon Valley[1][3].\\\\- **Notable Alumni and Impact**: Stanford alumni include numerous Nobel laureates, billionaires, and leaders in technology and politics. The university's graduates have played significant roles in founding companies like Google, Yahoo!, and Hewlett-Packard[1][3].\\\\- **Location and Climate**: Located in the Bay Area of Northern California, Stanford benefits from a mild climate, offering students opportunities for outdoor activities and access to cultural and technological hubs like San Francisco[2][3]."))