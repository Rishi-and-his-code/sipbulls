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

  // If user has answered all questions, reset or shuffle all
  if (unasked.length < count) {
    unasked = [...bank];
  }

  // Shuffle unasked
  const shuffledUnasked = [...unasked].sort(() => 0.5 - Math.random());
  let paper = shuffledUnasked.slice(0, count);

  // If still need more (e.g. bank smaller than count), pull from remainder
  if (paper.length < count) {
    const remaining = bank.filter(q => !paper.some(p => p.id === q.id));
    const shuffledRem = remaining.sort(() => 0.5 - Math.random());
    paper = [...paper, ...shuffledRem.slice(0, count - paper.length)];
  }

  return paper;
}
