from difflib import SequenceMatcher

def sequence_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

similarity = sequence_similarity("anh", "ah")
print(similarity)
