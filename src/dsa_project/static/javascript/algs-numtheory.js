
document.addEventListener("DOMContentLoaded", () => {

    // =================================
    // FORMULA DEFINITIONS
    // =================================

    const formulas = {
        gcd: {
            name: "Greatest Common Divisor (GCD)",
            description: "Find the greatest positive integer that divides both a and b.",
            fields: [
                { id: "a", label: "First Integer", default: 252 },
                { id: "b", label: "Second Integer", default: 198 }
            ]
        },

        lcm: {
            name: "Least Common Multiple (LCM)",
            description: "Find the smallest positive integer that is a multiple of both a and b.",
            fields: [
                { id: "a", label: "First Integer", default: 12 },
                { id: "b", label: "Second Integer", default: 18 }
            ]
        },

        division: {
            name: "Division Algorithm",
            description: "Express a as bq + r, where 0 ≤ r < |b|.",
            fields: [
                { id: "a", label: "Dividend (a)", default: -157 },
                { id: "b", label: "Divisor (b)", default: 23 }
            ]
        },

        divisibility: {
            name: "Divisibility",
            description: "Determine whether a divides b. In other words, whether b = ak for some integer k.",
            fields: [
                { id: "a", label: "Divisor (a)", default: 7 },
                { id: "b", label: "Number (b)", default: 84 }
            ]
        },

        extended_gcd: {
            name: "Extended Euclidean Algorithm",
            description: "Find gcd(a, b) and integers x and y such that gcd(a, b) = ax + by.",
            fields: [
                { id: "a", label: "First Integer", default: 252 },
                { id: "b", label: "Second Integer", default: 198 }
            ]
        },

        binomial_coefficient: {
            name: "Binomial Coefficient",
            description: "Calculate the binomial coefficient C(n, k), also written as n choose k.",
            fields: [
                { id: "n", label: "n", default: 8 },
                { id: "k", label: "k", default: 5 }
            ]
        },

        binomial_term: {
            name: "Binomial Expansion Term",
            description: "Find the coefficient of x^k in the expansion of (ax + b)^n.",
            fields: [
                { id: "n", label: "Exponent (n)", default: 8 },
                { id: "k", label: "Power of x (k)", default: 5 },
                { id: "a", label: "Coefficient of x (a)", default: 2 },
                { id: "b", label: "Constant (b)", default: -3 }
            ]
        }
    };


    // =================================
    // ELEMENTS
    // =================================

    const formulaSelect = document.getElementById("formula-select");
    const description = document.getElementById("formula-description");
    const inputsContainer = document.getElementById("formula-inputs");
    const calculateButton = document.getElementById("calculate-formula");
    const resultContainer = document.getElementById("formula-result");


    // =================================
    // RENDER INPUTS
    // =================================

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


    // =================================
    // DISPLAY RESULT
    // =================================

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


    // =================================
    // EVENT LISTENERS
    // =================================

    formulaSelect.addEventListener("change", renderFormula);
    calculateButton.addEventListener("click", calculate);

    renderFormula();

});
