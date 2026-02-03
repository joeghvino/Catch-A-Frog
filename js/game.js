
// Author: Joseph Ghviniashvili
// Date: 1/14/2026


// Frontend of game: fetch and render server state; send clicks to API
let board = null;
let rows = 11; 
let cols = 11;
// track current frog location to avoid scanning whole board
let frogPos = null; // [r, c] or null

function createCell(r, c) {
    // Creates a hex cell div with row and column attributes
    const cell = document.createElement('div');
    cell.className = 'hex-cell';
    cell.dataset.row = String(r);
    cell.dataset.col = String(c);
    const content = document.createElement('div');
    content.className = 'cell-content';
    cell.appendChild(content);
    cell.addEventListener('click', onCellClick);
    return cell;
}

function buildGrid(rows, cols) {
    // Builds the hex grid inside the board element
    if (!board) return;
    board.innerHTML = '';
    for (let r = 0; r < rows; r++) {
        const row = document.createElement('div');
        // add 'odd' class to every other row for offsetting hexes
        row.className = `hex-row${r % 2 ? ' odd' : ''}`;
        row.id = `hex-row-${r}`;
        for (let c = 0; c < cols; c++) {
            row.appendChild(createCell(r, c));
        }
        board.appendChild(row);
    }
}

function clearFrog() {
    if (!frogPos) return;
    const [pr, pc] = frogPos;
    const el = board.querySelector(`.hex-cell[data-row="${pr}"][data-col="${pc}"]`);
    if (el) {
        el.classList.remove('frog');
        const icon = el.querySelector('.frog-icon');
        if (icon) icon.remove();
    }
    frogPos = null;
}

function renderState(state) {
    if (!state || !board) return;
    // Grid is fixed and built once at init; only clear previous frog
    clearFrog();
    // place frog (use inline SVG icon inside the cell)
    const frog = state.frog;
    if (Array.isArray(frog) && frog.length === 2) {
        const [frogr, frogc] = frog;
        const el = board.querySelector(`.hex-cell[data-row="${frogr}"][data-col="${frogc}"]`);
        if (el) {
            el.classList.add('frog');
            // add a small inline SVG icon centered in the cell
            const svg = `<svg class="frog-icon" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">` +
                `<g><circle cx="32" cy="36" r="18" fill="#27ae60"/><circle cx="22" cy="24" r="6" fill="#ffffff"/><circle cx="42" cy="24" r="6" fill="#ffffff"/><circle cx="22" cy="24" r="2" fill="#000"/><circle cx="42" cy="24" r="2" fill="#000"/><path d="M22 44c4 4 16 4 20 0" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round"/></g></svg>`;
            // remove previous icon if any then insert
            const old = el.querySelector('.frog-icon');
            if (old) old.remove();
            el.insertAdjacentHTML('beforeend', svg);
            frogPos = [frogr, frogc];
        }
    }
    // place obstacles
    board.querySelectorAll('.hex-cell.obstacle').forEach(el => el.classList.remove('obstacle'));
    if (Array.isArray(state.obstacles)) {
        state.obstacles.forEach(o => {
            if (Array.isArray(o) && o.length === 2) {
                const [obstacler, obstaclec] = o;
                const el = board.querySelector(`.hex-cell[data-row="${obstacler}"][data-col="${obstaclec}"]`);
                if (el) el.classList.add('obstacle');
            }
        });
    }

    // show status message and disable board when game ends
    const statusEl = document.getElementById('game-status');
    if (statusEl) {
        if (state.status === 'win') {
            statusEl.textContent = 'You win — the frog is trapped!';
            board.classList.add('disabled');
        } else if (state.status === 'lose') {
            statusEl.textContent = 'You lose — the frog reached the edge.';
            board.classList.add('disabled');
        } else {
            statusEl.textContent = '';
            board.classList.remove('disabled');
        }
    }
}

async function onCellClick(ev) {
    const cell = ev.currentTarget;
    const r = Number(cell.dataset.row);
    const c = Number(cell.dataset.col);
    // prevent placing where an obstacle already exists or on the frog (invalid moves)
    // use `frogPos` for a fast identity check instead of querying the DOM
    if (cell.classList.contains('obstacle') || (frogPos && frogPos[0] === r && frogPos[1] === c)) {
        // small visual feedback: briefly flash
        cell.style.transition = 'box-shadow 0.15s';
        const prev = cell.style.boxShadow;
        cell.style.boxShadow = '0 0 0 3px rgba(255,0,0,0.6)';
        setTimeout(() => { cell.style.boxShadow = prev; }, 200);
        return;
    }
    try {
        const resp = await fetch('/click', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ r, c }),
            cache: 'no-store'
        });
        const data = await resp.json();
        console.log('click response', data);
        if (!resp.ok) {
            console.error('/click failed', resp.status, data);
            return;
        }
        // server returns { result, state }
        renderState(data.state || data);
    } catch (err) {
        console.error('click request failed', err);
    }
}

async function onResetClick() {
    try {
        const resp = await fetch('/reset', { method: 'POST' });
        if (!resp.ok) throw new Error('Network error');
        const data = await resp.json();
        renderState(data.state || data);
    } catch (err) {
        console.error('reset request failed', err);
    }
}

async function init() {
    const resetBtn = document.getElementById('reset-button');
    resetBtn?.addEventListener('click', onResetClick);

    // fetch server state; if unavailable, fall back to local defaults
    try {
        const resp = await fetch('/state?cb=' + Date.now(), { cache: 'no-store' });
        if (resp.ok) {
            const state = await resp.json();
            console.log('fetched state', state);
            renderState(state);
            return;
        } else {
            console.warn('Failed to fetch /state:', resp.status);
        }
    } catch (err) {
        console.warn('Error fetching /state', err);
    }

    // fallback: place frog in center of the pre-built grid
    const centerR = Math.floor(rows / 2);
    const centerC = Math.floor(cols / 2);
    const el = board.querySelector(`.hex-cell[data-row="${centerR}"][data-col="${centerC}"]`);
    if (el) {
        el.classList.add('frog');
        // insert same inline SVG used by renderState for visual consistency
        const svg = `<svg class="frog-icon" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">` +
            `<g><circle cx="32" cy="36" r="18" fill="#27ae60"/><circle cx="22" cy="24" r="6" fill="#ffffff"/><circle cx="42" cy="24" r="6" fill="#ffffff"/><circle cx="22" cy="24" r="2" fill="#000"/><circle cx="42" cy="24" r="2" fill="#000"/><path d="M22 44c4 4 16 4 20 0" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round"/></g></svg>`;
        const old = el.querySelector('.frog-icon');
        if (old) old.remove();
        el.insertAdjacentHTML('beforeend', svg);
    }
    frogPos = [centerR, centerC];
}

// Defer DOM access until ready
window.addEventListener('DOMContentLoaded', () => {
    console.log('game.js loaded');
    board = document.getElementById('game-board');
    // Build the fixed grid once at startup
    buildGrid(rows, cols);
    init();
});
