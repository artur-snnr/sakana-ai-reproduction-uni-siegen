import openai

client = openai.OpenAI(api_key="sk-") # Hier den API-Key einfügen

try:
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "user", "content": "Was ist Matrixfaktorisierung?"}
        ]
    )

    print("API funktioniert!")
    print("Antwort:", response.choices[0].message.content)

except openai.AuthenticationError:
    print("API-Key ist ungültig oder fehlt Zugriff.")

except openai.BadRequestError as e:
    print("Anfragefehler")
    print("Details:", e)

except Exception as e:
    print("Anderer Fehler:")
    print(e)