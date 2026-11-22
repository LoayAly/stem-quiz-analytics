# stem-quiz-analytics Trackere
A lightweight, modular Python tool designed to help students practice core STEM concepts (Algebra, Binary Logic, and Python Basics) while giving instructors clear visibility into topic-by-topic mastery.

# Key Features
- **Interactive Quiz Engine:** Randomizes questions, validates student input, and gives immediate step-by-step explanations for incorrect answers.
- **CSV Progress Logging:** Automatically records every attempt to `student_progress.csv` so performance can be tracked across multiple sessions.
- **Automated Topic Mastery Report:** Calculates per-topic accuracy and flags weak areas (<75%) for targeted review.
- **Extensible Question Bank:** Supports loading custom questions from an external `questions.csv` file without modifying the source code.

## Tech & Design Concepts Used
- Python 3 (Standard Library: `csv`, `os`, `random`)
- Object-Oriented Programming (`Question` class)
- File I/O & Exception Handling
- Data Aggregation & Sorting

## How to Run
```bash
python stem_quiz_tracker.py
