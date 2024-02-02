# crewai_tests

(python 3.10.8)

## to get the code env setup

1. run `python3 -m venv .venv`
2. kill vscode terminal
3. right click ollama_test.py and choose run (it wont successfully run if you don't have Ollama running locally)
4. now you can `pip install`
5. finally you need to setup your .env file with all the appropriate api keys

```
OPENAI_API_KEY=""
OPENAI_API_BASE_URL="https://api.openai.com/v1"
#MODEL_NAME="gpt-3.5-turbo"
MODEL_NAME="gpt-4"
OPENAI_ORG_ID=""
SERPER_API_KEY=""
GEMINI-API-KEY=""
```

## to spin up Ollama

1. go to ollama.ai and download it
2. install it
3. open a new terminal
4. run `ollama run mistral` (replace mistral with any model you want to use)
5. find models at https://ollama.ai/library

## to chat with local Ollama LLM

1. <first spin up Ollama with a model>
2. right click ollama_test.py and click run
3. go to http://127.0.0.1:7860 in your browser
