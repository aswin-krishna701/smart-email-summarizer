const analyzeBtn = document.getElementById("analyzeBtn");
const extractBtn = document.getElementById("extractBtn");
const clearBtn = document.getElementById("clearBtn");
const copyReplyBtn = document.getElementById("copyReplyBtn");

const emailText = document.getElementById("emailText");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const messageBox = document.getElementById("messageBox");

const summary = document.getElementById("summary");
const priority = document.getElementById("priority");
const priorityReason = document.getElementById("priorityReason");
const tone = document.getElementById("tone");
const keyPoints = document.getElementById("keyPoints");
const actionItems = document.getElementById("actionItems");
const suggestedReply = document.getElementById("suggestedReply");

const BACKEND_URL = "http://127.0.0.1:5000/analyze";

function showMessage(message) {
  messageBox.textContent = message;
  messageBox.classList.remove("hidden");
}

function hideMessage() {
  messageBox.textContent = "";
  messageBox.classList.add("hidden");
}

function renderList(element, items) {
  element.innerHTML = "";

  if (!items || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No items found.";
    element.appendChild(li);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    element.appendChild(li);
  });
}

function setLoading(isLoading) {
  loading.classList.toggle("hidden", !isLoading);
  analyzeBtn.disabled = isLoading;
  extractBtn.disabled = isLoading;
  clearBtn.disabled = isLoading;
  analyzeBtn.textContent = isLoading ? "Analyzing..." : "Analyze Email";
}

function resetPriorityStyle() {
  priority.classList.remove("priority-high", "priority-medium", "priority-low");
}

function applyPriorityStyle(priorityValue) {
  resetPriorityStyle();

  const value = priorityValue.toLowerCase();

  if (value === "high") {
    priority.classList.add("priority-high");
  } else if (value === "medium") {
    priority.classList.add("priority-medium");
  } else if (value === "low") {
    priority.classList.add("priority-low");
  }
}

analyzeBtn.addEventListener("click", async () => {
  const text = emailText.value.trim();
  hideMessage();

  if (!text) {
    showMessage("Please paste email text or extract selected text first.");
    return;
  }

  setLoading(true);
  result.classList.add("hidden");
  resetPriorityStyle();

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email_text: text })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.details || data.error || "Backend request failed.");
    }

    const priorityValue = data.priority || "Not classified.";

    summary.textContent = data.summary || "No summary generated.";
    priority.textContent = priorityValue;
    priorityReason.textContent = data.priority_reason || "No priority reason available.";
    tone.textContent = data.tone || "Not detected.";
    suggestedReply.textContent = data.suggested_reply || "No suggested reply generated.";

    applyPriorityStyle(priorityValue);
    renderList(keyPoints, data.key_points);
    renderList(actionItems, data.action_items);

    copyReplyBtn.textContent = "Copy Reply";
    result.classList.remove("hidden");
  } catch (error) {
    showMessage("Error: " + error.message);
    console.error("Extension error:", error);
  } finally {
    setLoading(false);
  }
});

extractBtn.addEventListener("click", async () => {
  hideMessage();

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true
    });

    if (!tab || !tab.id) {
      showMessage("Could not access the current tab.");
      return;
    }

    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection().toString()
    });

    const selectedText = results?.[0]?.result?.trim();

    if (!selectedText) {
      showMessage("Select email text on the page first, then click Extract Selected Text.");
      return;
    }

    emailText.value = selectedText;
  } catch (error) {
    showMessage("Could not extract text from this page. You can paste the email manually.");
    console.error("Text extraction error:", error);
  }
});

clearBtn.addEventListener("click", () => {
  emailText.value = "";
  result.classList.add("hidden");
  hideMessage();
  resetPriorityStyle();
  copyReplyBtn.textContent = "Copy Reply";
});

copyReplyBtn.addEventListener("click", async () => {
  const reply = suggestedReply.textContent.trim();

  if (!reply) {
    showMessage("No reply available to copy.");
    return;
  }

  try {
    await navigator.clipboard.writeText(reply);
    copyReplyBtn.textContent = "Copied!";
    setTimeout(() => {
      copyReplyBtn.textContent = "Copy Reply";
    }, 1200);
  } catch (error) {
    showMessage("Could not copy reply. Please copy it manually.");
    console.error("Copy error:", error);
  }
});