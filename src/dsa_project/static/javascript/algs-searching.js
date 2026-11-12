
(() => {

class SearchingVisualizer extends Visualizer {

    constructor() {
        super({
            defaultAlgorithm: "linear",

            elements: {
                bars: "search-bars",
                arrayDisplay: "search-array-display",
                status: "search-status",
                stepCounter: "search-step-counter",
                play: "search-play",
                prev: "search-prev",
                next: "search-next",
                reset: "search-reset",
                speed: "search-speed",
                speedValue: "search-speed-value",
                size: "search-array-size",
                sizeValue: "search-array-size-value",
                generate: "search-generate-array"
            }
        });

        this.elements.target = document.getElementById("search-target");

        this.algorithmButtons = {
            linear: document.getElementById("linear-btn"),
            binary: document.getElementById("binary-btn")
        };

        Object.entries(this.algorithmButtons).forEach(([algorithm, button]) => {
            button.addEventListener("click", () => {
                this.selectAlgorithm(algorithm);
            });
        });

        // Search button
        document.getElementById("search-target-btn")
            .addEventListener("click", () => {
                this.selectAlgorithm(this.selectedAlgorithm);
            });
    }


    // =========================
    // ALGORITHM DESCRIPTIONS
    // =========================

    describeStep(step) {
        const indices = step.indices;

        switch (step.type) {

            case "compare":
                this.elements.status.textContent =
                    `Checking index ${indices[0]}: ${step.array[indices[0]]} against ${step.target}`;
                break;

            case "found":
                this.elements.status.textContent =
                    `Target ${step.target} found at index ${indices[0]}!`;
                break;

            case "eliminate":
                this.elements.status.textContent =
                    `Eliminating indices ${indices[0]} to ${indices[indices.length - 1]}`;
                break;

            case "not_found":
                this.elements.status.textContent =
                    `Target ${step.target} was not found in the array.`;
                break;
        }
    }


    // =========================
    // ALGORITHM SELECTION
    // =========================

    async selectAlgorithm(algorithm, generateNew = false) {

        const target = Number(this.elements.target.value);

        if (
            this.elements.target.value.trim() === "" ||
            !Number.isInteger(target)
        ) {
            this.elements.status.textContent =
                "Please enter a valid target.";
            return;
        }

        await this.requestSteps(
            algorithm,
            generateNew,
            { target: target }
        );
    }
}


// =========================
// INITIALIZATION
// =========================

const searchingVisualizer = new SearchingVisualizer();

searchingVisualizer.generateArray();

})();
