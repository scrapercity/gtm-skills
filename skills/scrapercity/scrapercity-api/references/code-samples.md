# Code Samples: curl, Python, Node

Working clients for the ScraperCity REST API. Each block starts with a `file:` comment naming the file to save it as. The Python files use only the standard library (Python 3.8+). The Node files use only built-ins (Node 18+, for global `fetch`). Every block was checked with `python3 -m py_compile`, `node --check` or `bash -n`, then run end to end against a local mock of the endpoints in `references/endpoint-reference.md`.

Behavior mirrors `lib/client.mjs` in the `scrapercity` npm package: Bearer auth, JSON bodies, the error message read from `error` or `message`, database reads switching from GET to POST past 6,000 characters of query string, and the download path without `/v1`.

`SCRAPERCITY_BASE` exists only so the clients can be pointed at a mock server in tests. Leave it unset in production.

## curl

```bash
# file: scrapercity.sh
# Usage: source scrapercity.sh, then call the functions. Needs curl and jq.
SC_BASE="${SCRAPERCITY_BASE:-https://app.scrapercity.com}"

sc_get() {   # sc_get /api/v1/wallet
  curl -sS --fail-with-body "$SC_BASE$1" -H "Authorization: Bearer $SCRAPERCITY_API_KEY"
}

sc_post() {  # sc_post /api/v1/scrape/maps '{"searchStringsArray":["plumbers"]}'
  curl -sS --fail-with-body -X POST "$SC_BASE$1" \
    -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$2"
}

sc_download() {  # sc_download <runId> out.csv   (path has no /v1)
  curl -sS --fail -o "$2" "$SC_BASE/api/downloads/$1" -H "Authorization: Bearer $SCRAPERCITY_API_KEY"
}

# Every row of a Lead Database search, 100 per call, cursor paging, appended as JSON lines.
sc_leads_all() {  # sc_leads_all out.jsonl  title=CTO country="United States" hasEmail=true
  local out="$1"; shift
  local after="0" args=() kv page next
  for kv in "$@"; do args+=(--data-urlencode "$kv"); done
  : > "$out"
  while :; do
    page=$(curl -sS --fail-with-body -G "$SC_BASE/api/v1/database/leads" \
      -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
      "${args[@]}" --data-urlencode "limit=100" --data-urlencode "after=$after") || return 1
    echo "$page" | jq -c '.data[]' >> "$out"
    next=$(echo "$page" | jq -r '.pagination.next_after // empty')
    [ -z "$next" ] && break
    after="$next"
  done
  wc -l < "$out"
}
```

One-off calls:

```bash
# file: curl-examples.sh
# Balance and plan
curl -sS https://app.scrapercity.com/api/v1/wallet -H "Authorization: Bearer $SCRAPERCITY_API_KEY"

# Start a Google Maps run (returns runId)
curl -sS -X POST https://app.scrapercity.com/api/v1/scrape/maps \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"searchStringsArray":["roofing contractor"],"locationQuery":"Denver, CO","maxCrawledPlacesPerSearch":200}'

# Status, logs, cancel
curl -sS https://app.scrapercity.com/api/v1/scrape/status/RUN_ID -H "Authorization: Bearer $SCRAPERCITY_API_KEY"
curl -sS https://app.scrapercity.com/api/v1/scrape/logs/RUN_ID -H "Authorization: Bearer $SCRAPERCITY_API_KEY"
curl -sS -X POST https://app.scrapercity.com/api/v1/scrape/cancel/RUN_ID -H "Authorization: Bearer $SCRAPERCITY_API_KEY"

# Download the CSV once status is SUCCEEDED
curl -sS --fail -o maps-roofers-denver-co.csv https://app.scrapercity.com/api/downloads/RUN_ID \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY"

# Count a Lead Database search (limit 1, read pagination.total)
curl -sS -G https://app.scrapercity.com/api/v1/database/leads \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
  --data-urlencode "title=VP Sales" --data-urlencode "seniority=vp" \
  --data-urlencode "country=United States" --data-urlencode "minEmployees=50" \
  --data-urlencode "maxEmployees=200" --data-urlencode "hasEmail=true" --data-urlencode "limit=1"

# Long request: a saved search URL goes in a JSON body
curl -sS -X POST https://app.scrapercity.com/api/v1/database/local-businesses \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://www.google.com/maps/search/dentists+in+Austin,+TX/","hasEmail":"true","limit":100,"after":"0"}'
```

