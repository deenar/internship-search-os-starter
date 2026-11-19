#!/usr/bin/env python3
"""Write path for data/applications.json. Subcommands: add, update, find.

Never guesses a required field — the caller (the application-tracker skill) must gather
company/role/source/url from the user before invoking `add`.

Every skill that writes into `applications/<company>_<role>/` (company-research,
application-strategy, cv-tailor, cover-letter, interview-prep, networking-intelligence) must
run `find --company "<company>"` first and confirm a matching entry exists before producing
any document — see .claude/CLAUDE.md's Ground rules for skills.
"""
import argparse
import json
import sys
from datetime import date

VALID_STATUSES = [
    "targeted",
    "drafting",
    "submitted",
    "online_test",
    "interview",
    "assessment_centre",
    "offer",
    "rejected",
    "withdrawn",
]

VALID_SOURCES = ["trackr", "linkedin", "company_site", "other"]


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def next_id(applications):
    if not applications:
        return "APP-0001"
    nums = [int(a["id"].split("-")[1]) for a in applications if a.get("id", "").startswith("APP-")]
    return f"APP-{(max(nums) + 1):04d}" if nums else "APP-0001"


def cmd_add(args):
    data = load(args.applications)
    apps = data["applications"]

    if args.source not in VALID_SOURCES:
        sys.exit(f"error: --source must be one of {VALID_SOURCES}, got {args.source!r}")

    dup = [a for a in apps if a["company"].lower() == args.company.lower() and a["role"].lower() == args.role.lower()]
    if dup:
        sys.exit(
            f"error: an application for {args.company!r} / {args.role!r} already exists as "
            f"{dup[0]['id']} (status={dup[0]['status']}) — use `update` instead of adding a duplicate."
        )

    entry = {
        "id": next_id(apps),
        "company": args.company,
        "role": args.role,
        "source": args.source,
        "url": args.url,
        "location": args.location,
        "date_found": args.date_found or date.today().isoformat(),
        "deadline": args.deadline,
        "status": "targeted",
        "date_submitted": None,
        "cv_path": None,
        "cover_letter_path": None,
        "followup_due": None,
        "followup_sent_at": None,
        "notes": args.notes or "",
        "status_history": [{"status": "targeted", "date": args.date_found or date.today().isoformat()}],
    }
    apps.append(entry)
    data["as_of"] = date.today().isoformat()
    save(args.applications, data)
    print(f"Added {entry['id']}: {entry['company']} — {entry['role']} (source={entry['source']}, status=targeted)")


def cmd_update(args):
    data = load(args.applications)
    apps = data["applications"]
    match = [a for a in apps if a["id"] == args.id]
    if not match:
        sys.exit(f"error: no application with id {args.id!r} in {args.applications}")
    entry = match[0]

    changed = []

    if args.status:
        if args.status not in VALID_STATUSES:
            sys.exit(f"error: --status must be one of {VALID_STATUSES}, got {args.status!r}")
        entry["status"] = args.status
        entry.setdefault("status_history", []).append(
            {"status": args.status, "date": args.date or date.today().isoformat()}
        )
        changed.append(f"status -> {args.status}")
        if args.status == "submitted" and not entry.get("date_submitted"):
            entry["date_submitted"] = args.date or date.today().isoformat()
            changed.append(f"date_submitted -> {entry['date_submitted']}")

    if args.role:
        entry["role"] = args.role
        changed.append(f"role -> {args.role}")
    if args.location:
        entry["location"] = args.location
        changed.append(f"location -> {args.location}")
    if args.deadline:
        entry["deadline"] = args.deadline
        changed.append(f"deadline -> {args.deadline}")
    if args.cv_path:
        entry["cv_path"] = args.cv_path
        changed.append(f"cv_path -> {args.cv_path}")
    if args.cover_letter_path:
        entry["cover_letter_path"] = args.cover_letter_path
        changed.append(f"cover_letter_path -> {args.cover_letter_path}")
    if args.followup_due:
        entry["followup_due"] = args.followup_due
        changed.append(f"followup_due -> {args.followup_due}")
    if args.followup_sent_at:
        entry["followup_sent_at"] = args.followup_sent_at
        changed.append(f"followup_sent_at -> {args.followup_sent_at}")
    if args.notes_append:
        sep = "\n" if entry.get("notes") else ""
        entry["notes"] = f"{entry.get('notes', '')}{sep}[{date.today().isoformat()}] {args.notes_append}"
        changed.append("notes appended")

    if not changed:
        sys.exit("error: no fields supplied to update")

    data["as_of"] = date.today().isoformat()
    save(args.applications, data)
    print(f"Updated {entry['id']} ({entry['company']} — {entry['role']}): " + "; ".join(changed))


def cmd_find(args):
    data = load(args.applications)
    apps = data["applications"]
    company_q = args.company.lower()
    matches = [
        a for a in apps
        if company_q in a["company"].lower() or a["company"].lower() in company_q
    ]
    if args.role:
        role_q = args.role.lower()
        narrowed = [a for a in matches if role_q in a["role"].lower() or a["role"].lower() in role_q]
        if narrowed:
            matches = narrowed

    if not matches:
        detail = f"company={args.company!r}" + (f" role={args.role!r}" if args.role else "")
        sys.exit(f"error: no application found matching {detail} — run `add` to create one first.")

    for a in matches:
        print(
            f"{a['id']}: {a['company']} — {a['role']} (status={a['status']}, "
            f"cv={'yes' if a['cv_path'] else 'no'}, cover_letter={'yes' if a['cover_letter_path'] else 'no'})"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--applications", required=True, help="path to data/applications.json")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--company", required=True)
    p_add.add_argument("--role", required=True)
    p_add.add_argument("--source", required=True, help=f"one of {VALID_SOURCES}")
    p_add.add_argument("--url", required=True)
    p_add.add_argument("--location", default=None)
    p_add.add_argument("--date-found", default=None, help="YYYY-MM-DD, defaults to today")
    p_add.add_argument("--deadline", default=None, help="YYYY-MM-DD")
    p_add.add_argument("--notes", default=None)
    p_add.set_defaults(func=cmd_add)

    p_upd = sub.add_parser("update")
    p_upd.add_argument("--id", required=True)
    p_upd.add_argument("--status", default=None, help=f"one of {VALID_STATUSES}")
    p_upd.add_argument("--date", default=None, help="YYYY-MM-DD for this status change, defaults to today")
    p_upd.add_argument("--deadline", default=None)
    p_upd.add_argument("--cv-path", default=None)
    p_upd.add_argument("--cover-letter-path", default=None)
    p_upd.add_argument("--followup-due", default=None)
    p_upd.add_argument("--followup-sent-at", default=None)
    p_upd.add_argument("--role", default=None, help="correct a mis-recorded role title")
    p_upd.add_argument("--location", default=None, help="correct or backfill the location")
    p_upd.add_argument("--notes-append", default=None)
    p_upd.set_defaults(func=cmd_update)

    p_find = sub.add_parser("find")
    p_find.add_argument("--company", required=True)
    p_find.add_argument("--role", default=None)
    p_find.set_defaults(func=cmd_find)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
