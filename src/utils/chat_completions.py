
import os
from textwrap import dedent
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORG_ID
)

MODEL = "gpt-4o"

# Step 1: Generate multiquery questions from a user question from different perspectives
def get_multiquery_questions(prompt, question):
    try:
        response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": dedent(prompt)
            },
            {
                "role": "user", 
                "content": dedent(question)
            }
        ],
        # We want some creativity here but not too much to keep the original intent
        temperature=0.5, 
        # With stuctured output we want to ensure always getting proper JSON format from the LLM
        response_format={ 
            "type": "json_schema",
            "json_schema": {
                "name": "multiquery_questions",
                "schema": {
                    "type": "object",
                    "properties": {
                        "original_query": {
                            "type": "string",
                            "description": "The original question provided by the user"
                        },
                        "variations": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Ten different variations of the original question"
                        }  
                    },
                    "required":["original_query", "variations"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return {str(e)}


# Step 2: Generate leetspeak variations of the multiquery questions
def get_leet_variations(prompt, question):
    try:
        response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": dedent(prompt)
            },
            {
                "role": "user", 
                "content": f"Generate 10 leetspeak variations of: {dedent(question)}"
            }
        ],
        # We want increased temperature here to get more creative with the leetspeak variations
        temperature=0.8,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "leet_variations",
                "schema": {
                    "type": "object",
                    "properties": {
                        "original": {
                            "type": "string",
                            "description": "The original question"
                        },
                        "leet_variations": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Ten leetspeak variations of the question"
                        }  
                    },
                    "required":["original", "leet_variations"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating leetspeak variations: {str(e)}")
        return {str(e)}


# Step 3: Generate the potentially harmful answers to the multiquery leetspeak variations
def get_harmful_answers(prompt, question):
    try:
        response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": dedent(prompt)
            },
            {
                "role": "user", 
                "content": f"Generate answer to: {dedent(question)}"
            }
        ],
        # Adjust the temperature here based on the preferred results
        temperature=0.8,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "leet_variations",
                "schema": {
                    "type": "object",
                    "properties": {
                        "leet_question": {
                            "type": "string",
                            "description": "The leetspeak question"
                        },
                        "leet_answer": {
                            "type": "string",
                            "description": "The leetspeak answer to the question"
                        }, 
                    },
                    "required":["leet_question", "leet_answer"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating leetspeak variations: {str(e)}")
        return {str(e)}
    

# Step 5: Process the jailbroken answers with our follow-up question to rest our case
def process_qa_with_follow_up(qa_data, new_question):
    conversation_history = {}
     # Process each QA pair
    for question_id, content in qa_data.items():
        # Initialize the messages list for this question_id
        conversation_history[question_id] = {
            "messages": [
                {"role": "user", "content": content['leet_question']},
                {"role": "assistant", "content": content['leet_answer']},
                {"role": "user", "content": f"Following up on the previous question and answer: {new_question}"}
            ]
        }
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=conversation_history[question_id]["messages"],
                temperature=0.5
            )
            # Add the new response to the conversation history
            conversation_history[question_id]["messages"].append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })   
        except Exception as e:
            print(f"Error processing question {question_id}: {str(e)}")
    return conversation_history


def continue_conversation(conversation_history, new_question):
    updated_conversations = {}
    for question_id, conv in conversation_history.items():
        # Copy existing messages
        updated_conversations[question_id] = {
            "messages": conv["messages"].copy()
        }
        updated_conversations[question_id]["messages"].append({
            "role": "user",
            "content": new_question
        })
        try:
            # Get response using the full conversation history plus new question
            response = client.chat.completions.create(
                model=MODEL,
                messages=updated_conversations[question_id]["messages"],
                temperature=0.5
            )
            updated_conversations[question_id]["messages"].append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })    
        except Exception as e:
            print(f"Error processing question {question_id}: {str(e)}")
    return updated_conversations