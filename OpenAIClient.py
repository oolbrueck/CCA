import openai
from openai import OpenAI


class OpenAIClient:

    def __init__(self, context, openai_key):
        self.context = context
        openai.api_key = openai_key

    def submit_prompt(self):
        # create two variables, one for the substring in self.context that ist before <insert Code here>, and the other for the substring after <insert Code here>
        before = self.context.split("<insert Code here>")[0]
        after = self.context.split("<insert Code here>")[1]

        print("before: ", before)
        print("after: ", after)

        client = OpenAI()
        # response = client.completions.create(
        #     model="gpt-3.5-turbo-instruct",
        #     prompt=before + "\n" + "//insert Code here",
        #     suffix=after,
        #     max_tokens=100
        # )
        # return response.choices[0].text.strip()
        # completion = openai.chat.completions.create(
        #     model="gpt-3.5-turbo-0125",
        #     messages=[
        #         {"role": "system", "content": "You are a Programmer who is an expert in the field of context-usage."},
        #         {"role": "user", "content": "insert code where <insert Code here> is and return only the inserted code: " + self.context}
        #     ]
        # )
        prompt_instruction = "insert code where <insert Code here> is and return only the inserted code: "

        completion = openai.chat.completions.create(
            model="GPT-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a Programmer who is an expert in the field of context-usage."},
                {"role": "user", "content": prompt_instruction + self.context},
            ],
            temperature=1.0,
        )
        print("completion: ", completion)
        return completion.choices[0].message
