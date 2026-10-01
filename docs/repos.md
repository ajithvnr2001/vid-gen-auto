# Reference repos — what each contributed (from ins.txt)

## kairi003/Get-cookies.txt-Locally
Browser extension exporting the current tab's cookies as Netscape `cookies.txt`
(7 TAB fields: domain, subdomain-flag, path, secure-flag, expiry, name, value;
`#HttpOnly_` prefix lines). Used for the session-bootstrap attempt
(`scripts/01_cookies_probe.py` maps each line to a Playwright cookie dict).
Lesson: Google's `g.a000…` bound sessions reject datacenter IPs, so cookies.txt
is a fallback, not the primary path — live login (script 02) is.

## D4Vinci/Scrapling
Adaptive scraping framework. Used here: `Fetcher` (TLS-impersonating HTTP) for
the static docs crawl and `DynamicFetcher` (Playwright Chromium, `network_idle`)
for JS-rendered help pages — see `tools/crawl_flow_docs.py`. Useful unused
patterns for Flow work: `DynamicSession`/`StealthySession` for persistent
logged-in sessions, `capture_xhr` to intercept Flow's internal JSON APIs instead
of scraping DOM, `cdp_url` for remote browsers.

## ScrapeGraphAI/Scrapegraph-ai
LLM-driven extraction (`SmartScraperGraph`). Evaluated and deliberately NOT used
as the automation driver: no cookie session management, nondeterministic output,
per-run token cost/latency. Sensible only as a downstream helper over already-
fetched HTML. Kept documented so nobody re-tries it as the driver.

## microsoft/playwright (+ playwright-mcp)
The actual driver. Used: `add_cookies` injection, `storage_state` pattern
(cookies + localStorage beats cookies.txt for SPAs), `connect_over_cdp` to a
live Chrome, auto-waiting locators, `force=True` clicks through CDK backdrops,
`Browser.setDownloadBehavior` for dialog-free downloads, aria-snapshot polling
instead of `time.sleep` for generation completion, `request` context sharing
cookies for direct API calls.
