// SIPBULLS User Authentication & Smart Question History Engine

const USER_KEY = "sipbulls_current_user";
const HISTORY_KEY = "sipbulls_test_history_";
const ASKED_KEY = "sipbulls_asked_questions_";

export function getCurrentUser() {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function setCurrentUser(user) {
  if (!user) {
    localStorage.removeItem(USER_KEY);
  } else {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }
}

export function getUserHistory(username) {
  if (!username) return [];
  try {
    const raw = localStorage.getItem(HISTORY_KEY + username);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveUserTestResult(username, resultData) {
  if (!username) return;
  const history = getUserHistory(username);
  history.unshift({
    id: 'test-' + Date.now(),
    date: new Date().toISOString(),
    ...resultData
  });
  // Keep last 50 tests
  localStorage.setItem(HISTORY_KEY + username, JSON.stringify(history.slice(0, 50)));

  // Save asked questions
  const asked = getAskedQuestions(username);
  const newIds = resultData.questionIds || [];
  newIds.forEach(id => asked.add(id));
  localStorage.setItem(ASKED_KEY + username, JSON.stringify([...asked]));
}

export function getAskedQuestions(username) {
  if (!username) return new Set();
  try {
    const raw = localStorage.getItem(ASKED_KEY + username);
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
}

export function selectSmartPaper(bank, username, count = 150) {
  const asked = getAskedQuestions(username);
  // Filter questions not yet asked to this user
  let unasked = bank.filter(q => !asked.has(q.id));

  // Prefer unseen questions. When fewer than `count` remain, use the remaining
  // unseen questions first and only then fill the paper from the least-recently
  // seen questions. This avoids repeats until the bank is exhausted and avoids
  // the old behaviour of immediately resetting to the entire bank.
  const unaskedPaper = shuffle(unasked).slice(0, count);
  if (unaskedPaper.length >= count) return unaskedPaper;

  const selectedIds = new Set(unaskedPaper.map(q => q.id));
  const repeatPool = shuffle(bank.filter(q => !selectedIds.has(q.id) && asked.has(q.id)));
  return [...unaskedPaper, ...repeatPool].slice(0, count);
}

function shuffle(items) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}
