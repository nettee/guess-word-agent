#!/usr/bin/env python3
import requests
import sys
from urllib.parse import quote
from datetime import datetime

def guess_word(word, date=None):
    """猜一个词并返回结果"""
    if date is None:
        date = datetime.now().strftime("%Y%m%d")

    encoded_word = quote(word)
    url = f"https://xiaoce.fun/api/v0/quiz/daily/GuessWord/guess?date={date}&word={encoded_word}"

    try:
        response = requests.get(url)
        data = response.json()

        if not data.get("success", True):
            error_msg = data.get("errorMessage", "Unknown error")
            print(f"ERROR: {error_msg}")
            return None

        score = data.get("doubleScore", 0)
        correct = data.get("correct", False)

        return {
            "word": word,
            "score": score,
            "correct": correct
        }
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 guess_word.py <word> [date]")
        sys.exit(1)

    word = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else None

    result = guess_word(word, date)

    if result:
        if result["correct"]:
            print(f"✅ CORRECT! {result['word']}")
        else:
            print(f"{result['word']}: {result['score']:.4%}")
