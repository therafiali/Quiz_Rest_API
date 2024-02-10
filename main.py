from fastapi import FastAPI, Path, Query
from typing import Union
from enum import Enum
from pydantic import BaseModel
from unittest.util import _MAX_LENGTH
from sqlmodel import Session
from database import engine
from models import Student, Quiz_Question, Answer
from sqlmodel import select
import requests
import json


app: FastAPI = FastAPI(title="Quiz API")


@app.post("/create_student")
def create_student(student: Student):
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student


@app.get("/get_students")
def get_student():
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        return students


@app.post("/create_question")
def create_question(question: Quiz_Question):
    with Session(engine) as session:
        session.add(question)
        session.commit()
        session.refresh(question)
        return question


@app.get("/get_questions")
def get_questions():
    with Session(engine) as session:
        questions = session.exec(select(Quiz_Question)).all()
        # question_data = [{"id": question.id, "question": question.question, "choices": question.choices} for question in questions]
        return questions


@app.post("/answers")
def answers(answer: Answer):
    with Session(engine) as session:
        session.add(answer)
        session.commit()
        session.refresh(answer)
        return answer


@app.get("/get_answers")
def get_answers():
    with Session(engine) as session:
        answers = session.exec(select(Answer)).all()
        return answers



@app.get("/get_result")
def get_result():
    def verify_answer():
        def get_questions():
            with Session(engine) as session:
                questions1 = session.exec(select(Quiz_Question)).all()
                questions112 = [
                    {
                        'question': q.question,
                        'choices': q.choices,
                        'id': q.id,
                        'correct_answer': q.correct_answer
                    }
                    for q in questions1
                ]
                return questions112

        question_response1 = get_questions()
        print("question_response1", question_response1)
        # print("question_response",question_response1["Quiz_Question"])

        answer_response = requests.get('http://127.0.0.1:8000/get_answers')
        user_answers = answer_response.json()
        # print(user_answers,"user_answers")

        results = []
        for question in question_response1:
            question_id = question["id"]
            correct_answer = question["correct_answer"]

            user_answer = next(
                (answer for answer in user_answers if answer["question_id"] == question_id),
                None,
            )

            if not user_answer:
                raise ValueError(
                    f"Question ID {question_id} not found in user answer list.")

            user_answer = user_answer["correct_answer"]

            is_correct = user_answer == correct_answer
            message = "Correct!" if is_correct else "Incorrect."

            # Generate feedback specific to the question and answer
            feedback = "Your answer was " + user_answer + "."
            if not is_correct:
                feedback += " The correct answer is " + correct_answer + "."

                # Implement partial credit logic (if needed)
                # ...

            result = {
                "question": question["question"],
                "message": message,
                "feedback": feedback,
                "correct_answer": correct_answer,  # Add if desired
                # "partial_credit": ...,  # Add if implemented
                # "additional_statistics": ...,  # Add if desired
            }

            results.append(result)

        return results

    results = verify_answer()
    return results  # Change this line
