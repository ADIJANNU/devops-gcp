## Incident: admin user created with an empty password

- **What happened:** While creating the first admin with a hidden password prompt, I pressed Enter with nothing typed. The helper hashed the empty string and inserted the user.
- **Detection:** I queried the users table and found a row with a valid-looking bcrypt hash of the empty password.
- **Impact:** None. No login form existed yet and the site is behind a Cloud Armor allowlist. Row deleted within minutes.
- **Root cause:** The helper printed "12+ chars" but never enforced it.
- **Fix:** Deleted the row. Added a length check that aborts before anything is created.
- **Prevention:** Validate at the boundary, not in the prompt text. Known gap: the API has no minimum password length yet.
