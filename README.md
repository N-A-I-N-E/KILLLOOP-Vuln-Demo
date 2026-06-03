# killloop-vuln-demo

**Lab-only** vulnerable Python app for KillLoop: SQL injection, secrets, command injection, and a runnable `/user` endpoint for canary tests.

## What breaks KillLoop checks

| Layer | What in this repo |
|-------|-------------------|
| Code (SAST) | `app/db.py`, `app/main.py` SQLi; `app/config.py` secrets; `app/shell_util.py` `os.system` |
| Runtime (canary) | `GET /user?id=1' OR '1'='1` returns a user with `exploit_blocked: false` |

Fixed version lives in sibling folder `../killloop-vuln-demo-fixed/` (use on a PR branch to get **CLOSE**).

## Option A — Run inside KillLoop (no GitHub)

KillLoop maps this folder as `local/demo-vuln`:

```bash
curl -X POST http://localhost:8000/api/runs/trigger \
  -H "Content-Type: application/json" \
  -d '{"repo_full_name":"local/demo-vuln","ticket_id":"DEMO-VULN","finding_id":"SQL_INJECTION","head_sha":"demo-vuln-1"}'
```

Open the GUI run page — expect **REOPEN** on code check.

Full 3-layer simulation (enterprise stack):

```bash
./scripts/simulate_demo_repo_push.sh vulnerable
```

## Option B — Push to GitHub

1. Create a **new empty repo** on GitHub (e.g. `your-org/killloop-vuln-demo`).
2. Copy **only this folder** into it and push:

```bash
cd demo-repo/killloop-vuln-demo
git init
git add .
git commit -m "Initial vulnerable demo"
git branch -M main
git remote add origin git@github.com:YOUR_ORG/killloop-vuln-demo.git
git push -u origin main
```

3. Point KillLoop webhook to your server: `POST /webhooks/github`, event **Pull requests**.
4. Set GitHub repo secrets:
   - `KILLLOOP_URL` — e.g. `https://your-host` or `http://your-ip:8000`
   - `KILLLOOP_STAGING_URL` — URL canary hits, e.g. enterprise staging `http://HOST:8081/user` (see parent `demo-repo/README.md`)
5. Open a PR (or push to PR branch) with title/body containing `[KILLLOOP:FIX]` or label `fix-claimed` when testing a fix branch.

Flow: **PR push → KillLoop webhook (SAST) → this workflow (artifact + deploy URL) → verdict**.
