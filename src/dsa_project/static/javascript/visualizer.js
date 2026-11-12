
class Visualizer {
    constructor(config) {
        // Configuration
        this.endpoint = config.endpoint || "/algorithms/steps";

        this.elements = {};

        // Get DOM elements from configuration
        for (const [key, id] of Object.entries(config.elements)) {
            this.elements[key] = document.getElementById(id);
        }

        // State
        this.steps = [];
        this.currentStep = 0;
        this.interval = null;
        this.currentArray = [];
        this.displayArray = [];
        this.selectedAlgorithm = config.defaultAlgorithm;

        // Event listeners
        this.bindControls();
    }


    // =========================
    // EVENT LISTENERS
    // =========================

    bindControls() {
        const e = this.elements;

        e.next.addEventListener("click", () => this.nextStep());
        e.prev.addEventListener("click", () => this.previousStep());
        e.play.addEventListener("click", () => this.play());
        e.reset.addEventListener("click", () => this.reset());

        e.speed.addEventListener("input", () => {
            e.speedValue.textContent = e.speed.value;

            // Apply new speed immediately
            if (this.interval !== null) {
                this.pause();
                this.play();
            }
        });

        e.size.addEventListener("input", () => {
            e.sizeValue.textContent = e.size.value;
        });

        e.generate.addEventListener("click", () => {
            this.generateArray();
        });
    }


    // =========================
    // ARRAY GENERATION
    // =========================

    async generateArray() {
        await this.selectAlgorithm(this.selectedAlgorithm, true);
    }


    // =========================
    // API REQUEST
    // =========================

    async requestSteps(algorithm, generateNew = false, extraData = {}) {
        this.pause();

        this.selectedAlgorithm = algorithm;
        this.setActiveButton(algorithm);

        this.elements.status.textContent = "Generating steps...";

        const payload = {
            algorithm: algorithm,
            ...extraData
        };

        if (generateNew || this.currentArray.length === 0) {
            payload.size = Number(this.elements.size.value);
        } else {
            payload.array = this.currentArray;
        }

        try {
            const response = await fetch(this.endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Failed to generate steps");
            }

            this.currentArray = data.original_array;
            this.displayArray = data.display_array ?? data.original_array;

            this.steps = data.steps;
            this.currentStep = 0;

            this.showStep(0);

        } catch (error) {
            console.error(error);
            this.elements.status.textContent = error.message;
        }
    }


    // =========================
    // BUTTON STATES
    // =========================

    setActiveButton(algorithm) {
        for (const [name, button] of Object.entries(this.algorithmButtons)) {
            button.classList.toggle("active", name === algorithm);
        }
    }


    // =========================
    // ARRAY RENDERING
    // =========================

    renderArray(array, indices = [], type = "") {
        const container = this.elements.arrayDisplay;
        container.innerHTML = "";

        array.forEach((value, index) => {
            const item = document.createElement("span");

            item.classList.add("array-item");
            item.textContent = value;

            if (indices.includes(index)) {
                item.classList.add(type);
            }

            container.appendChild(item);
        });
    }


    // =========================
    // BAR RENDERING
    // =========================

    renderBars(array, indices = [], type = "") {
        const container = this.elements.bars;
        container.innerHTML = "";

        const maxValue = Math.max(...array, 1);

        array.forEach((value, index) => {
            const bar = document.createElement("div");

            bar.classList.add("bar");
            bar.style.height = `${(value / maxValue) * 100}%`;
            bar.textContent = value;

            if (indices.includes(index)) {
                bar.classList.add(type);
            }

            container.appendChild(bar);
        });
    }


    // =========================
    // DISPLAY STEPS
    // =========================

    showStep(stepIndex) {
        if (stepIndex < 0 || stepIndex >= this.steps.length) return;

        this.currentStep = stepIndex;

        const step = this.steps[stepIndex];

        this.renderBars(step.array, step.indices, step.type);
        this.renderArray(step.array, step.indices, step.type);

        this.describeStep(step);

        this.elements.stepCounter.textContent =
            `Step ${this.currentStep + 1} / ${this.steps.length}`;
    }


    // Child classes implement their own descriptions
    describeStep(step) {
        this.elements.status.textContent = step.type;
    }


    // =========================
    // NAVIGATION
    // =========================

    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.showStep(this.currentStep + 1);
        } else {
            this.pause();
        }
    }


    previousStep() {
        if (this.currentStep > 0) {
            this.showStep(this.currentStep - 1);
        }
    }


    reset() {
        this.pause();
        this.showStep(0);
    }


    // =========================
    // PLAY / PAUSE
    // =========================

    play() {
        if (this.interval !== null) {
            this.pause();
            return;
        }

        if (this.steps.length === 0) return;

        if (this.currentStep === this.steps.length - 1) {
            this.showStep(0);
        }

        this.elements.play.textContent = "Pause";

        this.interval = setInterval(() => {
            this.nextStep();
        }, Number(this.elements.speed.value));
    }


    pause() {
        clearInterval(this.interval);
        this.interval = null;

        this.elements.play.textContent = "Play";
    }


    // =========================
    // ALGORITHM SELECTION
    // =========================

    async selectAlgorithm(algorithm, generateNew = false) {
        await this.requestSteps(algorithm, generateNew);
    }
}
