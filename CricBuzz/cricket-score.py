from datetime import datetime
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


LIVE_MATCHES_URL = "https://www.cricbuzz.com/cricket-match/live-scores"
MATCH_SELECTOR = 'main a[href^="/live-cricket-scores/"]:has(.text-cbLive)'
SCORE_SELECTOR = "main div.flex.flex-col:has(> .text-cbTxtLive):visible"


def get_live_matches(page):
    response = page.goto(
        LIVE_MATCHES_URL,
        wait_until="domcontentloaded",
        timeout=30000
    )
    if response is not None and response.status >= 400:
        raise RuntimeError(f"Could not access live matches (HTTP {response.status}).")

    page.locator("main").wait_for(state="visible", timeout=10000)
    matches = []
    seen_urls = set()
    for card in page.locator(MATCH_SELECTOR).all():
        href = card.get_attribute("href")
        if not href:
            continue
        match_url = urljoin(LIVE_MATCHES_URL, href)
        if match_url in seen_urls:
            continue
        seen_urls.add(match_url)
        lines = [
            line.strip() for line in card.inner_text().splitlines() if line.strip()
        ]
        matches.append({
            "url": match_url,
            "description": " | ".join(lines),
            "is_india": any(line.upper() in {"IND", "INDIA"} for line in lines)
        })
    return matches


def get_cricket_score():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page(
            viewport={"width": 1440, "height": 900}
        )

        try:
            print("Finding live matches on Cricbuzz...")
            matches = get_live_matches(page)
            if not matches:
                print("No live matches are available right now.")
                return

            india_match = next((match for match in matches if match["is_india"]), None)
            if india_match is not None:
                print(f"\nIndia live match found: {india_match['description']}")
                match_url = india_match["url"]
            else:
                print("\nNo India live match found. Choose another live match:")
                for match_number, match in enumerate(matches, start=1):
                    print(f"{match_number}. {match['description']}")

                while True:
                    choice = input("\nChoose a match number (or q to quit): ").strip()
                    if choice.lower() == "q":
                        return
                    try:
                        match_number = int(choice)
                    except ValueError:
                        print("Please enter a number from the list.")
                        continue
                    if 1 <= match_number <= len(matches):
                        match_url = matches[match_number - 1]["url"]
                        break
                    print(f"Please choose a number between 1 and {len(matches)}.")

            response = page.goto(
                match_url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            if response is not None and response.status >= 400:
                print(f"\nCould not access the match page (HTTP {response.status}).")
                return

            print("Waiting for live score...")

            score_element = page.locator(SCORE_SELECTOR).first

            score_element.wait_for(
                state="visible",
                timeout=10000
            )

            score_lines = []
            team_rows = score_element.locator(":scope > div:first-child > div")
            for team_row in team_rows.all():
                fields = team_row.locator(":scope > div > div")
                team = fields.nth(0).inner_text().strip()
                score = "".join(fields.nth(1).inner_text().split())
                score_lines.extend([team, score])

            status = score_element.locator(":scope > .text-cbTxtLive").inner_text().strip()
            score_lines.append(status)

            print("\nLatest Cricket Score:")
            print("\n".join(score_lines))

        except PlaywrightTimeoutError:
            print("\nCould not load the score for the selected match.")

        except (EOFError, KeyboardInterrupt):
            print("\nMatch selection cancelled.")

        except Exception as error:
            print(f"\nError: {error}")

        finally:
            screenshot_path = f"score_{datetime.now():%Y-%m-%d_%H-%M-%S_%f}.png"
            try:
                page.screenshot(
                    path=screenshot_path,
                    full_page=True
                )
                print(f"\nScreenshot saved as {screenshot_path}")
            finally:
                browser.close()


if __name__ == "__main__":
    get_cricket_score()
