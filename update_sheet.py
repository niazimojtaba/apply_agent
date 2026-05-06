"""
update_sheet.py — log a job application to a Google Sheet.

Setup (one-time):
  1. Create a Google Sheet with these column headers in row 1:
        Company | Applied By | Date | Status | Role | Link | Notes | Match
  2. Create a Google Cloud service account and share the sheet with its email.
  3. Download the service account key as service_account.json (git-ignored).
  4. Copy sheet_config.yaml.example → sheet_config.yaml and fill in your Sheet ID.

Usage:
    python3 update_sheet.py \\
        --company "Acme" \\
        --role "Senior Backend Engineer" \\
        --link "https://jobs.acme.com/..." \\
        --status "Applied" \\
        --match 82
"""
import argparse
import datetime
import sys
from pathlib import Path

try:
    import yaml
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    sys.exit(
        "Missing dependencies. Run:\n"
        "  pip install pyyaml google-auth google-api-python-client"
    )

_CONFIG_PATH      = Path(__file__).parent / "sheet_config.yaml"
_KEY_FILE         = Path(__file__).parent / "service_account.json"
_SCOPES           = ["https://www.googleapis.com/auth/spreadsheets"]

# Column order — must match your sheet's header row exactly.
# Edit here if your sheet uses a different layout.
_COLUMNS = ["Company", "Applied By", "Date", "Status", "Role", "Link", "Notes", "Match"]


def _load_config() -> dict:
    if not _CONFIG_PATH.exists():
        sys.exit(
            f"sheet_config.yaml not found.\n"
            f"Copy sheet_config.yaml.example → sheet_config.yaml and fill in your Sheet ID."
        )
    with open(_CONFIG_PATH) as f:
        return yaml.safe_load(f)


def _get_service():
    if not _KEY_FILE.exists():
        sys.exit(
            "service_account.json not found.\n"
            "Download your Google service account key and place it here."
        )
    creds = service_account.Credentials.from_service_account_file(
        str(_KEY_FILE), scopes=_SCOPES
    )
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def append_entry(company, role, link, status="Applied", notes="", match=""):
    config     = _load_config()
    sheet_id   = config["sheet_id"]
    sheet_name = config.get("sheet_name", "Applications")
    service    = _get_service()

    today     = datetime.date.today().strftime("%-m/%-d/%Y")
    match_str = f"{match}%" if match != "" else ""

    row = [company, "claude", today, status, role, link, notes, match_str]

    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]},
    ).execute()

    print(f"Added: {company} — {role} ({today})" + (f" | Match: {match_str}" if match_str else ""))


def main():
    parser = argparse.ArgumentParser(description="Log a job application to Google Sheets.")
    parser.add_argument("--company", required=True,  help="Company name")
    parser.add_argument("--role",    required=True,  help="Role title")
    parser.add_argument("--link",    default="",     help="Job posting URL")
    parser.add_argument("--status",  default="Applied", help="Application status")
    parser.add_argument("--notes",   default="",     help="Free-text notes")
    parser.add_argument("--match",   default="",     help="JD match score 0–100 (no %% sign)")
    args = parser.parse_args()
    append_entry(args.company, args.role, args.link, args.status, args.notes, args.match)


if __name__ == "__main__":
    main()
