# SIPBULLS — NISM Series V-D Exam Prep

Practice site by **SIPBULLS** (founder **Yagnesh Kachhadia**) for the **NISM Series V-D — Mutual Fund (Specialized Investment Fund) Distributors** certification.

**Live domain:** [sipbulls.com](https://sipbulls.com)

**Contact:** [yagnesh2879@gmail.com](mailto:yagnesh2879@gmail.com) · +91 98794 57057

## Publish sipbulls.com (GitHub Pages + GoDaddy)

This site is static. GitHub hosts the files for free. GoDaddy only needs to point the domain at GitHub.

### 1. Put only the website on GitHub

Do **not** upload the study PDFs or the raw HTML question dumps. The live site only needs:

- `index.html`, `bank.html`, `exam.html`
- `assets/`
- `data/`
- `CNAME` (already set to `sipbulls.com`)
- `README.md`, `.gitignore`

In Terminal, from this project folder:

```bash
cd "/Users/rishikachhadia/Documents/RISHI/CODING/NISM V D Exam"

git add index.html bank.html exam.html CNAME README.md .gitignore assets data
git commit -m "Publish SIPBULLS NISM V-D prep site"
```

Create a **public** GitHub repository (example name: `sipbulls`), then:

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/sipbulls.git
git branch -M main
git push -u origin main
```

The repository must be **public** unless you have GitHub Pro (private Pages is a paid feature).

### 2. Turn on GitHub Pages

1. Open the repo on GitHub → **Settings** → **Pages**.
2. **Source:** Deploy from a branch.
3. **Branch:** `main` / folder `/ (root)`.
4. **Custom domain:** `sipbulls.com` → Save.
5. Wait until GitHub shows the domain. Leave **Enforce HTTPS** off until DNS works, then turn it on.

### 3. Point GoDaddy DNS at GitHub

In [GoDaddy DNS](https://dcc.godaddy.com/manage/sipbulls.com/dns):

1. Delete the parking / “Launching Soon” **A** records and any GoDaddy forwarding for `sipbulls.com`.
2. Keep **MX** records if you use GoDaddy email.
3. Add these **A** records for `@` (the root domain):

| Type | Name | Value | TTL |
|------|------|--------|-----|
| A | @ | 185.199.108.153 | 600 |
| A | @ | 185.199.109.153 | 600 |
| A | @ | 185.199.110.153 | 600 |
| A | @ | 185.199.111.153 | 600 |
| CNAME | www | YOUR_GITHUB_USERNAME.github.io | 600 |

Replace `YOUR_GITHUB_USERNAME` with your real GitHub username.

DNS often updates in 10–60 minutes; it can take up to 24 hours.

### 4. Turn on HTTPS

When `http://sipbulls.com` loads this site:

1. GitHub → Settings → Pages → **Enforce HTTPS**.
2. Visit `https://sipbulls.com`.

## Run locally

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

## Rebuild the question bank

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/extract_questions.py
```

A SIPBULLS product. Unofficial practice tool — not affiliated with NISM or SEBI.
