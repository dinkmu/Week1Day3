# CricBuzz Live Score Viewer

A Python command-line program that discovers live matches on Cricbuzz,
automatically displays a live India match when available, and otherwise lets you
choose another match. It also saves a timestamped screenshot.

The application is in [cricket-score.py](cricket-score.py). Dependencies are
listed in [requirements.txt](requirements.txt).

## Features

- Discover live matches without entering a match URL.
- Automatically select the first live match with an exact `India` or `IND` team
  name. India A, India U19, and India Women do not trigger automatic selection.
- Offer a numbered list of other live matches if no India match is found.
- Show match details, available scores, and status in the selection menu.
- Include ongoing matches at innings breaks or stumps, as marked by Cricbuzz.
- Exclude completed and upcoming matches and remove duplicate match links.
- Validate your selection and allow `q` to quit.
- Display team names, scores, and match status on separate lines.
- Save a full-page screenshot with local date and time in its filename.

## Setup

You need Python 3, an internet connection, and a desktop environment because the
script opens a visible Chromium browser.

Run these commands from this `CricBuzz` folder. To use the existing virtual
environment in the parent project folder:

```bash
source ../venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

For a fresh checkout without that environment, create a local one instead:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Installing the Python package alone does not install Chromium; the Playwright
browser installation command is also required. `datetime` and `urllib.parse`
are part of Python's standard library and need no separate installation.

## Run

```bash
python cricket-score.py
```

1. Wait for the browser to load Cricbuzz's live-match listing.
2. If a live India match is available, its score is displayed automatically.
3. Otherwise, choose a match number from the terminal menu, or enter `q` to quit.
4. View the score in the terminal and the screenshot filename printed afterward.

The program reads one selected match and exits; it does not continuously refresh
the score. Run it again to get a new reading or choose another match.

## Example Output

Illustrative score output; actual teams, scores, and status come from the selected
match and may change:

```text
Latest Cricket Score:
NZ
134(41)
IND
16-1(3.1)
India need 119 runs - 47 overs game
```

## Screenshots

Screenshots are saved in the directory from which you run the command, with names
such as:

```text
score_2026-11-07_14-30-05_123456.png
```

The filename contains the local date, hour, minute, second, and microseconds to
avoid overwriting previous captures. The script also attempts a screenshot when
you quit or when loading fails, so an image may show the listing or an error page
rather than a match score.

## Troubleshooting

- **No module named playwright:** Activate your virtual environment and run
  `python -m pip install -r requirements.txt`.
- **Browser executable missing:** Run `python -m playwright install chromium`.
- **HTTP 403 / Access Denied:** Cricbuzz may block automated browser access. The
  script reports the failure; it does not bypass access restrictions.
- **No live matches:** No active match cards were found on the current listing.
- **Score loading timeout:** The connection may be slow, the match may have
  finished, or Cricbuzz may have changed its page structure. The selectors in
  [cricket-score.py](cricket-score.py) depend on that structure.

This is an unofficial educational project and is not affiliated with Cricbuzz.
Use it in accordance with the website's terms and access restrictions.