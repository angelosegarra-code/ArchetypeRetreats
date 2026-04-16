const form = document.getElementById("reflectionForm");
const entriesDiv = document.getElementById("entries");

let entries = JSON.parse(localStorage.getItem("innercube_entries")) || [];

function saveEntries() {
  localStorage.setItem("innercube_entries", JSON.stringify(entries));
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text || "";
  return div.innerHTML;
}

function renderEntries() {
  entriesDiv.innerHTML = "";

  const privateEntries = entries.slice().reverse();

  if (privateEntries.length === 0) {
    entriesDiv.innerHTML = `
      <div class="entries-card-inner">
        <h2>Your Reflections</h2>
        <p>No reflections yet.</p>
        <p>Begin with a single insight and let the pattern reveal itself over time.</p>
      </div>
    `;
    return;
  }

  const wrapper = document.createElement("div");
  wrapper.className = "entries-card-inner";

  const heading = document.createElement("h2");
  heading.textContent = "Your Reflections";
  wrapper.appendChild(heading);

  const intro = document.createElement("p");
  intro.textContent = "A private record of what you’ve been noticing.";
  wrapper.appendChild(intro);

  privateEntries.forEach((entry) => {
    const card = document.createElement("div");
    card.className = "entry-card";

    card.innerHTML = `
      <p><strong>Date:</strong> ${escapeHtml(entry.date)}</p>
      <p><strong>Working with:</strong> ${escapeHtml(entry.journal)}</p>
      <p><strong>Archetype:</strong> ${escapeHtml(entry.archetype)}</p>
      <p><strong>Insight:</strong> ${escapeHtml(entry.insight)}</p>
      <p><strong>Shared:</strong> ${entry.share ? "Yes, anonymously" : "Private"}</p>
    `;

    wrapper.appendChild(card);
  });

  entriesDiv.appendChild(wrapper);
}

function updateSummary() {
  let dreamer = 0;
  let observer = 0;
  let alchemist = 0;
  let visionary = 0;

  entries.forEach((entry) => {
    if (entry.archetype === "Dreamer") dreamer++;
    if (entry.archetype === "Observer") observer++;
    if (entry.archetype === "Alchemist") alchemist++;
    if (entry.archetype === "Visionary") visionary++;
  });

  document.getElementById("dreamerCount").textContent = dreamer;
  document.getElementById("observerCount").textContent = observer;
  document.getElementById("alchemistCount").textContent = alchemist;
  document.getElementById("visionaryCount").textContent = visionary;
}

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const date = document.getElementById("date").value;
  const journal = document.getElementById("journal").value;
  const archetype = document.getElementById("archetype").value;
  const insight = document.getElementById("insight").value.trim();
  const share = document.getElementById("shareAnonymously")
    ? document.getElementById("shareAnonymously").checked
    : false;

  if (!date || !journal || !archetype || !insight) {
    alert("Please complete all fields before recording your insight.");
    return;
  }

  const entry = {
    date,
    journal,
    archetype,
    insight,
    share,
    createdAt: new Date().toISOString()
  };

  entries.push(entry);
  saveEntries();

  form.reset();
  renderEntries();
  updateSummary();
});

renderEntries();
updateSummary();
