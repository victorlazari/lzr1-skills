# Playwright Automation for Google Meet

This reference details the specifics of automating a headless Chromium browser using Playwright to join and interact with Google Meet.

## Authentication and Session State

Google Meet actively blocks automated access and service accounts. The bot must operate using a real Google Workspace or Gmail account.

1.  **Manual Login**: Perform an initial manual login using the dedicated bot account (e.g., `bot@domain.com`).
2.  **Save State**: Save the authenticated browser state (cookies, local storage) to a file (e.g., `workspace/config/meet-auth-state.json`).
3.  **Inject State**: When launching the headless browser, inject this state using Playwright's `storageState` parameter. This bypasses the login screens and 2FA prompts entirely.

```javascript
const context = await browser.newContext({
  storageState: 'workspace/config/meet-auth-state.json',
});
```

## The Join Flow

The process of joining a Google Meet involves navigating several dynamic screens and popups.

### 1. The Pre-Join Screen (Green Room)

When navigating to a Meet URL, the bot first lands on the pre-join screen.

*   **Mute Media**: Ensure the bot's microphone and camera are turned off before joining to prevent feedback loops and visual clutter. While Chromium flags (`--use-fake-device-for-media-stream`) provide fake streams, it's best practice to click the mute buttons in the UI.
*   **Locate Buttons**: Use Playwright's robust selectors (e.g., `page.getByRole`, `page.getByLabel`) to find the mute buttons and the "Join now" or "Ask to join" button.
*   **Handle "Ask to Join"**: If the bot is not invited to the calendar event, it will see an "Ask to join" button. The bot must click this and then wait to be admitted by a host. Implement a timeout; if not admitted within a specific timeframe, the bot should exit gracefully.

### 2. Handling Popups and Dialogs

Google Meet frequently displays popups (e.g., "Use your microphone", tooltips, audio device notifications).

*   **CDP Permissions**: The most critical step is granting media permissions at the browser level to avoid blocking popups. Use the Chrome DevTools Protocol (CDP) via Playwright to grant permissions for the specific origin.

```javascript
// Grant permissions at the context level
await context.grantPermissions(['microphone', 'camera'], { origin: 'https://meet.google.com' });
```

*   **Dismissing In-UI Popups**: Use Playwright to detect and dismiss any overlay dialogs that might obscure the UI or prevent interaction.

### 3. Enabling Captions (Optional Fallback)

If the primary low-latency STT pipeline (via PulseAudio) fails, scraping the DOM for live captions is a fallback method.

*   Click the "Turn on captions" button (usually `page.getByLabel('Turn on captions')`).
*   Use `page.evaluate()` to inject a `MutationObserver` into the DOM.
*   Watch the specific `div` or `<region>` where Google Meet renders caption text.
*   Extract the speaker name and text, deduplicate the segments, and pass them back to the Node.js context via `page.exposeFunction()`.

*Note: DOM scraping is fragile as Google frequently changes class names and layouts. The PulseAudio + API STT approach is strongly preferred for reliability.*

## Managing the Meeting State

*   **Monitoring Participants**: The bot should monitor the participant list. If all human users leave, the bot should automatically disconnect to save resources.
*   **Exit Phrases**: Implement logic in the STT stream to listen for commands like "Bot, leave the meeting" to trigger a graceful exit.
*   **Graceful Teardown**: When leaving, ensure the Playwright context is closed, the browser is terminated, and the associated PulseAudio streams are cleaned up.

## Anti-Bot Detection

Google Meet employs heuristics to detect and block bots.

*   **Avoid Service Accounts**: As mentioned, use real user accounts.
*   **Human-like Interaction**: Add slight delays (`page.waitForTimeout()`) between actions on the pre-join screen rather than clicking instantly.
*   **Domain Allowlisting**: If operating within a Google Workspace, ensure the bot's account domain is trusted by the host's domain to bypass the waiting room where possible.
