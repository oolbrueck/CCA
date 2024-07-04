import os
import openai
from openai import OpenAI

# Setzen der Umgebungsvariable im Skript (nur für das Beispiel)
os.environ["OPENAI_API_KEY"] = "sk-proj-MzvNgAHh1QSA1e9R0OELT3BlbkFJhzvvRnZegqPx3jscg2ea"

# Initialisierung des Clients
openai.api_key = os.environ.get("OPENAI_API_KEY")

class OpenAIClient:

    def __init__(self, context):
        self.context = context


    def submitPrompt(self):
        print("insert code where <insert Code here> is written: " + self.context)
        client = OpenAI()
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="insert code where <insert Code here> is written: " + self.context,
            max_tokens=100
        )
        return response.choices[0].text.strip()




