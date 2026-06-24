---
name: build-snake-html-game
description: Create a polished standalone Snake web game as a single HTML file. Use when the user asks Codex to generate a snake game, 贪吃蛇, browser mini-game, HTML game, or a self-contained web game that should run by opening an .html file without a build step.
---

# Build Snake HTML Game

## Overview

Build a complete, playable Snake game as one self-contained `.html` file with inline CSS and JavaScript. Prefer a direct artifact over an explanation unless the user only asks for guidance.

## Workflow

1. Create or update a single HTML file, usually `snake.html` unless the user names another file.
2. Include inline `<style>` and `<script>` blocks so the file works by double-clicking it.
3. Implement the game with `<canvas>` for the board and plain JavaScript for logic.
4. Add responsive layout so desktop and mobile screens both work.
5. Verify the file exists and contains the expected HTML, canvas, controls, and script.

## Required Features

- A visible title, score, and best score.
- A square game board rendered on canvas.
- Snake movement with arrow keys and WASD.
- Start, pause/resume, and restart controls.
- Food placement that never appears inside the snake.
- Collision detection for walls and the snake body.
- Score increases when food is eaten.
- Best score saved with `localStorage`.
- Clear start, pause, and game-over messages.
- Mobile-friendly on-screen directional controls.

## Implementation Guidance

- Use a fixed logical grid, such as `20 x 20`, and scale the canvas with CSS.
- Keep state explicit: `snake`, `food`, `direction`, `nextDirection`, `score`, `best`, `running`, `paused`, and timer/speed values.
- Prevent instant reverse turns by rejecting a new direction opposite to the current direction.
- Restart the interval when speed changes after eating food.
- Make the visual design polished but not dependent on external images, fonts, packages, or network access.
- Use Chinese UI text if the user asks in Chinese or requests 贪吃蛇.
- Keep controls stable on small screens; buttons and text must not overflow.

## Quality Check

After writing the file, confirm:

- The file exists at the intended path.
- It contains `<!DOCTYPE html>`, a `<canvas>`, a start button, a restart button, and a `<script>`.
- The game can run without a dev server or external assets.
- If browser verification is possible, open the page and check that the board is nonblank and controls are visible. If local `file://` browsing is blocked, state that and report the file-level checks instead.
