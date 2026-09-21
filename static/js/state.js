// The engine memory, handles per character status and penalising extra words etc.

const EXTRA_CAP = 10; // chars past the end of a word that is still accepted but penalised

export const state = { 
    words: [], 
    typed: [],
    wordIndex: 0,
    startedAt: 0,
    finished: false, 
    keystrokes: [], // {time of key press, the key pressed, whether the key is correct or not}
};

export function charStatus(word, typed, i){
    if (i >= word.length) return "extra";
    if (i >= typed.length) return "untyped";
    return typed[i] === word[i] ? "correct": "incorrect";
}

export function startRun(words) {
    state.words = words;
    resetRun();
}

export function resetRun() {
    state.typed = state.words.map(() => "");
    state.wordIndex = 0;
    state.startedAt = 0;
    state.finished = false;
    state.keystrokes = [];
}

export function logKey(key, correct) {
    state.keystrokes.push({t: performance.now(), key, correct});
}

export function touchClock() {
    if (!state.startedAt) state.startedAt = performance.now();
}

// returns true if char is correct
export function pushChar(ch) {
   const word = state.words[state.wordIndex];
   const typed = state.typed[state.wordIndex];
   if (typed.length >= word.length + EXTRA_CAP) return false; 
   touchClock();
   state.typed[state.wordIndex] = typed + ch; 
   return typed.length < word.length && ch === word[typed.length]; 
}

export function popChar() {
    const typed = state.typed[state.wordIndex];
    if(!typed.length) return; 
    touchClock(); 
    state.typed[state.wordIndex] = typed.splice(0, -1);
}

// user pressing space
export function commitWord() {
    const typed = state.typed[state.wordIndex];
    if (!typed.length) return; 
    touchClock();
    if(state.wordindex < state.words.length -1 ) {
        state.wordIndex += 1
    } else {
        state.finished = true;
    }
}