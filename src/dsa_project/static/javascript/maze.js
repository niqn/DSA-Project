class MazeVisualizer {
    constructor() {
        this.elements = {
            grid: document.getElementById("maze-grid"),
            rows: document.getElementById("maze-rows"),
            cols: document.getElementById("maze-cols"),
            create: document.getElementById("create-maze"),
            generate: document.getElementById("generate-maze"),
            algorithm: document.getElementById("maze-algorithm"),
            solve: document.getElementById("solve-maze"),
            prev: document.getElementById("maze-prev"),
            play: document.getElementById("maze-play"),
            next: document.getElementById("maze-next"),
            reset: document.getElementById("maze-reset"),
            speed: document.getElementById("maze-speed"),
            speedValue: document.getElementById("maze-speed-value"),
            stepCounter: document.getElementById("maze-step-counter"),
            status: document.getElementById("maze-status")
        };

        this.maze = null;
        this.finalMaze = null;
        this.steps = [];
        this.currentStep = -1;
        this.interval = null;

        this.bindControls();
        this.loadMaze();
    }

    bindControls() {
        const e = this.elements;
        e.create.addEventListener("click", () => this.loadMaze());
        e.generate.addEventListener("click", () => this.generateMaze());
        e.solve.addEventListener("click", () => this.solveMaze());
        e.next.addEventListener("click", () => this.nextStep());
        e.prev.addEventListener("click", () => this.previousStep());
        e.play.addEventListener("click", () => this.play());
        e.reset.addEventListener("click", () => this.reset());
        e.speed.addEventListener("input", () => {
            e.speedValue.textContent = e.speed.value;
            if (this.interval !== null) {
                this.pause();
                this.play();
            }
        });
    }

    async requestJSON(url, options = {}) {
        const response = await fetch(url, options);
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "The request failed.");
        return data;
    }

    getDimensions() {
        const rows = Number(this.elements.rows.value);
        const cols = Number(this.elements.cols.value);
        if (!Number.isInteger(rows) || !Number.isInteger(cols) ||
            rows < 5 || rows > 30 || cols < 5 || cols > 30) {
            throw new Error("Rows and columns must be between 5 and 30.");
        }
        return { rows, cols };
    }

    async loadMaze() {
        this.pause();
        this.finalMaze = null;
        this.elements.status.textContent = "Creating graph grid...";
        try {
            const { rows, cols } = this.getDimensions();
            const params = new URLSearchParams({ rows, cols });
            const data = await this.requestJSON(`/maze/data?${params}`);
            this.setMazeData(data);
            this.elements.status.textContent = "Empty graph created. No edges yet.";
        } catch (error) {
            this.elements.status.textContent = error.message;
        }
    }

    async generateMaze() {
        this.pause();
        this.elements.status.textContent = "Generating graph...";
        try {
            const dimensions = this.getDimensions();
            const data = await this.requestJSON("/maze/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dimensions)
            });
            this.finalMaze = data.final_maze;
            this.setMazeData(data);
            this.elements.status.textContent = "Graph generated. Ready to solve.";
        } catch (error) {
            this.elements.status.textContent = error.message;
        }
    }

    async solveMaze() {
        this.pause();
        if (!this.finalMaze) {
            this.elements.status.textContent = "Generate a maze before solving it.";
            return;
        }
        this.elements.status.textContent = "Running graph traversal...";
        try {
            const data = await this.requestJSON("/maze/solve", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    algorithm: this.elements.algorithm.value,
                    maze: this.finalMaze
                })
            });
            this.maze = this.finalMaze;
            this.steps = data.steps || [];
            this.currentStep = -1;
            this.showStep(-1);
            this.elements.status.textContent = `${data.algorithm.toUpperCase()} ready. Press Play or Next.`;
        } catch (error) {
            this.elements.status.textContent = error.message;
        }
    }

    setMazeData(data) {
        this.maze = data.maze;
        this.steps = data.steps || [];
        this.currentStep = -1;
        this.showStep(-1);
    }

    cellElement(vertex) {
        return this.elements.grid.querySelector(`[data-vertex="${vertex}"]`);
    }

    renderMaze() {
        const container = this.elements.grid;
        container.innerHTML = "";
        container.style.setProperty("--cols", this.maze.cols);

        for (const row of this.maze.cells) {
            for (const cellData of row) {
                const cell = document.createElement("div");
                cell.className = "maze-cell";
                cell.dataset.vertex = cellData.id;
                cell.dataset.row = cellData.row;
                cell.dataset.col = cellData.col;
                cell.id = `cell-${cellData.id}`;
                cell.textContent = "";

                const [startRow, startCol] = this.maze.start.split("-").map(Number);
                const [endRow, endCol] = this.maze.end.split("-").map(Number);
                if (cellData.row === startRow && cellData.col === startCol) {
                    cell.classList.add("start");
                    cell.title = `Start: ${cellData.id}`;
                }
                if (cellData.row === endRow && cellData.col === endCol) {
                    cell.classList.add("end");
                    cell.title = `End: ${cellData.id}`;
                }

                container.appendChild(cell);
            }
        }

        // Draw passages from the graph's adjacency list, not from wall data.
        for (const [u, neighbors] of Object.entries(this.maze.graph)) {
            for (const v of neighbors) this.openPassage(u, v);
        }
    }

    openPassage(u, v) {
        const first = this.cellElement(u);
        const second = this.cellElement(v);
        if (!first || !second) return;

        const [r1, c1] = u.split("-").map(Number);
        const [r2, c2] = v.split("-").map(Number);
        const directions = {
            "-1,0": ["borderTop", "borderBottom"],
            "0,1": ["borderRight", "borderLeft"],
            "1,0": ["borderBottom", "borderTop"],
            "0,-1": ["borderLeft", "borderRight"]
        };
        const sides = directions[`${r2 - r1},${c2 - c1}`];
        if (!sides) return;
        first.style[sides[0]] = "2px solid transparent";
        second.style[sides[1]] = "2px solid transparent";
    }

    applyStep(step) {
        if (step.type === "add_edge") {
            this.openPassage(step.u, step.v);
        } else if (step.type === "visit") {
            this.cellElement(step.vertex)?.classList.add("visited");
        } else if (step.type === "current") {
            this.elements.grid.querySelectorAll(".current").forEach(el => el.classList.remove("current"));
            this.cellElement(step.vertex)?.classList.add("current");
        } else if (step.type === "backtrack") {
            this.elements.grid.querySelectorAll(".current").forEach(el => el.classList.remove("current"));
            this.cellElement(step.vertex)?.classList.add("backtrack");
        } else if (step.type === "path") {
            for (const vertex of step.vertices) this.cellElement(vertex)?.classList.add("path");
        }
    }

    showStep(index) {
        if (!this.maze || index < -1 || index >= this.steps.length) return;
        this.currentStep = index;
        this.renderMaze();
        for (let i = 0; i <= index; i++) this.applyStep(this.steps[i]);
        this.elements.stepCounter.textContent = `Step ${index + 1} / ${this.steps.length}`;
        this.elements.status.textContent = this.steps[index]?.message || "Ready";
    }

    nextStep() {
        if (this.currentStep >= this.steps.length - 1) {
            this.pause();
            return;
        }
        this.currentStep += 1;
        const step = this.steps[this.currentStep];
        this.applyStep(step);
        this.elements.stepCounter.textContent = `Step ${this.currentStep + 1} / ${this.steps.length}`;
        this.elements.status.textContent = step.message || "Processing...";
        if (this.currentStep === this.steps.length - 1) this.pause();
    }

    previousStep() {
        if (this.currentStep <= -1) return;
        this.pause();
        this.showStep(this.currentStep - 1);
    }

    reset() {
        this.pause();
        this.showStep(-1);
    }

    play() {
        if (this.interval !== null) {
            this.pause();
            return;
        }
        if (!this.steps.length) return;
        if (this.currentStep >= this.steps.length - 1) this.showStep(-1);
        this.elements.play.textContent = "Pause";
        this.interval = setInterval(() => this.nextStep(), Number(this.elements.speed.value));
    }

    pause() {
        clearInterval(this.interval);
        this.interval = null;
        if (this.elements.play) this.elements.play.textContent = "Play";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    window.mazeVisualizer = new MazeVisualizer();
});
