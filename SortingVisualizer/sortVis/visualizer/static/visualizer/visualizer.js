let array = [];

document.getElementById("generate-array").addEventListener("click", () => {
    const size = document.getElementById("array-size").value;
    fetch(`/generate-array/?size=${size}`)
        .then(response => response.json())
        .then(data => {
            array = data.array;
            renderArray(array);
        });
});

document.getElementById("start-sort").addEventListener("click", () => {
    fetch(`/sort-array/?array=${JSON.stringify(array)}`)
        .then(response => response.json())
        .then(data => {
            visualizeSorting(data.steps);
        });
});

function renderArray(arr) {
    const visualizer = document.getElementById("visualizer");
    visualizer.innerHTML = ""; // Clear existing bars
    arr.forEach(height => {
        const bar = document.createElement("div");
        bar.classList.add("bar");
        bar.style.height = `${height * 3}px`;
        visualizer.appendChild(bar);
    });
}

function visualizeSorting(steps) {
    const bars = document.querySelectorAll(".bar");
    steps.forEach((step, index) => {
        setTimeout(() => {
            const [i, j] = step.swap || [];
            if (i !== undefined && j !== undefined) {
                const tempHeight = bars[i].style.height;
                bars[i].style.height = bars[j].style.height;
                bars[j].style.height = tempHeight;
            }
        }, index * 100);
    });
}