## Python

```python
# file: scrapercity_client.py
"""Minimal ScraperCity REST client. Python 3.8+, standard library only.

Set SCRAPERCITY_API_KEY in the environment. SCRAPERCITY_BASE overrides the host for tests only.
"""
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("SCRAPERCITY_BASE", "https://app.scrapercity.com")
LONG_QUERY = 6000      # the npm client switches database reads to POST past this many characters
RATE_LIMIT_WAIT = 30   # seconds to wait after a 429
MAX_TRIES = 5
LEADS = "/api/v1/database/leads"
LOCAL = "/api/v1/database/local-businesses"


class ScraperCityError(Exception):
    def __init__(self, status, message, body=None):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.body = body or {}


def _key():
    key = os.environ.get("SCRAPERCITY_API_KEY", "").strip()
    if not key:
        raise ScraperCityError(401, "SCRAPERCITY_API_KEY is not set")
    return key


def _send(method, path, body=None, raw=False):
    url = path if path.startswith("http") else BASE + path
    data = None if body is None or method == "GET" else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + _key(),
        "Content-Type": "application/json",
        "User-Agent": "my-integration/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = resp.read()
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(text)
        except ValueError:
            parsed = {"raw": text}
        msg = parsed.get("error") or parsed.get("message") or f"HTTP {exc.code}"
        raise ScraperCityError(exc.code, msg, parsed) from None
    if raw:
        return payload
    text = payload.decode("utf-8", "replace")
    try:
        return json.loads(text)
    except ValueError:
        return {"raw": text}


def _retrying(method, path, body=None, raw=False, retry_503=True):
    """Only for calls that are safe to repeat: reads, database queries, cancel."""
    for attempt in range(1, MAX_TRIES + 1):
        try:
            return _send(method, path, body, raw)
        except ScraperCityError as exc:
            retryable = exc.status == 429 or (exc.status == 503 and retry_503)
            if not retryable or attempt == MAX_TRIES:
                raise
            wait = RATE_LIMIT_WAIT if exc.status == 429 else min(60, 2 ** attempt)
        except (urllib.error.URLError, TimeoutError):
            if attempt == MAX_TRIES:
                raise
            wait = min(60, 2 ** attempt)
        time.sleep(wait + random.uniform(0, 1))


def wallet():
    return _retrying("GET", "/api/v1/wallet")


def runs(hours=24, limit=50):
    return _retrying("GET", f"/api/v1/runs?hours={hours}&limit={limit}").get("runs", [])


def status(run_id):
    return _retrying("GET", f"/api/v1/scrape/status/{run_id}")


def logs(run_id):
    return _retrying("GET", f"/api/v1/scrape/logs/{run_id}")


def cancel(run_id):
    return _retrying("POST", f"/api/v1/scrape/cancel/{run_id}")


def download(run_id, out_path):
    """Works only once status is SUCCEEDED, and within 48 hours. The path has no /v1."""
    data = _retrying("GET", f"/api/downloads/{run_id}", raw=True)
    with open(out_path, "wb") as fh:
        fh.write(data)
    return len(data)


def find_recent_run(match, hours=1):
    for run in runs(hours=hours, limit=100):
        if match(run):
            return run.get("run_id")
    return None


def start(slug, body, match=None):
    """Start a paid run once and return its runId.

    match(run) picks this request out of GET /api/v1/runs, for example by file_name.
    On 409 or 429 the same search may already be running, so reuse it.
    On a lost response the run may still have started, so look before resubmitting.
    """
    path = f"/api/v1/scrape/{slug}"
    try:
        return _send("POST", path, body)["runId"]
    except ScraperCityError as exc:
        if exc.status not in (409, 429):
            raise
        code = exc.status
    except (urllib.error.URLError, TimeoutError):
        code = 0
        time.sleep(10)
    found = find_recent_run(match) if match else None
    if found:
        return found
    if code == 409:
        raise ScraperCityError(409, "duplicate refused and no matching run in the last hour")
    if code == 429:
        time.sleep(RATE_LIMIT_WAIT)
    return _send("POST", path, body)["runId"]


def wait_for(run_id, every=30, give_up=1800):
    """Poll a short run. Never use this for scrape_apollo: register a webhook instead."""
    deadline = time.time() + give_up
    while time.time() < deadline:
        s = status(run_id)
        state = s.get("status")
        if state == "SUCCEEDED":
            return s
        if state in ("FAILED", "CANCELLED"):
            raise ScraperCityError(0, f"run {run_id} ended {state}: {s.get('statusMessage', '')}", s)
        time.sleep(every)
    raise TimeoutError(f"run {run_id} still RUNNING after {give_up}s")


def _clean(params):
    out = {}
    for k, v in params.items():
        if v is None or v == "" or v is False:
            continue
        out[k] = "true" if v is True else v
    return out


def db_page(endpoint, params):
    """One database page: GET with repeated keys, or POST with a JSON body when the query is long."""
    params = _clean(params)
    pairs = []
    for k, v in params.items():
        for item in (v if isinstance(v, (list, tuple)) else [v]):
            pairs.append((k, str(item)))
    query = urllib.parse.urlencode(pairs)
    if len(query) > LONG_QUERY:
        return _retrying("POST", endpoint, params, retry_503=False)
    return _retrying("GET", f"{endpoint}?{query}", retry_503=False)


def db_all(endpoint, params, max_rows=None):
    """Every row of a database search, 100 per call, using the after cursor."""
    params = dict(params, limit=100, after="0")
    params.pop("page", None)
    fetched = 0
    while True:
        page = db_page(endpoint, params)
        for row in page.get("data", []):
            yield row
            fetched += 1
            if max_rows and fetched >= max_rows:
                return
        cursor = (page.get("pagination") or {}).get("next_after")
        if cursor in (None, "", 0, "0"):
            return
        params["after"] = str(cursor)
```

