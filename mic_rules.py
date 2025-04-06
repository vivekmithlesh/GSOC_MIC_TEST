def rule_based_mic_detector(text):
    keywords = ['military', 'conflict', 'attack', 'soldier', 'killed', 'strike', 'clash', 'troops']
    return any(word in text.lower() for word in keywords)