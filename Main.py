# import os
# import openai
#
# # Setzen der Umgebungsvariable im Skript (nur für das Beispiel)
# os.environ["OPENAI_API_KEY"] = "KEY"
#
# # Initialisierung des Clients
# openai.api_key = os.environ.get("OPENAI_API_KEY")
#
# # Erstellen einer Vervollständigung
# completion = openai.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "system", "content": "You are a LLM scientist who is an expert in the field of context-usage."},
#         {"role": "user", "content": "What strategies does GitHub Copilot use to capture and select context?"}
#     ]
# )
#
# # Ausgabe der Antwort
# print(completion.choices[0].message)


#codeCompletion = CodeCompletion(r"C:\Users\oligo\OneDrive\Bachelor Arbeit\repos\elasticsearch-java-main")
#codeCompletion.complete(r"C:\Users\oligo\OneDrive\Bachelor Arbeit\repos\elasticsearch-java-main\java-client\src\main\java\co\elastic\clients\json\SimpleJsonpMapper.java", 107)


# Ursprünglicher Pfad mit vielen Backslashes
path = "C:\\Users\\oligo\\OneDrive\\Bachelor Arbeit\\repos\\elasticsearch-java-main\\examples\\realworld-app\\rw-database\\src\\main\\java\\realworld\\db\\UserService.java"

# Ersetzen von Backslashes durch Forward Slashes
normalized_path = path.replace("\\", "/")

print(normalized_path)


