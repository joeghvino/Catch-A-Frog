# Catch A Frog
-Personal project by Joseph Ghivniashvili
-Date: 1/14/2026
-A small browser game where the player traps a frog. This repository contains the HTML/CSS/JS front-end and a Python backend for optional server features.
-Inspired by the Cat Trap game.

## Live preview
- Use the gh pages for the easiest way to demo the game (https://joeghvino.github.io/Catch-A-Frog/)
- (If the game is not loading fully, the render server is offline and you will have to run the backend using the following steps)

OR 

- run a simple local HTTP server and visit http://localhost:8000:

```powershell
cd "C:\Users\19085\OneDrive\Desktop\Catch A Frog Project"
python -m http.server 8000
```

## Tech
- Frontend: HTML, CSS, JavaScript (files in root / `css/` / `js/`)
- Backend (): Python (files in `src/`) - Backend Server running on Render

## Installation
1. (Optional but recommened) Create a virtual environment and install Python dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the frontend by opening `Index.html` (or use the HTTP server above).

## Running the  backend
- The backend files are in `src/`. If you plan to run any API server, ensure dependencies from `requirements.txt` are installed and run the appropriate module (for example `python src/api.py`) — check `src/api.py` for details.

## License
This project is released under the MIT License — see `LICENSE`.

