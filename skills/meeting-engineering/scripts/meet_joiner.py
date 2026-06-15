#!/usr/bin/env python3
"""meet_joiner.py — Playwright (Python) template for joining Google Meet.

Launches non-headless Chromium on Xvfb with PulseAudio-backed real audio,
injects saved auth state, grants media permissions via CDP, navigates the
pre-join screen, and waits for admission. UI selectors use role/aria-label
based locators with fallbacks because Google rotates class names.
"""
import asyncio
import os
import re

from playwright.async_api import async_playwright, Page, TimeoutError as PWTimeout

AUTH_STATE = os.environ.get("MEET_AUTH_STATE", "workspace/config/meet-auth-state.json")
DISPLAY = os.environ.get("DISPLAY", ":99")
PULSE_SERVER = os.environ.get("PULSE_SERVER", "unix:/tmp/pulse-socket")
ADMIT_TIMEOUT_S = int(os.environ.get("MEET_ADMIT_TIMEOUT_S", "300"))
BOT_NAME = os.environ.get("MEET_BOT_NAME", "Assistant")

CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--autoplay-policy=no-user-gesture-required",
    "--use-fake-ui-for-media-stream",   # auto-accept mic/cam prompts
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--window-size=1280,720",
    # NOTE: do NOT use --use-fake-device-for-media-stream here;
    # real PulseAudio devices must back getUserMedia for audio I/O.
]


async def click_if_visible(page: Page, locator, timeout=3000) -> bool:
    try:
        await locator.first.click(timeout=timeout)
        return True
    except PWTimeout:
        return False


async def join_meet(meet_url: str) -> tuple:
    """Join a meeting. Returns (playwright, browser, context, page) for the caller to manage."""
    assert re.match(r"^https://meet\.google\.com/[a-z]{3}-[a-z]{4}-[a-z]{3}", meet_url), \
        f"Invalid Meet URL: {meet_url}"

    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,  # real (non-headless) Chromium on Xvfb for full WebRTC media
        args=CHROMIUM_ARGS,
        env={**os.environ, "DISPLAY": DISPLAY, "PULSE_SERVER": PULSE_SERVER},
    )
    context = await browser.new_context(
        storage_state=AUTH_STATE if os.path.exists(AUTH_STATE) else None,
        viewport={"width": 1280, "height": 720},
        permissions=["microphone", "camera"],
    )
    await context.grant_permissions(
        ["microphone", "camera"], origin="https://meet.google.com"
    )
    page = await context.new_page()
    page.on("console", lambda m: print(f"[page:{m.type}] {m.text}"))

    await page.goto(meet_url, wait_until="networkidle")
    await page.wait_for_timeout(2000)  # let the green room settle

    # --- Pre-join screen ---------------------------------------------------
    # Turn OFF camera; keep microphone ON (TTS plays through the virtual mic).
    # Toggle camera off if currently on (aria-label contains "Turn off camera").
    await click_if_visible(page, page.get_by_role("button", name=re.compile("Turn off camera", re.I)))

    # Guest flow: fill name field if present (unauthenticated join).
    name_box = page.get_by_placeholder(re.compile("your name", re.I))
    try:
        await name_box.fill(BOT_NAME, timeout=2000)
    except PWTimeout:
        pass

    # Dismiss any blocking dialogs ("Got it", device popups, etc.).
    await click_if_visible(page, page.get_by_role("button", name=re.compile(r"^(Got it|Dismiss|Continue without)", re.I)))

    # Join: "Join now" (invited/same-domain) or "Ask to join" (waiting room).
    joined = await click_if_visible(page, page.get_by_role("button", name=re.compile(r"^Join now$", re.I)), timeout=5000)
    if not joined:
        asked = await click_if_visible(page, page.get_by_role("button", name=re.compile(r"^Ask to join$", re.I)), timeout=5000)
        if not asked:
            raise RuntimeError("Could not find Join now / Ask to join button")

    # --- Wait for admission --------------------------------------------------
    # In-call marker: the leave-call button exists only after admission.
    try:
        await page.get_by_role("button", name=re.compile("Leave call", re.I)).wait_for(
            state="visible", timeout=ADMIT_TIMEOUT_S * 1000
        )
    except PWTimeout:
        # Check for explicit denial
        body = await page.inner_text("body")
        if re.search(r"(denied|can't join|You can't join)", body, re.I):
            raise RuntimeError("Entry denied by host")
        raise RuntimeError(f"Not admitted within {ADMIT_TIMEOUT_S}s")

    print("[joiner] In the meeting.")
    return pw, browser, context, page


async def participant_count(page: Page) -> int:
    """Read participant count from the People button badge; 0 if unknown."""
    try:
        label = await page.get_by_role("button", name=re.compile(r"People", re.I)).first.get_attribute("aria-label")
        m = re.search(r"(\d+)", label or "")
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


async def leave_meeting(page: Page):
    try:
        await page.get_by_role("button", name=re.compile("Leave call", re.I)).first.click(timeout=5000)
    except Exception:
        pass  # page may already be closed


if __name__ == "__main__":
    async def main():
        url = os.environ["MEETING_URL"]
        pw, browser, context, page = await join_meet(url)
        try:
            # Auto-leave when alone for 60s
            alone_since = None
            while True:
                await asyncio.sleep(10)
                n = await participant_count(page)
                if n <= 1:
                    alone_since = alone_since or asyncio.get_event_loop().time()
                    if asyncio.get_event_loop().time() - alone_since > 60:
                        print("[joiner] Alone in meeting, leaving.")
                        break
                else:
                    alone_since = None
        finally:
            await leave_meeting(page)
            await context.close()
            await browser.close()
            await pw.stop()

    asyncio.run(main())
