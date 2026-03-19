#!/usr/bin/env python3
"""Generate SQL to change an admin password from the command line."""

import argparse
import getpass

import bcrypt

DEFAULT_USERNAME = "admin"


def sql_quote(value: str) -> str:
    """Quote a string for safe inclusion in a simple SQL literal."""
    return value.replace("'", "''")


def build_password_update_sql(username: str, new_password: str) -> str:
    """Build SQL for updating an admin password hash."""
    if not new_password:
        raise ValueError("New password must not be empty")

    password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    return (
        "BEGIN;\n"
        "UPDATE admin\n"
        f"SET password_hash = '{sql_quote(password_hash)}'\n"
        f"WHERE username = '{sql_quote(username)}';\n"
        "COMMIT;"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Change Poetry Site admin password")
    parser.add_argument("password", nargs="?", help="New password. If omitted, you'll be prompted securely.")
    parser.add_argument("--username", default=DEFAULT_USERNAME, help=f"Admin username (default: {DEFAULT_USERNAME})")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    password = args.password

    if password is None:
        password = getpass.getpass(f"New password for {args.username}: ")
        confirmation = getpass.getpass("Repeat new password: ")
        if password != confirmation:
            raise SystemExit("Passwords do not match")

    print(build_password_update_sql(args.username, password))


if __name__ == "__main__":
    main()
