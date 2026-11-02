## Drill: restore the nightly backup into a scratch database

- **What I did:** Downloaded the latest dump from the backup bucket and restored it into a scratch database (restore_test) in the same Postgres, then compared row counts with the live database.
- **Result:** Row counts for companies, equipment, users and readings matched exactly between live and restored databases.
- **Measured restore time (RTO):** not recorded on this run, to be measured on the next drill
- **Recovery point (RPO):** up to ~24 hours of readings, since the backup runs daily at 02:00 UTC.
- **Cleanup:** Dropped the scratch database and deleted the local dump (it contains password hashes).
- **Limits:** Scratch restore proves the file is valid and complete, not that I could rebuild a lost production cluster. A full disaster test would restore into a new Postgres on a fresh cluster. The backup is still a single copy in one region.
