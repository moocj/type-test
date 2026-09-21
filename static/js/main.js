// main JS file 
// handles fetching words -> rendering -> collecting typing data -> presenting stats 

import { getWords, postResult } from "./api.js";

const WORD_COUNT = 30; 
const LIST = "english_1k";

const wordsEl = document.getElementById("words");
const inputEl = document.getElementById("typed");
const statusEl = document.getElementById("status");

let targetText = "";
let startedAt = 0; 
let finished = false; 

async function start() {
    const words = await getWords(WORD_COUNT, LIST);
    targetText = words.join(" ");
    wordsEl.textContent = targetText;
    inputEl.value = "";
    inputEl.focus(); // means the inputs from user goes to the input properly 
    statusEl.textContent = "type the text above";
}

async function finish() {
    finished = true; 
    inputEl.disabled = true;
    const duration = Math.max((performance.now() - startedAt) / 1000, 0.01); // have to be at least 0.01 else the API breaks 
    statusEl.textContent = "scoring...";
    try { 
        const row = await postResult({
            target: targetText,
            typed: inputEl.value,
            duration,
            per_second: [],
            mode: "words",
            mode_value: WORD_COUNT,
            list: LIST,
        });
        statusEl.textcontent = `saved #${row.id} - ${row.wpm.toFixed(1)} wpm - ${row.acc.toFixed(0)}% acc`;
        alert(`wpm: ${row.wpm.toFixed(1)}`); // PLACEHOLDER 
    } catch (err) {
        statusEl.textContent = String(err);
    }
}

inputEl.addEventListener("input", () => {
    if(!startedAt) startedAt = performance.now();
    if(!finished && inputEl.value.length >= targetText.length) void finish();
});

document.body.addEventListener("click", () => inputEl.focus());

start().catch((err) => {
    statusEl.textContent = STring(err);
});
