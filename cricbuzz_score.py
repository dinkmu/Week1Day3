
"""
Capture a Live Cricket Score with Playwright
Website: https://www.cricbuzz.com/
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pathlib import Path
import argparse


URL = "https://www.cricbuzz.com/"
SCREENSHOT = Path(__file__).resolve().parent / "score.png"


# JavaScript used to discover a visible score element
DISCOVER_SCORE = """
() => {
    const scorePattern = /\\b\\d{1,3}\\s*[-/]\\s*\\d{1,2}\\b/;

    function isVisible(el) {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();

        return style.display !== "none" &&
               style.visibility !== "hidden" &&
               rect.width > 0 &&
               rect.height > 0;
    }

    function getSelector(el) {
        const parts = [];

        while (el && el !== document.body) {
            let part = el.tagName.toLowerCase();

            if (el.id) {
                part += "#" + CSS.escape(el.id);
                parts.unshift(part);
                break;
            }

            const parent = el.parentElement;

            if (parent) {
                const siblings = Array.from(parent.children)
                    .filter(child => child.tagName === el.tagName);

                if (siblings.length > 1) {
                    part += ":nth-of-type(" +
                        (siblings.indexOf(el) + 1) + ")";
                }
            }

            parts.unshift(part);
            el = parent;
        }

        return parts.join(" > ");
    }

    const candidates = Array.from(
        document.querySelectorAll("body *")
    )
    .filter(el => {
        if (!isVisible(el)) return false;

        const text = (el.innerText || "").trim();

        return text.length > 0 &&
               text.length < 150 &&
               scorePattern.test(text);
    });

    // Prefer the smallest visible element containing a score.
    candidates.sort((a, b) =>
        a.innerText.trim().length - b.innerText.trim().length
    );

    if (candidates.length === 0) {
        return null;
    }

    const element = candidates[0];

    return {
        selector: getSelector(element),
        score: element.innerText.trim()
    };
}
"""


def capture_score(headless=False):

    with sync_playwright() as playwright:

        print("Launching Chromium...")

        browser = playwright.chromium.launch(
            headless=headless
        )

        page = browser.new_page(
            viewport={
                "width": 1366,
                "height": 768
            }
        )

        try:

            print("Opening Cricbuzz...")

            page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("Waiting for a visible cricket score...")

            # Wait until a visible score-like element appears.
            page.wait_for_function(
                DISCOVER_SCORE,
                timeout=30000
            )

            # Inspect the actual DOM and obtain its selector.
            result = page.evaluate(DISCOVER_SCORE)

            if not result:
                print("No live cricket score found.")
                return

            score_locator = page.locator(
                result["selector"]
            ).first

            # Wait for the discovered element to be visible.
            score_locator.wait_for(
                state="visible",
                timeout=10000
            )

            score_text = score_locator.inner_text()

            print("\n========== LIVE CRICKET SCORE ==========")
            print(score_text)
            print("=========================================")

        except PlaywrightTimeoutError:

            print("\nNo live score appeared within 30 seconds.")
            print("There may be no live match currently.")

        except Exception as error:

            print("\nAn error occurred:", error)

        finally:

            # Save screenshot even if no live match is found.
            page.screenshot(
                path=str(SCREENSHOT),
                full_page=True
            )

            print("\nScreenshot saved:", SCREENSHOT)

            browser.close()

            print("Browser closed.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser without displaying the window"
    )

    args = parser.parse_args()

    capture_score(headless=args.headless)
