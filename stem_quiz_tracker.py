import csv
import os
import random


class Question:
    """Represents a single multiple-choice STEM question."""

    def __init__(self, topic, prompt, options, answer, explanation):
        self.topic = topic
        self.prompt = prompt
        self.options = options
        self.answer = answer.upper()
        self.explanation = explanation


DEFAULT_QUESTIONS = [
    Question(
        topic="Algebra & Functions",
        prompt="If f(x) = 2x + 3, what is f(4)?",
        options={"A": "8", "B": "11", "C": "14"},
        answer="B",
        explanation="Substitute x = 4 into 2(4) + 3 = 8 + 3 = 11.",
    ),
    Question(
        topic="Binary & Logic",
        prompt="What is the decimal value of the 4-bit binary number 1010?",
        options={"A": "6", "B": "10", "C": "12"},
        answer="B",
        explanation="1*8 + 0*4 + 1*2 + 0*1 = 10.",
    ),
    Question(
        topic="Python Basics",
        prompt="In Python, what does len([10, 20, 30, 40]) return?",
        options={"A": "3", "B": "4", "C": "40"},
        answer="B",
        explanation="There are 4 elements in the list.",
    ),
    Question(
        topic="Algebra & Functions",
        prompt="Solve for x: 3x - 5 = 16",
        options={"A": "x = 7", "B": "x = 3.67", "C": "x = 11"},
        answer="A",
        explanation="Add 5 to both sides (3x = 21), then divide by 3 (x = 7).",
    ),
    Question(
        topic="Binary & Logic",
        prompt="What is the output of (True and False) or True?",
        options={"A": "False", "B": "True", "C": "Error"},
        answer="B",
        explanation="True and False is False; False or True evaluates to True.",
    ),
]


def load_questions(csv_path):
    """Loads custom questions from a CSV file if it exists, otherwise uses defaults."""
    if os.path.exists(csv_path) == False:
        return DEFAULT_QUESTIONS

    questions = []
    try:
        with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                q = Question(
                    topic=row["topic"].strip(),
                    prompt=row["prompt"].strip(),
                    options={
                        "A": row["option_a"].strip(),
                        "B": row["option_b"].strip(),
                        "C": row["option_c"].strip(),
                    },
                    answer=row["answer"].strip(),
                    explanation=row["explanation"].strip(),
                )
                questions.append(q)
    except Exception as err:
        print(f"[Notice] Could not load {csv_path} ({err}). Using built-in questions.")
        return DEFAULT_QUESTIONS

    if len(questions) > 0:
        return questions
    else:
        return DEFAULT_QUESTIONS


def log_attempt(log_path, student_name, topic, is_correct):
    """Appends a single question result to the CSV progress log."""
    file_exists = os.path.exists(log_path)
    try:
        with open(log_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file_exists == False:
                writer.writerow(["student", "topic", "correct"])
            writer.writerow([student_name, topic, int(is_correct)])
    except Exception as err:
        print(f"[Warning] Could not save attempt to log: {err}")


def show_topic_summary(log_path, student_name):
    """Reads the student's log history and highlights topics below 75% accuracy."""
    if os.path.exists(log_path) == False:
        print("No progress history found yet.")
        return

    # Stores topic -> [correct_count, total_attempts]
    stats = {}
    try:
        with open(log_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["student"].strip().lower() == student_name.lower():
                    topic = row["topic"].strip()
                    correct = int(row["correct"])
                    if topic not in stats:
                        stats[topic] = [0, 0]
                    stats[topic][0] = stats[topic][0] + correct
                    stats[topic][1] = stats[topic][1] + 1
    except Exception as err:
        print(f"[Warning] Error reading progress log: {err}")
        return

    if len(stats) == 0:
        print(f"No recorded attempts found for {student_name}.")
        return

    print(f"\n--- Report for {student_name} ---")
    weak_areas = []
    for topic in sorted(stats.keys()):
        right = stats[topic][0]
        total = stats[topic][1]
        pct = (right / total) * 100
        print(f"  {topic}: {right}/{total} ({round(pct)}%)")
        if pct < 75.0:
            weak_areas.append([pct, topic])

    if len(weak_areas) > 0:
        weak_areas.sort()
        review_names = []
        for item in weak_areas:
            review_names.append(item[1])
        review_list = ", ".join(review_names)
        print(f"Suggested review topics: {review_list}")
    else:
        print("Solid performance across all topics!")


def start_quiz(questions, log_path):
    """Runs an interactive quiz session and updates student analytics."""
    name = input("Enter student name (or press Enter for 'Guest'): ").strip()
    if name == "":
        name = "Guest"

    quiz_pool = list(questions)
    random.shuffle(quiz_pool)

    score = 0
    q_num = 1
    for q in quiz_pool:
        print(f"\nQ{q_num} [{q.topic}]: {q.prompt}")
        for option_key in ("A", "B", "C"):
            print(f"  {option_key}) {q.options[option_key]}")

        choice = ""
        while choice not in ("A", "B", "C"):
            choice = input("Your answer (A/B/C): ").strip().upper()
            if choice not in ("A", "B", "C"):
                print("Invalid input. Please enter A, B, or C.")

        if choice == q.answer:
            score = score + 1
            print("Correct!")
            log_attempt(log_path, name, q.topic, True)
        else:
            print(f"Incorrect — the answer is {q.answer}. {q.explanation}")
            log_attempt(log_path, name, q.topic, False)

        q_num = q_num + 1

    print(f"\nSession Score: {score}/{len(quiz_pool)}")
    show_topic_summary(log_path, name)


if __name__ == "__main__":
    active_questions = load_questions("questions.csv")
    start_quiz(active_questions, "student_progress.csv")