A job that uses it: wallet check, count, a capped daily pull of new leads, then validation.

```python
# file: daily_feed.py
import csv
import sys

import scrapercity_client as sc

FILTERS = {
    "title": "VP Sales, Head of Sales",
    "country": ["United States"],
    "minEmployees": 50,
    "maxEmployees": 200,
    "keywords": ["saas"],
    "hasEmail": True,
}
DAILY_CAP = 500
VALIDATE_PRICE = 0.0072  # validate_emails, per email, from references/scrapercity-catalog.md

w = sc.wallet()
balance = float(w["wallet"]["total_balance_dollars"])
print(f"plan={w['plan']['name']} balance=${balance:.2f}")

total = sc.db_page(sc.LEADS, dict(FILTERS, limit=1))["pagination"]["total"]
print(f"matching leads: {total}")

rows = list(sc.db_all(sc.LEADS, dict(FILTERS, excludeDelivered=True), max_rows=DAILY_CAP))
emails = sorted({r["email"].lower() for r in rows if r.get("email")})
cost = len(emails) * VALIDATE_PRICE
print(f"new leads: {len(rows)}, unique emails: {len(emails)}, validation estimate: ${cost:.2f}")
if cost > balance * 0.5:
    sys.exit("validation would use over half the wallet; stop and ask")

if rows:
    with open("leads-new.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=sorted({k for r in rows for k in r}))
        writer.writeheader()
        writer.writerows(rows)

if emails:
    run_id = sc.start("email-validator", {"emails": emails})
    print(f"validator run: {run_id}")
    sc.wait_for(run_id, every=30, give_up=1800)
    size = sc.download(run_id, f"validated-{run_id[:8]}.csv")
    print(f"downloaded {size} bytes")
```

The Python webhook receiver. Register its public URL (with a long random path) at app.scrapercity.com/dashboard/webhooks.

