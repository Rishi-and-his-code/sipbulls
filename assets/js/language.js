const LANGUAGE_KEY = 'sipbulls-language';
const LEGACY_LANGUAGE_KEY = 'cha-language';
const COOKIE_MAX_AGE = 60 * 60 * 24 * 365;

function isLanguage(value) {
  return value === 'en' || value === 'hi';
}

function readCookie() {
  const match = document.cookie.match(/(?:^|; )sipbulls-language=([^;]*)/);
  return match ? decodeURIComponent(match[1]) : null;
}

export function getLanguage() {
  try {
    const saved = localStorage.getItem(LANGUAGE_KEY);
    if (isLanguage(saved)) return saved;
  } catch {
    // Use the cookie fallback below when storage is blocked.
  }

  const cookieLanguage = readCookie();
  if (isLanguage(cookieLanguage)) return cookieLanguage;

  // Do not use the old CHA-only key: it caused old Hindi selections to
  // override the new English default on every fresh page load.
  return 'en';
}

export function setLanguage(language) {
  const selected = isLanguage(language) ? language : 'en';

  try {
    localStorage.setItem(LANGUAGE_KEY, selected);
    // Remove the old key so legacy state can never override this preference.
    localStorage.removeItem(LEGACY_LANGUAGE_KEY);
  } catch {
    // Cookie persistence keeps the preference when localStorage is blocked.
  }

  try {
    document.cookie = `${LANGUAGE_KEY}=${encodeURIComponent(selected)}; Max-Age=${COOKIE_MAX_AGE}; Path=/; SameSite=Lax`;
  } catch {
    // The page still uses the selected value for this render.
  }

  document.documentElement.lang = selected === 'hi' ? 'hi' : 'en';
  window.dispatchEvent(new CustomEvent('sipbulls-language-change', { detail: selected }));
  return selected;
}

export function setupLanguageToggle(button, onChange) {
  if (!button) return;

  let language = setLanguage(getLanguage());
  const updateButton = () => {
    button.textContent = language === 'en' ? 'हिंदी' : 'English';
    button.setAttribute('aria-label', language === 'en' ? 'Switch to Hindi' : 'Switch to English');
    button.setAttribute('title', language === 'en' ? 'Switch to Hindi' : 'Switch to English');
  };

  updateButton();
  button.addEventListener('click', () => {
    language = setLanguage(language === 'en' ? 'hi' : 'en');
    updateButton();
    onChange?.(language);
  });

  onChange?.(language);
}
