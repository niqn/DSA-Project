
(() => {

class SortingVisualizer extends Visualizer {
    // constructs buttons
    constructor() {
        super({
            defaultAlgorithm: "bubble",

            elements: {
                bars: "bars",
                arrayDisplay: "array-display",
                status: "status",
                stepCounter: "step-counter",
                play: "play",
                prev: "prev",
                next: "next",
                reset: "reset",
                speed: "speed",
                speedValue: "speed-value",
                size: "array-size",
                sizeValue: "array-size-value",
                generate: "generate-array"
            }
        });
        // alg chooser
        this.algorithmButtons = {
            bubble: document.getElementById("bubble-btn"),
            insertion: document.getElementById("insertion-btn")
        };
        Object.entries(this.algorithmButtons).forEach(([algorithm, button]) => {
            button.addEventListener("click", () => {
                this.selectAlgorithm(algorithm);
            });
        });
    }


    describeStep(step) {
        const indices = step.indices;

        switch (step.type) {
            case "compare":
                this.elements.status.textContent =
                    `Comparing indices ${indices.join(" and ")}`;
                break;

            case "swap":
                this.elements.status.textContent =
                    `Swapping indices ${indices.join(" and ")}`;
                break;

            case "shift":
                this.elements.status.textContent =
                    `Shifting index ${indices[0]} to ${indices[1]}`;
                break;

            case "insert":
                this.elements.status.textContent =
                    `Inserting key at index ${indices[0]}`;
                break;

            case "sorted":
                this.elements.status.textContent =
                    "Array successfully sorted!";
                break;
        }
    }


    async selectAlgorithm(algorithm, generateNew = false) {
        await this.requestSteps(algorithm, generateNew);
    }
}

const sortingVisualizer = new SortingVisualizer();

sortingVisualizer.generateArray();

})();