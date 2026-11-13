//temp. will refactor everything about bn_tree

const svg = document.getElementById("tree-svg");

const rootInput = document.getElementById("root-value");
const nodeInput = document.getElementById("node-value");
const nodeSide = document.getElementById("node-side");

const createRootControls = document.getElementById("create-root-controls");
const nodeControls = document.getElementById("node-controls");

const selectedLabel = document.getElementById("selected-node");
const nodeCountLabel = document.getElementById("node-count");

const traversalMethod = document.getElementById("traversal-method");
const traversalResult = document.getElementById("traversal-result");
const traversalStatus = document.getElementById("traversal-status");
const traverseButton = document.getElementById("traverse-btn");

const deleteButton = document.getElementById("delete-node-btn");
const messageElement = document.getElementById("message");

let treeData = null;
let selectedNodeId = null;
let activeNodeId = null;
let animationToken = 0;

async function apiRequest(url, method = "GET", body = null) {
    const options = { method };

    if (body !== null) {
        options.headers = {
            "Content-Type": "application/json"
        };
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || "Something went wrong.");
    }

    return result;
}


let messageTimeout;

function showMessage(message) {
    messageElement.textContent = message;
    messageElement.classList.add("show");

    clearTimeout(messageTimeout);

    messageTimeout = setTimeout(() => {
        messageElement.classList.remove("show");
    }, 2500);
}



function drawTree() {
    svg.innerHTML = "";

    if (!treeData) {
        const text = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "text"
        );

        text.setAttribute("x", 300);
        text.setAttribute("y", 175);
        text.setAttribute("class", "empty-text");
        text.textContent = "Create a root node to get started.";

        svg.setAttribute("viewBox", "0 0 600 350");
        svg.setAttribute("width", "600");
        svg.setAttribute("height", "350");
        svg.appendChild(text);

        nodeCountLabel.textContent = "0 Nodes";
        return;
    }

    const positions = new Map();
    let index = 0;
    let maxDepth = 0;

    function calculatePositions(node, depth = 0) {
        if (!node) return;

        maxDepth = Math.max(maxDepth, depth);
        calculatePositions(node.left, depth + 1);

        positions.set(node.id, {
            x: 50 + index * 100,
            y: 60 + depth * 100
        });

        index++;
        calculatePositions(node.right, depth + 1);
    }

    calculatePositions(treeData);

    const width = Math.max(600, index * 100 + 100);
    const height = Math.max(350, (maxDepth + 1) * 100 + 100);

    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);

    function drawEdges(node) {
        if (!node) return;

        const parent = positions.get(node.id);

        [node.left, node.right].forEach(child => {
            if (!child) return;

            const childPosition = positions.get(child.id);
            const line = document.createElementNS(
                "http://www.w3.org/2000/svg",
                "line"
            );

            line.setAttribute("x1", parent.x);
            line.setAttribute("y1", parent.y);
            line.setAttribute("x2", childPosition.x);
            line.setAttribute("y2", childPosition.y);
            line.setAttribute("class", "edge");

            svg.appendChild(line);
        });

        drawEdges(node.left);
        drawEdges(node.right);
    }

    drawEdges(treeData);

    function drawNodes(node) {
        if (!node) return;

        const position = positions.get(node.id);
        const circle = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "circle"
        );

        circle.setAttribute("cx", position.x);
        circle.setAttribute("cy", position.y);
        circle.setAttribute("r", 25);

        let className = "node-circle";

        if (node.id === selectedNodeId) className += " selected";
        if (node.id === activeNodeId) className += " active";

        circle.setAttribute("class", className);

        circle.addEventListener("click", () => {
            animationToken++;
            activeNodeId = null;
            selectedNodeId = node.id;

            selectedLabel.textContent = `${node.data} (ID: ${node.id})`;
            deleteButton.disabled = false;

            drawTree();
        });

        svg.appendChild(circle);

        const text = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "text"
        );

        text.setAttribute("x", position.x);
        text.setAttribute("y", position.y);
        text.setAttribute("class", "node-text");
        text.textContent = node.data;
        svg.appendChild(text);

        const idText = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "text"
        );

        idText.setAttribute("x", position.x);
        idText.setAttribute("y", position.y + 40);
        idText.setAttribute("class", "node-id");
        idText.textContent = `ID: ${node.id}`;
        svg.appendChild(idText);

        drawNodes(node.left);
        drawNodes(node.right);
    }

    drawNodes(treeData);
    nodeCountLabel.textContent = `${positions.size} Nodes`;
}



