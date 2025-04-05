import json
import random
from evaluator import evaluate_answer

def load_questions(filename="questions.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def start_chatbot():
    print("🤖 Welcome to the AI Quiz Bot!")
    print("Type 'exit' anytime to quit.\n")

    questions = load_questions()
    score_sum = 0
    total_questions = 5

    for i in range(total_questions):
        question_data = random.choice(questions)
        print(f"Q{i+1}: {question_data['question']}")
        user_answer = input("Your answer: ")

        if user_answer.lower().strip() == 'exit':
            break

        result = evaluate_answer(user_answer, question_data)

        print(f"✅ Matched Keywords: {result['matched_keywords']}")
        print(f"🧠 Score: {result['score']}%\n")
        score_sum += result['score']

    avg_score = round(score_sum / total_questions, 2)
    print("🎉 Quiz Completed!")
    print(f"📊 Your Average Score: {avg_score}%")

if __name__ == "__main__":
    start_chatbot()
