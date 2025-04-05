import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# Download only once
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

def lemmatize_keywords(keywords):
    return [lemmatizer.lemmatize(word.lower()) for word in keywords]

def evaluate_answer(user_answer, question_data):
    user_tokens = word_tokenize(user_answer.lower())
    lemmatized_user = [lemmatizer.lemmatize(word) for word in user_tokens]

    ideal_keywords = lemmatize_keywords(question_data["keywords"])
    matched = [word for word in ideal_keywords if word in lemmatized_user]

    score = (len(matched) / len(ideal_keywords)) * question_data["marks"]

    feedback = ""
    if score == question_data["marks"]:
        feedback = "Excellent! You covered all key points."
    elif score >= question_data["marks"] / 2:
        feedback = "Good attempt. Missing: " + ", ".join(set(ideal_keywords) - set(matched))
    else:
        feedback = "Missed most key concepts. Revise: " + ", ".join(ideal_keywords)

    return {
        "score": round(score, 2),
        "max_marks": question_data["marks"],
        "matched_keywords": matched,
        "total_keywords": ideal_keywords,
        "feedback": feedback
    }
