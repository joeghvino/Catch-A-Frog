# Catch A Frog
Personal project by Joseph Ghivniashvili
Date: 1/14/2026
A small browser game where the player traps a frog. This repository contains the HTML/CSS/JS front-end and a Python backend for optional server features.

## Live preview
- Open `Index.html` in your browser (double-click) for a quick demo.
- Or run a simple local HTTP server and visit http://localhost:8000:

```powershell
cd "C:\Users\19085\OneDrive\Desktop\Catch A Frog Project"
python -m http.server 8000
```

## Tech
- Frontend: HTML, CSS, JavaScript (files in root / `css/` / `js/`)
- Backend (optional): Python (files in `src/`)

## Installation
1. (Optional) but recommened Create a virtual environment and install Python dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the frontend by opening `Index.html` (or use the HTTP server above).

## Running the  backend
- The backend files are in `src/`. If you plan to run any API server, ensure dependencies from `requirements.txt` are installed and run the appropriate module (for example `python src/api.py`) — check `src/api.py` for details.

## GitHub Pages
To host the static frontend on GitHub Pages:

1. Push this repository to GitHub.
2. In the repository settings, enable Pages and choose the `main` branch (root) or create and publish a `gh-pages` branch.

## License
This project is released under the MIT License — see `LICENSE`.

