document.addEventListener("DOMContentLoaded", () => {

    const formulaSelect = document.getElementById("formula-select");
    const description = document.getElementById("formula-description");
    const inputsContainer = document.getElementById("formula-inputs");
    const calculateButton = document.getElementById("calculate-formula");
    const resultContainer = document.getElementById("formula-result");

    // render input fields(forms)
    function renderFormula() {
        const selected = formulaSelect.value;
        const formula = formulas[selected];

        description.textContent = formula.description;
        inputsContainer.replaceChildren();

        formula.fields.forEach(field => {
            const wrapper = document.createElement("div");
            wrapper.className = "formula-input";

            const label = document.createElement("label");
            label.htmlFor = `formula-${field.id}`;
            label.textContent = field.label;

            const input = document.createElement("input");
            input.type = "number";
            input.id = `formula-${field.id}`;
            input.name = field.id;
            input.value = field.default;
            input.step = "1";
            input.required = true;

            wrapper.append(label, input);
            inputsContainer.appendChild(wrapper);
        });

        resultContainer.textContent = "Enter your values and calculate to see the result.";
    }

    //right side result display 
    function displayResult(result) {
        resultContainer.replaceChildren();

        if (result === null || result === undefined) {
            resultContainer.textContent = "No result returned.";
            return;
        }

        if (typeof result !== "object") {
            const value = document.createElement("p");
            value.className = "result-value";
            value.textContent = result;
            resultContainer.appendChild(value);
            return;
        }

        // Give special treatment to common result types
        if (result.equation) {
            const equation = document.createElement("p");
            equation.className = "result-equation";
            equation.textContent = result.equation;
            resultContainer.appendChild(equation);
        }

        if (result.message) {
            const message = document.createElement("p");
            message.className = "result-message";
            message.textContent = result.message;
            resultContainer.appendChild(message);
        }

        // Display remaining result properties
        Object.entries(result).forEach(([key, value]) => {
            if (key === "equation" || key === "message") return;

            const row = document.createElement("div");
            row.className = "result-row";

            const label = document.createElement("span");
            label.textContent = key.replaceAll("_", " ");

            const output = document.createElement("strong");
            output.textContent = value;

            row.append(label, output);
            resultContainer.appendChild(row);
        });
    }


    // =================================
    // CALCULATE
    // =================================

    async function calculate() {
        const operation = formulaSelect.value;
        const formula = formulas[operation];

        const values = {};

        for (const field of formula.fields) {
            const input = document.getElementById(`formula-${field.id}`);
            const value = input.value.trim();

            if (value === "" || !Number.isSafeInteger(Number(value))) {
                resultContainer.textContent = `Please enter a valid integer for ${field.label}.`;
                input.focus();
                return;
            }

            values[field.id] = Number(value);
        }

        calculateButton.disabled = true;
        calculateButton.textContent = "Calculating...";

        try {
            const response = await fetch("/algorithms/number-theory", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    operation,
                    values
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Something went wrong.");
            }
            displayResult(data.result);

        } catch (error) {
            resultContainer.textContent = error.message;
        } finally {
            calculateButton.disabled = false;
            calculateButton.textContent = "Calculate";
        }
    }


    formulaSelect.addEventListener("change", renderFormula);
    calculateButton.addEventListener("click", calculate);

    renderFormula();

});
