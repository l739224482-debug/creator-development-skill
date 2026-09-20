# Security Boundary

Never print, echo, serialize, or persist a credential value.

- Accept credentials only from the user's runtime environment or authorized secret store.
- Never ask the user to paste a key into chat, a prompt, a command argument, a log, or a tracked file.
- Never search for the author's keys, rotate through unknown keys, or use a fallback account.
- Stop retrying when an error indicates a wrong credential type; offer a compatible user-owned credential, public mode, or a stop.
- Sanitize diagnostics before saving them. Preserve error class and safe context, not headers, tokens, account IDs, private proxies, or full provider payloads.
- Use obvious fictitious values in fixtures. `.env.example` may contain only `your_key_here`.
- Exclude private caches, creator databases, quota history, and internal project paths from public and NAS packages.
- Scan the working tree, Git history, and exact release archive before publication.

Credit reports disclose consumption, remaining credits, method, status, and observation time only. They do not disclose the credential or private account identifier.
