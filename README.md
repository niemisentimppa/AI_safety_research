# 'Best-of-N' Jailbreaking of ChatGPT (gpt-4o)

## Purpose

To let you demonstrate & showcase how to potentially jailbreak OpenAI frontier models (or any 
other, such as Anthropic's) with very high attack success ratio. 

This is done with the help of LLM itself by chain prompting it in multiple steps to get 
variations of the original question, and as final step 'shotguning' the questions to 
LLM one by one ('Best-of-N jailbreaking').

- Tested working with only 100 variations in both English and Finnish languages.

## Installation

- clone the repository or download the files

- use virtual environment

python3 -m venv .
source ./bin/activate

- install required libraries

python3 -m pip install pip
pip install setuptools wheel
pip install python-dotenv openai 


## Requirements

- OPENAI_API_KEY (+ OPENAI_ORG_ID)
  - Stored in project root in .env file
  - Get yours from OpenAI API account
- Some $ in your OpenAI account

- You can use any other preferred LLM instead
  - Just change the keys and check the syntax of completions and structured outputs

## Usage

1. Enter your question to it's place in code.

2. Adjust the prompts however you see best, if needed.

3. Enter your paths to store the interim & final results.

4. Adjust the number of variations as you see fit for your demonstration
- Raise if it's needed for better results.

5. Run the code with 'python3 jailbreaking_chatgpt.py'. 
- Depending on the complexity of your questions and number of variations, it might take a few minutes.

6. Check the results from the prints & your files.

## Further study

I might add some other methods & techniques later to this repository, e.g. how to further chain use LLM for 
improved results.

Note that I haven't checked the repository Anthropic published recently on the same topic, so 
the methods used here are my own (Anthropic likely has more sophisticated methods, so check it out
if you want to learn some more).

## License

MIT License. Use for educational purposes & own responsibility.