# RAG = Retrieval-Augmented Generation
#
# This script 
# 1. retrieves 10 papers from Arxiv.org based on a search query QUERY_TEXT
# 2. uses openai api to create a numerical vector of each title
# 3. uses a local paper.csv as a vector storage
# 4. summarized and returns the paper summaries with urls... by their semantic equivalence to the QUERY_TEXT

# TO USE: simply change this and run python3 rag.py
QUERY_TEXT = "Are there papers about using CrewAI to automate repetive jobs at work?"

from openai import OpenAI
from scipy import spatial
import arxiv
from csv import writer
import pandas as pd
import json

from dotenv import load_dotenv
# load environment variables from .env file
load_dotenv()

client = OpenAI()

def embedding_request(text): 
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text)
    return response

def relatedness_function(a, b):
    return 1 - spatial.distance.cosine(a, b)

def get_articles(query):
    client = arxiv.Client()
    search = arxiv.Search(
        query = query,
        max_results=10
    )
    results_list = []

    # this ensure the contents of paper.csv is completely empty
    with open("paper.csv", "w") as f_object:
        writer_object = writer(f_object)
        f_object.close()


    for result in client.results(search):
        result_dict = {}
        result_dict.update({'title': result.title})
        result_dict.update({'summary': result.summary})
        result_dict.update({'article_url': [x.href for x in result.links][0]})
        result_dict.update({'pdf_url': [x.href for x in result.links][1]})
        results_list.append(result_dict)

        title_embedding = embedding_request(result.title).data[0].embedding
        row = [
            result.title,
            result.summary,
            result_dict['pdf_url'],
            title_embedding
        ]

        with open('paper.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(row)
            f_object.close()

    return results_list


# cow_embedding = embedding_request("A cow gently mooing under the morning sun in a peaceful pasture.").data[0].embedding
# dog_embedding = embedding_request("A dog is gently barking under the morning sun in a peaceful mannor.").data[0].embedding
# quantom_embedding = embedding_request("Quantum computing promises to revolutionize data encryption and processing speeds.").data[0].embedding

# print(get_articles('LLM applications via multiple agents'))

def titles_ranked_by_relatedness(query):
    query_embedding = embedding_request(query).data[0].embedding
    df = pd.read_csv('paper.csv', header=None)
    strings_and_relatedness = [
        (row[0], row[1], row[2], relatedness_function(query_embedding, json.loads(row[3]))) for i, row in df.iterrows()
    ]

    strings_and_relatedness.sort(key=lambda x: x[3], reverse=True)
    #strings, relatedness = zip(*strings_and_relatedness)

    return strings_and_relatedness

def fetch_articles_and_return_summary(description):
    get_articles(description)
    return titles_ranked_by_relatedness(description)

# TODO: move this into tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_articles_and_return_summary",
            "description": "Use this function to fetch papers and provide a summary for users",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Some keywords that can be used for an Arxiv search"
                    }
                },
                "required": ["keywords"]
            }
        }
    }
]


chat_completion = client.chat.completions.create(messages = [
    {
        "role": "user",
        "content": QUERY_TEXT
    }
],
model="gpt-3.5-turbo",
tools=tools
)

tool_call = chat_completion.choices[0].message.tool_calls[0]
function_name = tool_call.function.name
arguments = tool_call.function.arguments
# to test the tool call for chatgpt
#print (tool_call)

# to test the arxiv side
#print(fetch_articles_and_return_summary("AutoGen"))

if function_name == 'fetch_articles_and_return_summary':
    results = fetch_articles_and_return_summary(json.loads(arguments)['keywords'])
    for i, result in enumerate(results, start=1):
        title, summary, url, score = result #unpack the result assuming it's a tuple
        result_str = (
            f"Results {i}:\n"
            f"Title: {title}\n"
            f"Summary: {summary}\n"
            f"URL: {url}\n"
            f"Relatedness Score: {score:.2f}\n"
            f"{'-' * 40}" #divider for readability
        )
        print(result_str)

