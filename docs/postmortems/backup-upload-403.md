## Incident: backup upload denied (403), three times

- **What happened:** The backup CronJob's dump stage worked, but the upload failed with three successive 403s: objects.get, then (after a binding retry) objects.get again, then objects.list.
- **Root cause:** I granted roles/storage.objectCreator for least privilege, but `gcloud storage cp` checks for an existing object and lists the destination before uploading, so it needs objects.get and objects.list as well as objects.create.
- **Detection:** Each error named the exact missing permission and showed the pod was authenticated as the intended service account, so Workload Identity itself was working from the first run.
- **Fix:** A custom role with objects.create, objects.get and objects.list. Overwrite and delete still need objects.delete, so the job can add backups but not replace or remove them. It can read backup contents, which is a weaker guarantee than I first described.
- **Mistakes in my process:** The first attempt to bind the new custom role failed right after creating it ("does not exist in the resource's hierarchy"), and I re-ran the job without checking the binding, so the second run failed identically. Verify a permission change before testing with it, and don't guess permissions one at a time.
- **Known gap:** A stricter design would upload with a single API call needing only objects.create. The bucket, service account and custom role were created with gcloud and are not in Terraform.