```python
# file: webhook_receiver.py
"""Receives ScraperCity run notifications, confirms them, and downloads results once per run."""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import scrapercity_client as sc

HOOK_PATH = os.environ.get("WEBHOOK_PATH", "/hooks/scrapercity-change-me")
OUT_DIR = os.environ.get("OUT_DIR", "downloads")
SEEN = os.path.join(OUT_DIR, "seen-runs.txt")
LOCK = threading.Lock()


def claim(run_id):
    """Record the runId once; return False if it was already handled."""
    with LOCK:
        os.makedirs(OUT_DIR, exist_ok=True)
        seen = set(open(SEEN).read().split()) if os.path.exists(SEEN) else set()
        if run_id in seen:
            return False
        with open(SEEN, "a") as fh:
            fh.write(run_id + "\n")
        return True


def handle(payload):
    run_id = str(payload.get("runId") or "")
    if not run_id:
        return
    s = sc.status(run_id)  # the notification is a hint; the status call is the check
    if s.get("status") == "RUNNING":
        print(f"run {run_id} still RUNNING; the hourly sweep will pick it up")
        return
    if not claim(run_id):
        return
    if s.get("status") == "SUCCEEDED":
        name = str(payload.get("fileName") or "run").replace("/", "-")[:50]
        path = os.path.join(OUT_DIR, f"{name}-{run_id[:8]}.csv")
        sc.download(run_id, path)
        print(f"saved {path} ({payload.get('leadsCount')} leads reported)")
    else:
        print(f"run {run_id} is {s.get('status')}: {s.get('statusMessage', '')}")


class Hook(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != HOOK_PATH:
            self.send_response(404)
            self.end_headers()
            return
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
        try:
            payload = json.loads(body or b"{}")
        except ValueError:
            print("unreadable webhook body:", body[:200])
            return
        threading.Thread(target=handle, args=(payload,), daemon=True).start()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"listening on :{port}{HOOK_PATH}")
    ThreadingHTTPServer(("0.0.0.0", port), Hook).serve_forever()
```

No retry or signature scheme for notifications is documented, so pair the receiver with an hourly sweep that catches anything a missed delivery left behind. Run it from cron (`0 * * * *`).

```python
# file: sweep.py
"""Hourly: download every SUCCEEDED run from the last 48 hours that the receiver has not handled."""
import os

import scrapercity_client as sc
from webhook_receiver import OUT_DIR, claim

for run in sc.runs(hours=48, limit=100):
    run_id = run.get("run_id")
    if run.get("status") != "SUCCEEDED" or not run_id or not claim(run_id):
        continue
    name = str(run.get("file_name") or "run").replace("/", "-")[:50]
    path = os.path.join(OUT_DIR, f"{name}-{run_id[:8]}.csv")
    sc.download(run_id, path)
    print(f"sweep saved {path}")
```

## Node

