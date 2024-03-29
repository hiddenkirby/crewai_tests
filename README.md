# crewai_tests

(python 3.10.8)

## to get the code env setup

1. run `python3 -m venv .venv`
2. kill vscode terminal
3. right click ollama_test.py and choose run (it wont successfully run if you don't have Ollama running locally)
4. now you can `pip install -r requirements.txt`
5. finally you need to setup your .env file with all the appropriate api keys

```
OPENAI_API_KEY=""
OPENAI_API_BASE_URL="https://api.openai.com/v1"
#MODEL_NAME="gpt-3.5-turbo"
MODEL_NAME="gpt-4"
OPENAI_ORG_ID=""
SERPER_API_KEY=""
GEMINI-API-KEY=""
EXA_API_KEY=""
```

## to spin up Ollama

1. go to ollama.ai and download it
2. install it
3. open a new terminal
4. run `ollama run mistral` (replace mistral with any model you want to use)
5. find models at https://ollama.ai/library

## to chat with local Ollama LLM

1. first spin up Ollama with a model
2. right click ollama_test.py and click run
3. go to http://127.0.0.1:7860 in your browser

## to spin up privateGPT locally

1. back out or leave this project directory

```
git clone https://github.com/imartinez/privateGPT && cd privateGPT && \
python3.11 -m venv .venv && source .venv/bin/activate && \
pip install --upgrade pip poetry && poetry install --with ui,local && ./scripts/setup

# Launch the privateGPT API server **and** the gradio UI
poetry run python3.11 -m private_gpt

# In another terminal, create a new browser window on your private GPT!
open http://127.0.0.1:8001/
```

2. default is using mistral and the embedding model - converts text into vector storage (chromdb)

## to spin up a local UI that uses chatgpt api to write sql and query a local sqlite3 db (under data/)

1. ensure vevn and requirements are installed (see above)
2. run `streamlit run example_openai_sql.py`
