export async function getWords(count = 30, list = "english_1k"){
    const res = await fetch (`/api/words?count=${count}&list=${list}`);
    if(!res.ok) throw new Error(`getWords ${res.status}`);
    return res.json();
}

export async function postResult(payload){
    const res = await fetch("/api/results", {
        method:"POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify(payload),
    });
    if(!res.ok) throw new Error(`postResult ${res.status} ${await res.text()}`);
    return res.json();
}