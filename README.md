# Frida's Math Game

A web-based math game for kids with adaptive difficulty. Solve addition, subtraction, multiplication, and division problems, earn points, and level up!

## How to play

1. Start the server:

   ```bash
   python3 app.py
   ```

2. Open http://localhost:8001 in your browser.

3. Click **Let's Go!** and start solving problems.

## Scoring

- Correct answer: **+1 point**
- Wrong answer: **-0.5 points** (minimum 0)

## Difficulty

The game starts easy (small numbers, addition/subtraction) and gets harder as you answer correctly. Five correct answers in a row levels you up. Three wrong answers in a row brings you back down.

| Level | Operations | Number range |
|-------|-----------|-------------|
| 1 | + − | 1–10 |
| 2 | + − × | 1–10 |
| 3 | + − × ÷ | 1–20 |
| 4 | + − × ÷ | 1–50 |
| 5 | + − × ÷ | 1–100 |
