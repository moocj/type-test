// main JS file 

import { getWords, postResult } from "./api.js";
import { handleKey, render} from "./engine.js";
import { resetRun, startRun, state} from "./state.js";

const WORD_COUNT = 30; 
const LIST = "english_1k";

const wordsEl = document.getElementById("words");
const statusEl = document.getElementById("status");

window.state = state; // for debugging 

function showError(err) {
    statusEl.textContent = String(err);
}

async function newRun() {
    statusEl.textContent="loading..."; 
    const words = await getWords(WORD_COUNT, LIST);
    startRun(words);
    render(wordsEl);
    statusEl.textContent = "type the words. tab: restart. esc: retry with the same words"

}

function retry() {
    resetRun(); // resetting run doesnt reset words
    render(wordsEl);
}
async function finish() {
    const duration = Math.max((performance.now() - state.startedAt) / 1000, 0.01); // have to be at least 0.01 else the API breaks 
    statusEl.textContent = "scoring...";
    try { 
        const row = await postResult({
            target: state.words.join(" "),
            typed: state.typed.join(" "),
            duration,
            per_second: [],
            mode: "words",
            mode_value: WORD_COUNT,
            list: LIST,
        });
        statusEl.textContent = `saved #${row.id} - ${row.wpm.toFixed(1)} wpm - ${row.acc.toFixed(0)}% acc`; 
    } catch (err) {
        statusEl.textContent = String(err);
    }
}

document.body.addEventListener("keydown", (event) => {
    if (event.key == "Tab") {
        event.preventDefault();
        void newRun().catch(showError);
        return;
    }
    if (event.key == "Escape") {
        event.preventDefault();
        retry();
        return;
    }
    if(handleKey(event)){
        render(wordsEl);
        if(state.finished) void finish();
    }
});

void newRun().catch(showError);
