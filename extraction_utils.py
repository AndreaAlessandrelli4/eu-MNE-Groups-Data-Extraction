import json, os
import os
import warnings
warnings.filterwarnings("ignore")
from openai import OpenAI




# ChatGPT: Request to chatGPT to check the information and extract

# SYSTEM PROMPT for ChatGPT
SYSTEM_PROMPT = "You are an information extraction assistant specialized in processing content from corporate documents.\nYou will recive an url, a snippet and a Markdown documents or Markdown snippets related to multinational companies.\nYour task is to analyze all the input information. These documents are sourced from the web using `crawl4ai`, a Python library for web crawling and content extraction.\nYour goal is to extract the specific information requested, based on the target field provided in the input.\n\nYou must return the extracted information strictly following the schema provided. If the information is not present or cannot be confidently determined from the input, do not hallucinate—return `null` as the value.\nDo not include any explanations, comments, or additional text.\nBe precise, concise, and only return structured data."


# Function to interact with ChatGPT for information extraction
def ask_chatgpt(link, markdown, user_prompt, max_tok=100, model="gpt-4o-mini", sys = SYSTEM_PROMPT, key = os.getenv("OPENAI_API_KEY")):
    if len(markdown) >1:
        try:
            client = OpenAI(api_key=key)
            # Construct the prompts
            prompts = user_prompt+f"\n\nINPUT:\nCOMPANY NAME:\n{link['company_name']}\nURL:\n{link['url']}\n\nSNIPPET:\n{link['text_snippet']}\n\nMARKDOWN:\n{markdown}"
            # Send request to OpenAI API
            response = client.chat.completions.create(
                model=model,
                temperature=0,
                max_tokens=max_tok,
                messages=[
                    {"role": "system", "content": sys},
                    {"role": "user", "content": prompts}
                ],
            )
            # Extract and return the response content
            res = response.choices[0].message.content
            return res.strip()
        
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return 'null'



