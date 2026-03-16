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
});

renderEntries();
