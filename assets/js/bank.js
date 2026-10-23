import {
  loadQuestions,
  escapeHtml,
  optionLetter,
  subjectLabel,
} from "./common.js";
import { initAuthUI } from "./auth-ui.js";

const PAGE_SIZE = 20;
const state = {
  all: [],
  filtered: [],
  subject: "all",
  query: "",
  page: 1,
};

const listEl = document.getElementById("list");
const statusEl = document.getElementById("status");
const pagerEl = document.getElementById("pager");
const searchEl = document.getElementById("search");

function applyFilter() {
  const q = state.query.trim().toLowerCase();
  state.filtered = state.all.filter((item) => {
    if (state.subject !== "all" && item.subject !== state.subject) return false;
    if (!q) return true;
    const blob = [
      item.stem,
      item.explanation,
      ...(item.options || []),
    ].join(" ").toLowerCase();
    return blob.includes(q);
  });
  const maxPage = Math.max(1, Math.ceil(state.filtered.length / PAGE_SIZE));
  if (state.page > maxPage) state.page = 1;
  render();
}

function render() {
  const total = state.filtered.length;
  const start = (state.page - 1) * PAGE_SIZE;
  const slice = state.filtered.slice(start, start + PAGE_SIZE);
  statusEl.textContent = total
    ? `Showing ${start + 1}–${start + slice.length} of ${total} questions`
    : "No questions match your filters.";

  listEl.innerHTML = slice.map((item, idx) => {
    const n = start + idx + 1;
    const options = item.options.map((opt, i) => {
      const correct = i === item.correctIndex;
      return `<div class="option${correct ? " correct" : ""}"><strong>${optionLetter(i)}.</strong> ${escapeHtml(opt)}${correct ? " ✓" : ""}</div>`;
    }).join("");
    const correctText = item.options[item.correctIndex] || "";
    return `
      <article class="q-card">
        <div class="q-meta">
          <span class="badge ${item.subject}">${escapeHtml(subjectLabel(item.subject))}</span>
          <span class="muted">Q ${n}</span>
        </div>
        <p class="q-stem">${escapeHtml(item.stem)}</p>
        <div class="options">${options}</div>
        <div class="answer-box">Correct answer: ${optionLetter(item.correctIndex)}. ${escapeHtml(correctText)}</div>
        <div class="explain-box"><strong>Explanation</strong><div>${escapeHtml(item.explanation)}</div></div>
      </article>
    `;
  }).join("");

  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  pagerEl.innerHTML = `
    <button class="btn btn-ghost" id="prev-page" ${state.page <= 1 ? "disabled" : ""}>Previous</button>
    <span class="muted">Page ${state.page} of ${pages}</span>
    <button class="btn btn-gold" id="next-page" ${state.page >= pages ? "disabled" : ""}>Next</button>
  `;
  document.getElementById("prev-page").onclick = () => {
    state.page -= 1;
    window.scrollTo({ top: 0, behavior: "smooth" });
    render();
  };
  document.getElementById("next-page").onclick = () => {
    state.page += 1;
    window.scrollTo({ top: 0, behavior: "smooth" });
    render();
  };
}

document.getElementById("filters").addEventListener("click", (e) => {
  const btn = e.target.closest("[data-subject]");
  if (!btn) return;
  state.subject = btn.dataset.subject;
  state.page = 1;
  document.querySelectorAll("#filters .chip").forEach((c) => c.classList.toggle("active", c === btn));
  applyFilter();
});

searchEl.addEventListener("input", () => {
  state.query = searchEl.value;
  state.page = 1;
  applyFilter();
});

initAuthUI();

try {
  state.all = await loadQuestions();
  applyFilter();
} catch (err) {
  statusEl.textContent = "Could not load the question bank. Serve this folder over HTTP (GitHub Pages or a local static server).";
  console.error(err);
}
