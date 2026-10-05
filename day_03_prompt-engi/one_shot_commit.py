from openai import OpenAI
import os 
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


SYSTEM_PROMPT =  """ You write git commit messages in Conventional Commits 
format: type(scope): summary Types: feat, fix, docs, refactor, test, chore. 
The summary must be under 60 characters, in the imperative mood, with no period. 
Output only the commit message. 
Example: 
Change: Added a null check in the login handler because the app crashed when the email field was empty. 
Message: fix(auth): handle empty email in login 
Write the commit message for each change the user describes. """



changes =[  "fix the race condition issues in catalog service "   
        "No behavior change.",    
        "added email verification and password reset feature",  
        "updated readme added required dependencies.", 
    ]


def ask(system_prompt: str , user_text: str)->str:
    response = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text},
    ],
)

    return response.choices[0].message.content

for change in changes:
    print(ask(SYSTEM_PROMPT,change))