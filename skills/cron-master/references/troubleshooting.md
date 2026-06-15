# Cron Troubleshooting Checklist

If your cron job is not executing as expected, follow this checklist to guarantee a 100% correct resolution.

## 1. The "Silent Failure" Checks

If the job seems to do absolutely nothing:

- [ ] **Newline at EOF:** Does your crontab file end with an empty newline? Cron often ignores the last line if it doesn't end with a Line Feed (LF).
- [ ] **CRLF vs LF:** Did you edit the file on Windows? Ensure the file uses Unix line endings (LF), not Windows (CRLF).
- [ ] **Permissions:** Is the script you are calling executable? Run `chmod +x /path/to/script.sh`.
- [ ] **Absolute Paths:** Cron's `PATH` is minimal (`/usr/bin:/bin`). Are you using absolute paths for *everything*? (e.g., `/usr/local/bin/node` instead of `node`).

## 2. The "It Works Manually but Fails in Cron" Checks

If you can run the script in your terminal, but cron fails:

- [ ] **Environment Variables:** Cron does NOT load your `.bashrc` or `.profile`. If your script needs `DB_HOST`, you must define it at the top of the crontab, or source your profile inside the script:
  ```bash
  * * * * * source $HOME/.bash_profile && /path/to/script.sh
  ```
- [ ] **Working Directory:** Cron runs jobs from the user's home directory. Does your script assume it's running from a specific folder? Use `cd` in the cron command:
  ```bash
  * * * * * cd /opt/myapp && ./script.sh
  ```
- [ ] **TTY Requirements:** Does your script expect user input or a terminal? Commands like `docker exec -it` will fail in cron because there is no TTY. Remove the `-it` flags.

## 3. The "Docker Specific" Checks

If you are running cron inside or against Docker containers:

- [ ] **Did you use traditional `cron` in a container?** Standard cron drops environment variables. Switch to `supercronic` (See Pattern A).
- [ ] **Is the container actually running?** If using the Host-to-Docker pattern (Pattern B), ensure the container hasn't restarted or changed names. Use the `docker-cron-wrapper.sh` script.
- [ ] **Are logs disappearing?** Traditional cron logs to `syslog`. In Docker, `syslog` usually isn't running. Ensure your cron daemon (like `supercronic`) logs to `stdout`/`stderr`.

## 4. How to Debug

If you still can't find the issue, force cron to tell you what's wrong:

1. **Redirect ALL output:**
   ```bash
   * * * * * /path/to/script.sh > /tmp/cron_debug.log 2>&1
   ```
2. **Check System Logs (Local Machine):**
   ```bash
   grep CRON /var/log/syslog
   # or on RedHat/CentOS:
   grep CRON /var/log/cron
   ```
3. **Run the script in a simulated empty environment:**
   ```bash
   env -i /bin/bash -c '/path/to/script.sh'
   ```
   This simulates how cron runs your script. If it fails here, you know it's an environment variable issue.