```js
// file: scrapercity-client.mjs
// Minimal ScraperCity REST client for Node 18+ (global fetch). No dependencies.
import fs from 'node:fs'
import { randomInt } from 'node:crypto'

const BASE = process.env.SCRAPERCITY_BASE || 'https://app.scrapercity.com'
const LONG_QUERY = 6000
export const LEADS = '/api/v1/database/leads'
export const LOCAL = '/api/v1/database/local-businesses'
export const settings = { rateLimitWaitMs: 30000, maxTries: 5 }
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export class ScraperCityError extends Error {
  constructor (status, message, body = {}) {
    super(`HTTP ${status}: ${message}`)
    this.status = status
    this.body = body
  }
}

function apiKey () {
  const k = (process.env.SCRAPERCITY_API_KEY || '').trim()
  if (!k) throw new ScraperCityError(401, 'SCRAPERCITY_API_KEY is not set')
  return k
}

async function send (method, path, body, raw = false) {
  const url = path.startsWith('http') ? path : BASE + path
  const opts = {
    method,
    headers: {
      Authorization: `Bearer ${apiKey()}`,
      'Content-Type': 'application/json',
      'User-Agent': 'my-integration/1.0'
    },
    signal: AbortSignal.timeout(120000)
  }
  if (body !== undefined && method !== 'GET') opts.body = JSON.stringify(body)
  const res = await fetch(url, opts)
  if (raw && res.ok) return Buffer.from(await res.arrayBuffer())
  const text = await res.text()
  let data
  try { data = JSON.parse(text) } catch { data = { raw: text } }
  if (!res.ok) throw new ScraperCityError(res.status, data.error || data.message || `HTTP ${res.status}`, data)
  return data
}

// Only for calls that are safe to repeat: reads, database queries, cancel.
async function retrying (method, path, body, { raw = false, retry503 = true } = {}) {
  for (let attempt = 1; ; attempt++) {
    try {
      return await send(method, path, body, raw)
    } catch (err) {
      const status = err instanceof ScraperCityError ? err.status : 0
      const retryable = status === 429 || (status === 503 && retry503) || status === 0
      if (!retryable || attempt >= settings.maxTries) throw err
      const backoff = 2 ** attempt * 1000 > 60000 ? 60000 : 2 ** attempt * 1000
      const wait = status === 429 ? settings.rateLimitWaitMs : backoff
      await sleep(wait + randomInt(1000))
    }
  }
}

export const wallet = () => retrying('GET', '/api/v1/wallet')
export const runs = async (hours = 24, limit = 50) =>
  (await retrying('GET', `/api/v1/runs?hours=${hours}&limit=${limit}`)).runs || []
export const status = (runId) => retrying('GET', `/api/v1/scrape/status/${runId}`)
export const logs = (runId) => retrying('GET', `/api/v1/scrape/logs/${runId}`)
export const cancel = (runId) => retrying('POST', `/api/v1/scrape/cancel/${runId}`)

// Works only once status is SUCCEEDED, and within 48 hours. The path has no /v1.
export async function download (runId, outPath) {
  const buf = await retrying('GET', `/api/downloads/${runId}`, undefined, { raw: true })
  fs.writeFileSync(outPath, buf)
  return buf.length
}

export async function findRecentRun (match, hours = 1) {
  const found = (await runs(hours, 100)).find(match)
  return found ? found.run_id : null
}

// Start a paid run once. match(run) picks this request out of GET /api/v1/runs.
export async function start (slug, body, match) {
  const path = `/api/v1/scrape/${slug}`
  let code
  try {
    return (await send('POST', path, body)).runId
  } catch (err) {
    code = err instanceof ScraperCityError ? err.status : 0
    if (code !== 0 && code !== 409 && code !== 429) throw err
    if (code === 0) await sleep(10000)
  }
  const found = match ? await findRecentRun(match) : null
  if (found) return found
  if (code === 409) throw new ScraperCityError(409, 'duplicate refused and no matching run in the last hour')
  if (code === 429) await sleep(settings.rateLimitWaitMs)
  return (await send('POST', path, body)).runId
}

// Poll a short run. Never use this for scrape_apollo: register a webhook instead.
export async function waitFor (runId, { everyMs = 30000, giveUpMs = 1800000 } = {}) {
  const deadline = Date.now() + giveUpMs
  while (Date.now() < deadline) {
    const s = await status(runId)
    if (s.status === 'SUCCEEDED') return s
    if (s.status === 'FAILED' || s.status === 'CANCELLED') {
      throw new ScraperCityError(0, `run ${runId} ended ${s.status}: ${s.statusMessage || ''}`, s)
    }
    await sleep(everyMs)
  }
  throw new Error(`run ${runId} still RUNNING after ${giveUpMs / 1000}s`)
}

function clean (params) {
  const out = {}
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === '' || v === false) continue
    out[k] = v === true ? 'true' : v
  }
  return out
}

// One database page: GET with repeated keys, or POST with a JSON body when the query is long.
export async function dbPage (endpoint, params) {
  const p = clean(params)
  const qs = new URLSearchParams()
  for (const [k, v] of Object.entries(p)) {
    if (Array.isArray(v)) v.forEach((x) => qs.append(k, String(x)))
    else qs.append(k, String(v))
  }
  const query = qs.toString()
  if (query.length > LONG_QUERY) return retrying('POST', endpoint, p, { retry503: false })
  return retrying('GET', `${endpoint}?${query}`, undefined, { retry503: false })
}

// Every row of a database search, 100 per call, using the after cursor.
export async function * dbAll (endpoint, params, maxRows = Infinity) {
  const p = { ...params, limit: 100, after: '0' }
  delete p.page
  let fetched = 0
  while (true) {
    const page = await dbPage(endpoint, p)
    for (const row of page.data || []) {
      yield row
      if (++fetched >= maxRows) return
    }
    const cursor = page.pagination && page.pagination.next_after
    if (cursor === null || cursor === undefined || cursor === '' || String(cursor) === '0') return
    p.after = String(cursor)
  }
}
```

A job that uses it: start a Google Maps run, poll, download.

