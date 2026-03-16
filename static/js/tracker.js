function saveReflection() {
    const text = document.getElementById("reflection").value;

    localStorage.setItem("innercube_reflection", text);

    document.getElementById("saved").innerText = "Saved ✓";
}

window.onload = function () {

    const saved = localStorage.getItem("innercube_reflection");

    if (saved) {
        document.getElementById("reflection").value = saved;
    }

};
