import openai


class OpenAIClient:

    def __init__(self, context, openai_key, model):
        self.context = context
        openai.api_key = openai_key
        self.model = model

    # Funktion, die den Prompt an OpenAI sendet und die Antwort zurückgibt
    def submit_prompt(self):
        prompt_instruction = "insert code where <insert Code here> is and return only the inserted code: "

        completion = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a Programmer who is an expert in the field of context-usage."},
                {"role": "user", "content": prompt_instruction + self.context},
            ],
            temperature=1.0,
        )
        return completion.choices[0].message
