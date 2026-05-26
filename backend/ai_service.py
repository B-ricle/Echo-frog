def generate_response(user_message):
    normalized_message = user_message.lower()

    if "hello" in normalized_message:
        return "Ribbit. Good Day Person."
    
    return "Ribbit. I heard you."