```js
// file: maps-job.mjs
import * as sc from './scrapercity-client.mjs'

const PRICE = 0.0099 // scrape_maps, per business, from references/scrapercity-catalog.md
const body = {
  searchStringsArray: ['roofing contractor'],
  locationQuery: 'Denver, CO',
  maxCrawledPlacesPerSearch: 200
}

const w = await sc.wallet()
const ceiling = body.searchStringsArray.length * body.maxCrawledPlacesPerSearch * PRICE
console.log(`balance $${w.wallet.total_balance_dollars}, ceiling $${ceiling.toFixed(2)}`)
if (ceiling > Number(w.wallet.total_balance_dollars)) throw new Error('not enough balance')

const runId = await sc.start('maps', body)
console.log(`run ${runId}`)
const done = await sc.waitFor(runId, { everyMs: 120000, giveUpMs: 7200000 })
console.log(`handled ${done.handled} of ${done.requested}`)
const bytes = await sc.download(runId, `maps-roofing-denver-co-${runId.slice(0, 8)}.csv`)
console.log(`saved ${bytes} bytes`)
```

The Node webhook receiver:

```js
// file: webhook-receiver.mjs
// Receives ScraperCity run notifications, confirms them, and downloads results once per run.
import http from 'node:http'
import fs from 'node:fs'
import path from 'node:path'
import * as sc from './scrapercity-client.mjs'

const HOOK_PATH = process.env.WEBHOOK_PATH || '/hooks/scrapercity-change-me'
const OUT_DIR = process.env.OUT_DIR || 'downloads'
const SEEN = path.join(OUT_DIR, 'seen-runs.txt')
fs.mkdirSync(OUT_DIR, { recursive: true })
const seen = new Set(fs.existsSync(SEEN) ? fs.readFileSync(SEEN, 'utf8').split('\n').filter(Boolean) : [])

async function handle (payload) {
  const runId = String(payload.runId || '')
  if (!runId || seen.has(runId)) return
  const s = await sc.status(runId) // the notification is a hint; the status call is the check
  if (s.status === 'RUNNING') {
    console.log(`run ${runId} still RUNNING; the hourly sweep will pick it up`)
    return
  }
  if (seen.has(runId)) return // a second delivery arrived while we were checking
  seen.add(runId)
  fs.appendFileSync(SEEN, runId + '\n')
  if (s.status === 'SUCCEEDED') {
    const name = String(payload.fileName || 'run').replace(/\//g, '-').slice(0, 50)
    const out = path.join(OUT_DIR, `${name}-${runId.slice(0, 8)}.csv`)
    await sc.download(runId, out)
    console.log(`saved ${out} (${payload.leadsCount} leads reported)`)
  } else {
    console.log(`run ${runId} is ${s.status}: ${s.statusMessage || ''}`)
  }
}

http.createServer((req, res) => {
  if (req.method !== 'POST' || req.url !== HOOK_PATH) { res.writeHead(404).end(); return }
  const chunks = []
  req.on('data', (c) => chunks.push(c))
  req.on('end', () => {
    res.writeHead(200).end('ok')
    let payload
    try { payload = JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}') } catch { return }
    handle(payload).catch((err) => console.error('webhook handling failed:', err.message))
  })
}).listen(Number(process.env.PORT || 8080), () => console.log(`listening on ${HOOK_PATH}`))
```

## Test it before pointing it at a paid run

1. `python3 -m py_compile scrapercity_client.py daily_feed.py webhook_receiver.py sweep.py` and `node --check scrapercity-client.mjs maps-job.mjs webhook-receiver.mjs`.
2. Run `wallet()` alone. A 401 means the key is wrong or has stray quotes.
3. Run a database count with `limit: 1`. No wallet charge.
4. Start the cheapest real run you can: `validate_emails` on 3 addresses costs 3 x $0.0072 = $0.02.
5. Post a fake notification to the receiver with a run id you already have: `curl -X POST localhost:8080/hooks/scrapercity-change-me -H "Content-Type: application/json" -d '{"runId":"RUN_ID","fileName":"test","leadsCount":3}'`. It should download once and ignore a second post.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://docs.python.org/3/library/urllib.request.html
- https://docs.python.org/3/library/http.server.html
- https://nodejs.org/api/globals.html#fetch
- https://nodejs.org/api/http.html
- https://curl.se/docs/manpage.html
