import { getCurrentUser, setCurrentUser, getUserHistory, getAskedQuestions } from './user.js';

export function initAuthUI() {
  const nav = document.querySelector('.site-header .nav');
  if (!nav) return;

  if (!document.getElementById('user-profile-btn')) {
    const btn = document.createElement('button');
    btn.id = 'user-profile-btn';
    btn.className = 'user-chip';
    updateUserBtnLabel(btn);
    btn.addEventListener('click', openUserModal);
    nav.insertBefore(btn, nav.querySelector('.cta') || nav.lastElementChild);
  }

  if (!document.getElementById('sipbulls-user-modal')) {
    const modalDiv = document.createElement('div');
    modalDiv.id = 'sipbulls-user-modal';
    modalDiv.className = 'hidden';
    modalDiv.style.cssText = 'position:fixed;inset:0;background:rgba(11,31,58,0.78);z-index:200;display:grid;place-items:center;padding:20px;';
    modalDiv.innerHTML = `
      <div class="user-modal-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <div>
            <span class="kicker" style="color:#8a6c0d;background:var(--gold-soft);padding:4px 10px;border-radius:6px;font-size:11px;font-weight:800">SIPBULLS Profile & Tracker</span>
            <h2 id="user-modal-title" style="margin:10px 0 0;font-family:Fraunces,Georgia,serif;color:var(--navy)">User Account</h2>
          </div>
          <button class="btn btn-ghost" id="user-modal-close" style="padding:8px 14px">Close ✕</button>
        </div>
        <div id="user-modal-content"></div>
      </div>
    `;
    document.body.appendChild(modalDiv);

    document.getElementById('user-modal-close').addEventListener('click', closeUserModal);
    modalDiv.addEventListener('click', (e) => {
      if (e.target.id === 'sipbulls-user-modal') closeUserModal();
    });
  }
}

function updateUserBtnLabel(btn) {
  const user = getCurrentUser();
  if (user) {
    btn.innerHTML = `👤 ${user.name} <small style="opacity:0.85;font-size:11px;font-weight:700">(${getUserHistory(user.username).length} tests)</small>`;
  } else {
    btn.innerHTML = `👤 Sign In / Track`;
  }
}

export function openUserModal() {
  const modal = document.getElementById('sipbulls-user-modal');
  const content = document.getElementById('user-modal-content');
  const user = getCurrentUser();

  if (!user) {
    content.innerHTML = `
      <p style="color:var(--muted);margin-bottom:24px;line-height:1.6">Sign in with your name or email to save your mock test performances, track scores over time, and enable the <strong>Smart Question Engine</strong> (which avoids repeating questions you've already answered).</p>
      <form id="login-form" style="display:grid;gap:18px">
        <div>
          <label style="display:block;font-weight:700;font-size:13px;margin-bottom:6px;color:var(--navy)">Your Name or Email</label>
          <input type="text" id="login-name-input" required placeholder="e.g. Rishi Kachhadia" />
        </div>
        <button type="submit" class="btn btn-gold" style="width:100%;font-size:15px;padding:14px">Sign In & Start Tracking →</button>
      </form>
    `;
    modal.classList.remove('hidden');
    document.getElementById('login-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const val = document.getElementById('login-name-input').value.trim();
      if (!val) return;
      const username = val.toLowerCase().replace(/[^a-z0-9]/g, '_');
      setCurrentUser({ name: val, username });
      updateUserBtnLabel(document.getElementById('user-profile-btn'));
      openUserModal(); // Refresh modal view
    });
  } else {
    const history = getUserHistory(user.username);
    const askedCount = getAskedQuestions(user.username).size;
    const bestScore = history.length ? Math.max(...history.map(h => h.score)) : 0;

    content.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;background:var(--cream);padding:18px 22px;border-radius:14px;margin-bottom:24px;border:1px solid var(--line)">
        <div>
          <h3 style="margin:0 0 4px;font-family:Fraunces,Georgia,serif;color:var(--navy);font-size:1.3rem">${user.name}</h3>
          <p class="muted" style="margin:0;font-size:13px">Username ID: <code>${user.username}</code></p>
        </div>
        <button class="btn btn-ghost" id="signout-btn" style="color:var(--danger);border-color:rgba(217,75,75,0.3);background:white">Sign Out</button>
      </div>

      <div style="display:grid;grid-template-columns:repeat(3, minmax(0,1fr));gap:14px;margin-bottom:28px">
        <div class="stat"><b>${history.length}</b><span>Tests Taken</span></div>
        <div class="stat"><b>${bestScore} / 450</b><span>Best Score</span></div>
        <div class="stat"><b>${askedCount}</b><span>Unique Qs Practiced</span></div>
      </div>

      <h3 style="font-family:Fraunces,Georgia,serif;font-size:1.2rem;margin-bottom:14px;color:var(--navy)">Your Mock Test Performance History</h3>
      ${history.length === 0 ? '<p class="muted">No mock tests completed yet. Start a CHA or NISM mock test to build your performance history!</p>' : `
        <div style="max-height:300px;overflow-y:auto;display:grid;gap:12px">
          ${history.map(h => `
            <div class="history-item">
              <div>
                <strong style="color:var(--navy)">${new Date(h.date).toLocaleDateString()} ${new Date(h.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</strong>
                <div class="muted" style="font-size:12px;margin-top:2px">${h.correct} Correct, ${h.wrong} Incorrect, ${h.skipped} Unanswered</div>
              </div>
              <div style="text-align:right">
                <div style="font-weight:700;font-size:15px;color:var(--navy)">${h.score} / 450</div>
                <span class="score-badge ${h.passed ? 'pass' : 'fail'}">${h.passed ? 'Passed (≥270)' : 'Not Passed'}</span>
              </div>
            </div>
          `).join('')}
        </div>
      `}
    `;
    modal.classList.remove('hidden');

    document.getElementById('signout-btn').addEventListener('click', () => {
      setCurrentUser(null);
      updateUserBtnLabel(document.getElementById('user-profile-btn'));
      openUserModal();
    });
  }
}

export function closeUserModal() {
  const modal = document.getElementById('sipbulls-user-modal');
  if (modal) modal.classList.add('hidden');
}
