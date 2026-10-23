// SIPBULLS User Authentication & Smart Question History Engine

const USER_KEY = "sipbulls_current_user";
const HISTORY_KEY = "sipbulls_test_history_";
const ASKED_KEY = "sipbulls_asked_questions_";

function examKey(examType) {
  return examType === "nism-vd" ? "nism-vd" : "cha";
}

function scopedKey(prefix, username, examType) {
  return `${prefix}${examKey(examType)}_${username}`;
}

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

export function getUserHistory(username, examType) {
  if (!username) return [];
  try {
    const scoped = localStorage.getItem(scopedKey(HISTORY_KEY, username, examType));
    if (scoped) return JSON.parse(scoped);

    // Older releases stored all results in one unscoped CHA history key.
    // Keep those existing results visible while the user data migrates.
    const legacy = localStorage.getItem(HISTORY_KEY + username);
    if (legacy && examKey(examType) === "cha") {
      const migrated = JSON.parse(legacy).map((entry) => ({ ...entry, examType: "cha" }));
      localStorage.setItem(scopedKey(HISTORY_KEY, username, "cha"), JSON.stringify(migrated.slice(0, 50)));
      return migrated.slice(0, 50);
    }
    return [];
  } catch {
    return [];
  }
}

export function saveUserTestResult(username, resultData, examType) {
  if (!username) return;
  const history = getUserHistory(username, examType);
  history.unshift({
    id: 'test-' + Date.now(),
    date: new Date().toISOString(),
    examType: examKey(examType),
    ...resultData
  });
  // Keep the last 50 tests for each examination separately.
  localStorage.setItem(scopedKey(HISTORY_KEY, username, examType), JSON.stringify(history.slice(0, 50)));

  // Save asked questions only after a completed test, scoped to its question bank.
  const asked = getAskedQuestions(username, examType);
  const newIds = resultData.questionIds || [];
  newIds.forEach(id => asked.add(id));
  localStorage.setItem(scopedKey(ASKED_KEY, username, examType), JSON.stringify([...asked]));
}

export function getAskedQuestions(username, examType) {
  if (!username) return new Set();
  try {
    const raw = localStorage.getItem(scopedKey(ASKED_KEY, username, examType));
    if (raw) return new Set(JSON.parse(raw));
    if (examKey(examType) === "cha") {
      const legacy = localStorage.getItem(ASKED_KEY + username);
      if (legacy) {
        const ids = new Set(JSON.parse(legacy));
        localStorage.setItem(scopedKey(ASKED_KEY, username, "cha"), JSON.stringify([...ids]));
        return ids;
      }
    }
    return new Set();
  } catch {
    return new Set();
  }
}

export function selectSmartPaper(bank, username, count = 150, examType) {
  const asked = getAskedQuestions(username, examType);
  // Filter questions not yet asked to this user.
  const unasked = bank.filter(q => !asked.has(q.id));

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
