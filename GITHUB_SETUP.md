# Publishing this site on GitHub Pages

The whole `website/` folder is the website. `index.html` is the home page; the
other files (`build_site.py`, `curriculum.json`) are the source you regenerate from.
`.nojekyll` tells GitHub to serve the files as-is.

You only have to do the one-time setup once. After that, updating is three steps.

---

## One-time setup

### Option A — no terminal (easiest)
1. Create a free account at <https://github.com> (pick a username, e.g. `crossclampchronicles`).
2. Click **New repository**. Name it `cross-clamp-chronicles`. Set it **Public**. Click **Create repository**.
3. On the new repo page, click **uploading an existing file**.
4. Drag in **everything inside the `website` folder** — `index.html`, `build_site.py`,
   `curriculum.json`, `README.md`, `.nojekyll`. Click **Commit changes**.
5. Go to **Settings → Pages**. Under *Build and deployment*, set **Source = Deploy from a branch**,
   **Branch = main**, **folder = / (root)**. Click **Save**.
6. Wait ~1 minute. Your site is live at:
   `https://<username>.github.io/cross-clamp-chronicles/`

### Option B — with git (if you prefer the command line)
I've already initialized the repo and made the first commit for you. From the
`website` folder, just point it at your new (empty) GitHub repo and push:

```bash
git remote add origin https://github.com/<username>/cross-clamp-chronicles.git
git branch -M main
git push -u origin main
```

Then do step 5 above (Settings → Pages) to turn on hosting.

---

## Updating later (the recurring flow)
1. Add YouTube links to `curriculum.json` (or ask Claude to).
2. Run `python3 build_site.py` to regenerate `index.html`.
3. Re-upload the changed files (Option A: drag them in again) **or** `git add -A && git commit -m "update" && git push` (Option B).

The site refreshes within a minute.

---

## Custom domain (optional, ~$12/yr)
To serve the site at `crossclampchronicles.com` instead of the github.io address:
1. Buy the domain (Namecheap, Cloudflare, Google Domains, etc.).
2. In **Settings → Pages → Custom domain**, type the domain and Save. GitHub adds a
   `CNAME` file to the repo automatically.
3. At your domain registrar, add the DNS records GitHub shows you (four `A` records
   for the apex domain, or a `CNAME` record pointing `www` to `<username>.github.io`).
4. Tick **Enforce HTTPS** once it's verified.
