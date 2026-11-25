---
name: teach
description: Stateful personal tutor that teaches any software engineering concept, codebase, or report through short, visual HTML lessons with retrieval quizzes and learning records. Use when the user wants to learn a new topic, understand unfamiliar technical terms, or study an architecture report or book.
---

# Teach

Help the user build **real long-term understanding** (storage strength), not
just an in-the-moment illusion of understanding (fluency).

## Workspace Layout (Create Lazily)

In the current learning folder (or `learn/<topic>/`), keep state across
sessions:

- `MISSION.md` — *Why* the user wants to learn this and their real-world goal.
  If missing, ask 2–3 quick questions first to ground every lesson.
- `lessons/0001-<slug>.html` — Short, self-contained HTML lessons (one focused
  concept per lesson, clean readable typography, opened in the user's browser).
- `reference/<slug>.html` — Compressed cheat sheets & glossaries for quick
  lookup later.
- `learning-records/0001-<slug>.md` — Brief record of what the user mastered or
  struggled with, so the next lesson lands in their **zone of proximal
  development** (challenging enough to grow, never overwhelming).
- `NOTES.md` — User's learning preferences (e.g., prefers everyday analogies,
  examples from their own repos).

## How to Run a Lesson

1. **Check state first:** Read `MISSION.md` and recent `learning-records/` to
   see what the user already knows.
2. **Teach ONE small thing at a time:**
   - Start with a plain-English analogy and a concrete example (ideally from
     the user's own codebase or report).
   - Keep working memory light — a lesson should take 5–10 minutes to finish
     and give one clear win.
   - Cite high-trust primary sources (official docs, classic books) when
     relevant.
3. **Test retention (retrieval practice):**
   - Include a short interactive quiz or hands-on mini-task inside the HTML
     lesson with immediate feedback.
   - Make quiz options similar in length and vary the correct answer's position
     so formatting never gives away the answer.
4. **Open & invite questions:** Open the HTML lesson in the browser, print its
   path, remind the user to ask about anything unclear, and log a short
   `learning-records/` entry once they finish.
