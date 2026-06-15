# Cron Best Practices: Local Machine

When running cron jobs directly on a Linux host (local machine), follow these best practices to ensure 100% reliability and correct execution.

## 1. Environment Variables

Cron runs with a highly restricted environment. It does **not** load your `.bashrc`, `.bash_profile`, or system-wide environment variables by default.

**Best Practice:**
- Define essential environment variables at the top of your crontab file.
- ALWAYS use absolute paths for commands (e.g., `/usr/bin/python3` instead of `python3`).
- If your script relies on specific environment variables, source them inside the script or define them in the crontab.

```bash
# Example crontab environment setup
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=admin@example.com
MY_APP_ENV=production
```

## 2. Output and Error Handling

By default, cron emails the output of jobs to the user executing them. If no mail server is configured, this output is often lost or ends up in dead local mailboxes.

**Best Practice:**
- NEVER discard output blindly (e.g., `> /dev/null 2>&1`) unless you are absolutely sure you don't need it.
- Redirect standard output (`stdout`) and standard error (`stderr`) to a specific log file.

```bash
# Good: Redirects both stdout and stderr to a log file
0 * * * * /opt/myapp/script.sh >> /var/log/myapp/cron.log 2>&1

# Better: Use logger to send output to syslog
0 * * * * /opt/myapp/script.sh 2>&1 | /usr/bin/logger -t myapp_cron
```

## 3. Principle of Least Privilege

Running all cron jobs as `root` is a security risk.

**Best Practice:**
- Run jobs as a dedicated user with only the permissions required for that specific task.
- Edit the specific user's crontab using `crontab -e -u username` or place a file in `/etc/cron.d/` specifying the user.

```bash
# /etc/cron.d/myapp format (includes the user field)
0 * * * * myappuser /opt/myapp/script.sh >> /var/log/myapp/cron.log 2>&1
```

## 4. Preventing Job Overlaps

If a cron job takes longer to execute than its scheduled interval, multiple instances will run simultaneously, potentially causing resource exhaustion or data corruption.

**Best Practice:**
- Use a locking mechanism like `flock` to ensure only one instance runs at a time.

```bash
# Uses flock to prevent overlapping executions
*/5 * * * * /usr/bin/flock -n /tmp/myjob.lock /opt/myapp/script.sh >> /var/log/myapp/cron.log 2>&1
```

## 5. Script Permissions and Format

Cron will fail silently if the script it tries to execute is not formatted correctly.

**Best Practice:**
- Ensure the script is executable (`chmod +x /opt/myapp/script.sh`).
- Ensure the script has a valid shebang (e.g., `#!/bin/bash`).
- Ensure the crontab file ends with an empty newline character (LF), especially when placing files in `/etc/cron.d/`.
