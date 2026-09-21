// The engine itself, handles key presses and turning them into states 

import { charStatus, commitWord, logKey, popChar, pushChar, state } from "./state.js";

export function handleKey(event) {
    if (event.ctrlKey || event.metaKey || event.altKey) return false; //prevent it blocking browser shortcuts
    if (state.finished) return false; 

    const key = event.key 

    if (key === "Backspace") {
        event.preventDefault(); 
        popChar();
        logKey(key, false);
        return true;
    }

    if (key === " ") {
        event.preventDefault(); // stop page scrolling
        const typed = state.typed[state.wordIndex];
        if(!typed.length){
            logKey(key, false);
            return false; 
        }
        // only consider space to be "correct" if the word was "perfect"
        logKey(key, typed===state.words[state.wordIndex]);
        commitWord();
        return true;
    }

    if (key.length === 1) {
        logKey(key, pushChar(key));
        return true;
    }

    return false;
}

export function render(container) {
    const frag = document.createDocumentFragment(); 

    state.words.forEach((word, w) => {
        const wordEl = document.createElement("span");
        wordEl.className = w === state.wordIndex && !state.finished ? "word current" : "word";

        const typed = state.typed[w];
        const chars = Math.max(word.length, typed.length); 

        for(let i = 0; i < chars; i++){
            const ch = document.createElement("span");
            ch.textContent = i < word.length ? word[i] : typed[i]; // extras appear as what they were typed not the original word
            ch.className = charStatus(word, typed, i);
            wordEl.appendChild(ch);
        }

        frag.appendChild(wordEl);
        if(w < state.words.length - 1) frag.appendChild(document.createTextNode(" "));
    });

    container.replaceChildren(frag);
}