import json
import random
from evaluator import evaluate_answer
import nltk

# Download punkt if not available
nltk.download('punkt')
nltk.download('punkt_tab')

# Load the dataset
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Shuffle and select N questions
num_questions = 5
selected_questions = random.sample(data, num_questions)

total_score = 0
user_responses = []

print("\n📚 AI Model - Subjective Answer Evaluation\n")

for i, question_data in enumerate(selected_questions, 1):
    print(f"\nQuestion {i}: {question_data['question']}")
    user_answer = input("Your Answer: ")

    result = evaluate_answer(user_answer, question_data)

    print("✅ Score for this answer:", result["score"], "%")
    print("Matched Keywords:", result["matched_keywords"])

    # Track score and answers
    total_score += result["score"]
    user_responses.append({
        "question": question_data["question"],
        "user_answer": user_answer,
        "score": result["score"]
    })

# Final Summary
average_score = round(total_score / num_questions, 2)
print("\n🎯 Quiz Finished!")
print("Your Total Average Score:", average_score, "%")

# Optional: Save session data
with open("user_results.json", "w", encoding="utf-8") as f:
    json.dump(user_responses, f, indent=4)

print("📁 Session saved in user_results.json")
