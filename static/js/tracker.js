const form = document.getElementById("reflectionForm");
const entriesDiv = document.getElementById("entries");

let entries = JSON.parse(localStorage.getItem("innercube_entries")) || [];

function renderEntries() {
    entriesDiv.innerHTML = "";

    if (entries.length === 0) {
        entriesDiv.innerHTML = "<p>No reflections yet.</p>";
        return;
    }

    entries.slice().reverse().forEach(entry => {
        let div = document.createElement("div");
        div.innerHTML = `
            <hr>
            <p><strong>Date:</strong> ${entry.date}</p>
            <p><strong>Journal:</strong> ${entry.journal}</p>
            <p><strong>Archetype:</strong> ${entry.archetype}</p>
            <p><strong>Insight:</strong> ${entry.insight}</p>
        `;
        entriesDiv.appendChild(div);
    });
}

form.addEventListener("submit", function(e) {
    e.preventDefault();

    let entry = {
        date: document.getElementById("date").value,
        journal: document.getElementById("journal").value,
        archetype: document.getElementById("archetype").value,
        insight: document.getElementById("insight").value
    };

    entries.push(entry);
localStorage.setItem("innercube_entries", JSON.stringify(entries));

form.reset();
renderEntries();
updateSummary();

});

renderEntries();
updateSummary();

function updateSummary() {

let dreamer = 0;
let observer = 0;
let alchemist = 0;
let visionary = 0;

entries.forEach(e => {

if (e.archetype === "Dreamer") dreamer++;
if (e.archetype === "Observer") observer++;
if (e.archetype === "Alchemist") alchemist++;
if (e.archetype === "Visionary") visionary++;

});

document.getElementById("dreamerCount").textContent = dreamer;
document.getElementById("observerCount").textContent = observer;
document.getElementById("alchemistCount").textContent = alchemist;
document.getElementById("visionaryCount").textContent = visionary;

}
