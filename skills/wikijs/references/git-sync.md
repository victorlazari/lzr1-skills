# Git Storage Synchronization

**Verified against upstream:** 2026-08-07
**Primary Source:** https://docs.requarks.io/storage/git

This guide covers configuring and troubleshooting bidirectional Git storage synchronization in Wiki.js.

## Configuration

1. Navigate to **Administration > Storage** in the Wiki.js interface.
2. Select **Git** as the storage target.
3. Configure the repository URL (SSH preferred for security).
4. Provide the necessary authentication credentials (SSH private key or personal access token).
5. Set the sync interval or configure webhooks for real-time updates.

## Troubleshooting

- **Authentication Failures:** Ensure the SSH key is correctly formatted and has read/write access to the repository. If using a PAT, verify it hasn't expired and has the `repo` scope.
- **Sync Conflicts:** If bidirectional sync is enabled, conflicts may occur if a page is edited simultaneously in Wiki.js and the Git repository. Resolve conflicts manually in the Git repository and force a sync from the Wiki.js interface.
- **Connectivity Issues:** Use the `scripts/validate-git-sync.sh` script to verify basic SSH connectivity to the Git provider.