function updateTree(data) {
    treeData = data.tree;

    const hasRoot = treeData !== null;

    createRootControls.hidden = hasRoot;
    nodeControls.hidden = !hasRoot;
    traverseButton.disabled = !hasRoot;

    if (
        selectedNodeId !== null &&
        !findNode(treeData, selectedNodeId)
    ) {
        selectedNodeId = null;
    }

    if (selectedNodeId === null) {
        selectedLabel.textContent = "None";
        deleteButton.disabled = true;
    }

    drawTree();
}


function findNode(node, id) {
    if (!node) return null;
    if (node.id === id) return node;

    return findNode(node.left, id) || findNode(node.right, id);
}


//create button
async function createRoot() {
    const value = rootInput.value.trim();

    if (!value) {
        showMessage("Enter a root value.");
        return;
    }

    try {
        animationToken++;

        const result = await apiRequest(
            "/binary-tree/create",
            "POST",
            { data: value }
        );

        selectedNodeId = result.tree.id;
        activeNodeId = null;
        rootInput.value = "";

        updateTree(result);
        selectedLabel.textContent = `${result.tree.data} (ID: ${result.tree.id})`;
        deleteButton.disabled = false;

        showMessage("Root created.");
    } catch (error) {
        showMessage(error.message);
    }
}


//add button
async function addNode() {
    if (selectedNodeId === null) {
        showMessage("Select a parent node first.");
        return;
    }

    const value = nodeInput.value.trim();

    if (!value) {
        showMessage("Enter a node value.");
        return;
    }

    try {
        animationToken++;

        const result = await apiRequest(
            "/binary-tree/add",
            "POST",
            {
                parent_id: selectedNodeId,
                data: value,
                side: nodeSide.value
            }
        );

        activeNodeId = null;
        updateTree(result);
        nodeInput.value = "";

        showMessage("Node added.");
    } catch (error) {
        showMessage(error.message);
    }
}


//delete button

async function deleteNode() {
    if (selectedNodeId === null) {
        showMessage("Select a node first.");
        return;
    }

    if (!confirm("Delete this node and all its descendants?")) return;

    try {
        animationToken++;

        const result = await apiRequest(
            "/binary-tree/delete",
            "POST",
            { node_id: selectedNodeId }
        );

        selectedNodeId = null;
        activeNodeId = null;
        selectedLabel.textContent = "None";

        updateTree(result);
        showMessage("Node deleted.");
    } catch (error) {
        showMessage(error.message);
    }
}


//travers

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function displayTraversal(steps, currentIndex = -1) {
    traversalResult.innerHTML = "";

    if (!steps.length) {
        traversalResult.textContent = "No nodes to display.";
        return;
    }

    steps.forEach((step, index) => {
        const item = document.createElement("span");
        item.className = "result-node";

        if (index === currentIndex) {
            item.classList.add("current");
        }

        item.textContent = step.data;
        traversalResult.appendChild(item);
    });
}


async function traverse() {
    try {
        const result = await apiRequest(
            "/binary-tree/traverse",
            "POST",
            { method: traversalMethod.value }
        );

        const token = ++animationToken;
        activeNodeId = null;

        const steps = result.steps;
        traversalStatus.textContent = "Running";
        displayTraversal(steps);

        for (let i = 0; i < steps.length; i++) {
            if (token !== animationToken) return;

            activeNodeId = steps[i].id;
            drawTree();
            displayTraversal(steps, i);

            traversalStatus.textContent = `Visiting ${i + 1} / ${steps.length}`;
            await sleep(650);
        }

        if (token !== animationToken) return;

        activeNodeId = null;
        drawTree();
        displayTraversal(steps);
        traversalStatus.textContent = "Complete";

    } catch (error) {
        showMessage(error.message);
        traversalStatus.textContent = "Ready";
    }
}


//reset button

function resetTree() {
    if (!confirm("Reset the entire tree?")) return;
    window.location.reload();
}




document.getElementById("create-root-btn")
    .addEventListener("click", createRoot);

document.getElementById("add-node-btn")
    .addEventListener("click", addNode);

document.getElementById("delete-node-btn")
    .addEventListener("click", deleteNode);

document.getElementById("traverse-btn")
    .addEventListener("click", traverse);

document.getElementById("reset-btn")
    .addEventListener("click", resetTree);



async function init() {
    try {
        const result = await apiRequest("/binary-tree/data");
        updateTree(result);
    } catch (error) {
        showMessage(error.message);
    }
}

init();
