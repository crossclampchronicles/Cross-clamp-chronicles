# Publishing Cross-Clamp Chronicles at crossclampchronicles.com

Step-by-step, start to finish. The site is the whole `website/` folder; it's already a git repo
and a `CNAME` file (containing `crossclampchronicles.com`) is in place. Hosting is **free** on
GitHub Pages; the only cost is the domain (~$10–15/yr).

Two ways to do the GitHub part: **Terminal (git)** is cleanest for ongoing updates and is shown
first; a **no-terminal drag-and-drop** option is at the bottom.

---

## Step 0 — clean up leftover git lock files (do this once)

A previous automated step left three empty `.lock` files in `.git` that I couldn't delete from
my sandbox. Remove them on your Mac so git works:

```bash
cd "/Users/johnbryant/Documents/Claude/Projects/ABA cardiac lectures/website"
rm -f .git/HEAD.lock .git/packed-refs.lock .git/refs/heads/*.lock .git/index.lock
git status      # should run cleanly now
```

---

## Step 1 — create the GitHub repository

1. Sign in at <https://github.com>.
2. Top-right **+ → New repository**.
3. **Repository name:** `cross-clamp-chronicles`
4. Set **Public**. Do **not** add a README, .gitignore, or license (the folder already has them).
5. Click **Create repository**. Leave that page open — you'll need the URL it shows.

---

## Step 2 — push the site to GitHub (Terminal)

From the `website` folder:

```bash
cd "/Users/johnbryant/Documents/Claude/Projects/ABA cardiac lectures/website"
git branch -M main
git add -A
git commit -m "Publish site + CNAME for crossclampchronicles.com"
git remote add origin https://github.com/<your-username>/cross-clamp-chronicles.git
git push -u origin main
```

Replace `<your-username>`. If it asks for a password, use a **Personal Access Token**
(GitHub → Settings → Developer settings → Personal access tokens), not your account password.

> Already have a remote from a past attempt? Use `git remote set-url origin <url>` instead of `add`.

---

## Step 3 — turn on GitHub Pages

1. In the repo: **Settings → Pages**.
2. **Build and deployment → Source:** *Deploy from a branch*.
3. **Branch:** `main`, **folder:** `/ (root)`. **Save**.
4. Wait ~1 minute. A temporary address appears:
   `https://<your-username>.github.io/cross-clamp-chronicles/` — confirm the site loads there first.

---

## Step 4 — buy the domain

1. Buy **crossclampchronicles.com** at any registrar — **Cloudflare** (at-cost) or **Namecheap**
   are good. Porkbun and Squarespace Domains also fine.
2. You only need the domain itself. Skip the upsells (privacy is usually free/included).

---

## Step 5 — point the domain at GitHub (DNS records)

In your registrar's **DNS settings**, add these records. (Values are GitHub's current,
verified June 2026.)

**Apex domain (crossclampchronicles.com) — four A records:**

| Type | Host/Name | Value |
|------|-----------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

**Recommended — four AAAA records (IPv6), same Host `@`:**

`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`

**www subdomain — one CNAME record:**

| Type | Host/Name | Value |
|------|-----------|-------|
| CNAME | www | `<your-username>.github.io` |  ← note the trailing dot if your registrar requires it |

Delete any pre-existing parking/“A @” records the registrar added. DNS can take from a few
minutes up to ~24 hours to propagate.

---

## Step 6 — connect the domain in GitHub + HTTPS

1. **Settings → Pages → Custom domain:** type `crossclampchronicles.com` → **Save**.
   (The repo already contains the matching `CNAME` file, so this should verify quickly.)
2. Wait for the green “DNS check successful.”
3. Tick **Enforce HTTPS** (may take a little while to become available while a certificate
   is issued). Done — the site is live at **https://crossclampchronicles.com**, and `www`
   redirects to it automatically.

---

## Updating the site later (the recurring flow)

1. Add YouTube links to `curriculum.json` (or ask me to — I pull them from the recording tracker).
2. Regenerate the pages:
   ```bash
   python3 build_site.py
   ```
3. Publish:
   ```bash
   git add -A && git commit -m "update lectures" && git push
   ```
   The live site refreshes within a minute.

---

## No-terminal alternative (Steps 1–3)

After Step 0, on the new empty repo page click **“uploading an existing file,”** drag in
**everything inside `website/`** (including the hidden `.nojekyll` and `CNAME`), and **Commit**.
Then do Step 3. Updating later means dragging changed files in again. Steps 4–6 are identical.

---

### Quick reference
- Repo: `https://github.com/<your-username>/cross-clamp-chronicles`
- Test URL: `https://<your-username>.github.io/cross-clamp-chronicles/`
- Live URL: `https://crossclampchronicles.com`
- A records: 185.199.108–111.153 · CNAME www → `<your-username>.github.io`
