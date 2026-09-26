# 4. Security

This category covers code and configuration that lets attacker-controlled data
become code, authority, secrets, or an unsafe browser action. Leverage is
highest at trust boundaries: client/server transitions, auth, uploads, HTML
sinks, redirects, and privileged mutations. Trace the data, not just the
syntax.

**Hunt for:**

- `no-danger` — Raw HTML injection can run unsafe markup.
- `dangerous-html-sink` — HTML injection sink with dynamic content.
- `jsx-no-script-url` — `javascript:` URL in JSX.
- `jsx-no-target-blank` — Unsafe `target="_blank"` link for a declared legacy browser or Electron target.
- `no-eval` — `eval()` runs untrusted code strings.
- `no-secrets-in-client-code` — Secret in client code.
- `auth-token-in-web-storage` — Auth token in web storage.
- `untrusted-redirect-following` — Server fetch follows redirects for
  caller-shaped URL.

**Beyond the scan:** Verify authorization server-side, tenant isolation, CSRF
and origin checks, CSP and cookie flags, upload/content-type handling, rate
limits, dependency trust, and logging redaction. A sanitizer at one sink does
not make an untrusted value safe at another; follow it to its source and
privileged effect.
