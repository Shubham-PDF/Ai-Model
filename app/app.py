# Filename: app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import string
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# Load questions from JSON
with open("app/questions.json", "r") as f:
    all_questions = json.load(f)

# Group by domain
domain_questions = {}
for q in all_questions:
    domain = q.get("domain", "General")
    if domain not in domain_questions:
        domain_questions[domain] = []
    domain_questions[domain].append(q)

# Evaluate subjective answer
def evaluate_answer(user_answer, ideal_keywords):
    user_tokens = word_tokenize(user_answer.lower())
    user_tokens = [lemmatizer.lemmatize(word) for word in user_tokens if word not in string.punctuation]
    matched_keywords = [kw for kw in ideal_keywords if any(kw in word for word in user_tokens)]
    score = len(matched_keywords) / len(ideal_keywords) * 5
    return {
        "matched_keywords": matched_keywords,
        "score": round(score, 2),
        "total": 5,
        "feedback": generate_feedback(matched_keywords, ideal_keywords)
    }

def generate_feedback(matched, ideal):
    missed = list(set(ideal) - set(matched))
    if not missed:
        return "Excellent! You covered all the key points."
    else:
        return f"Try to include the following concepts: {', '.join(missed)}"

# API to fetch questions based on domain
@app.route("/api/get_questions", methods=["POST"])
def get_questions():
    data = request.json
    domain = data.get("domain")
    if not domain or domain not in domain_questions:
        return jsonify({"error": "Invalid or missing domain"}), 400
    questions = random.sample(domain_questions[domain], min(15, len(domain_questions[domain])))
    return jsonify({"questions": questions})

# API to evaluate answer
@app.route("/api/evaluate_answer", methods=["POST"])
def evaluate():
    data = request.json
    user_answer = data.get("answer")
    ideal_keywords = data.get("keywords")
    if not user_answer or not ideal_keywords:
        return jsonify({"error": "Missing answer or keywords"}), 400
    result = evaluate_answer(user_answer, ideal_keywords)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
