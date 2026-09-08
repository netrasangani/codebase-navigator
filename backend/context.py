conversation_history = []


def add_message(role, content):
    conversation_history.append({
        "role": role,
        "content": content
    })


def get_context():
    return "\n".join(
        f"{message['role']}: {message['content']}"
        for message in conversation_history[-6:]
    )


def clear_context():
    conversation_history.clear()