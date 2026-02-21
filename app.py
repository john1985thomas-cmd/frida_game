"""Frida Math Game — a web-based math game for kids."""

import json
import os
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8001


def generate_problem(level):
    """Generate a math problem appropriate for the given difficulty level."""
    if level == 1:
        ops = ["+", "-"]
        lo, hi = 1, 10
    elif level == 2:
        ops = ["+", "-", "×"]
        lo, hi = 1, 10
    elif level == 3:
        ops = ["+", "-", "×", "÷"]
        lo, hi = 1, 20
    elif level == 4:
        ops = ["+", "-", "×", "÷"]
        lo, hi = 1, 50
    else:
        ops = ["+", "-", "×", "÷"]
        lo, hi = 1, 100

    op = random.choice(ops)

    if op == "+":
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        answer = a + b
    elif op == "-":
        a = random.randint(lo, hi)
        b = random.randint(lo, a)
        answer = a - b
    elif op == "×":
        a = random.randint(lo, min(hi, 12))
        b = random.randint(lo, min(hi, 12))
        answer = a * b
    else:
        b = random.randint(lo, min(hi, 12))
        answer = random.randint(lo, min(hi, 12))
        a = b * answer

    return {"problem": f"{a} {op} {b}", "expected": answer}


def compute_new_state(correct, score, level, streak):
    """Update score, level, and streak based on whether the answer was correct."""
    if correct:
        score += 1
        streak = max(streak, 0) + 1
    else:
        score = max(0, score - 0.5)
        streak = min(streak, 0) - 1

    if streak >= 5 and level < 5:
        level += 1
        streak = 0
    elif streak <= -3 and level > 1:
        level -= 1
        streak = 0

    return score, level, streak


class GameHandler(SimpleHTTPRequestHandler):
    STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=self.STATIC_DIR, **kwargs)

    def do_POST(self):
        if self.path == "/api/check":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            answer = body.get("answer")
            expected = body.get("expected")
            score = body.get("score", 0)
            level = body.get("level", 1)
            streak = body.get("streak", 0)

            correct = answer == expected
            old_level = level
            score, level, streak = compute_new_state(correct, score, level, streak)
            next_q = generate_problem(level)

            response = {
                "correct": correct,
                "leveledUp": level > old_level,
                "newScore": score,
                "newLevel": level,
                "streak": streak,
                "nextProblem": next_q["problem"],
                "nextExpected": next_q["expected"],
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/api/start":
            q = generate_problem(1)
            response = {
                "problem": q["problem"],
                "expected": q["expected"],
                "level": 1,
                "score": 0,
                "streak": 0,
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass


def main():
    server = HTTPServer(("localhost", PORT), GameHandler)
    print(f"Frida Math Game running at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
