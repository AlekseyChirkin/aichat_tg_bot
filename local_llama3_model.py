import ollama


def get_response_from_ai(message_form_user: str) -> str:
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': message_form_user,
        },
    ])
    return response['message']['content']
