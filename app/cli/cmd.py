#!/usr/bin/env python3
"""
CLI for DevSaver.
"""

import argparse
from app.crud.user_crud import create_user, get_user_by_username
from app.crud.resource_crud import (
    create_resource,
    get_resources_by_user,
    search_resources,
    mark_resource_as_read,
    toggle_star_resource
)


def main():
    parser = argparse.ArgumentParser(
        description="DevSaver CLI - Manage users and developer resources."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --------------------
    # USER COMMANDS
    # --------------------
    user_parser = subparsers.add_parser("create-user", help="Create a new user")
    user_parser.add_argument("--username", required=True, help="Username of the user")
    user_parser.add_argument("--email", required=True, help="Email of the user")
    user_parser.add_argument("--password", required=True, help="Password (plain text for now)")
    user_parser.add_argument("--fullname", required=False, help="Full name of the user")

    get_user_parser = subparsers.add_parser("get-user", help="Get user details by username")
    get_user_parser.add_argument("--username", required=True, help="Username of the user")  
    
    # --------------------
    # RESOURCE COMMANDS
    # --------------------
    add_res_parser = subparsers.add_parser("add-resource", help="Add a new resource")
    add_res_parser.add_argument("--title", required=True, help="Title of the resource")
    add_res_parser.add_argument("--desc", required=True, help="Description")
    add_res_parser.add_argument("--tags", required=False, default="", help="Comma-separated tags")
    add_res_parser.add_argument("--type", required=True, help="Type of resource (e.g., article, video)")
    add_res_parser.add_argument("--source", required=True, help="Source/URL")
    add_res_parser.add_argument("--url", required=False, help="Date created (string for now)")
    add_res_parser.add_argument("--user-id", required=True, type=int, help="User ID")

    list_res_parser = subparsers.add_parser("list-resources", help="List resources for a user")
    list_res_parser.add_argument("--user-id", required=True, type=int, help="User ID")

    search_parser = subparsers.add_parser("search", help="Search resources by query")
    search_parser.add_argument("--user-id", required=True, type=int, help="User ID")
    search_parser.add_argument("--query", required=True, help="Search term")

    mark_parser = subparsers.add_parser("mark-read", help="Mark a resource as read")
    mark_parser.add_argument("--resource-id", required=True, type=int)

    star_parser = subparsers.add_parser("toggle-star", help="Toggle starred status of a resource")
    star_parser.add_argument("--resource-id", required=True, type=int)

    # --------------------
    # PARSE + EXECUTE
    # --------------------
    args = parser.parse_args()

    if args.command == "create-user":
        user = create_user(args.username, args.email, args.password, args.fullname)
        print(f"✅ User created: {user}")

    elif args.command == "get-user":
        user = get_user_by_username(args.username)
        if user:
            print(user)
        else:
            print("❌ User not found.")

    elif args.command == "add-resource":
        res = create_resource(
            title=args.title,
            description=args.desc,
            tags=args.tags,
            type=args.type,
            source=args.source,
            url=args.url,
            user_id=args.user_id
        )
        print(f"✅ Resource added: {res}")

    elif args.command == "list-resources":
        resources = get_resources_by_user(args.user_id)
        for r in resources:
            print(r)

    elif args.command == "search":
        resources = search_resources(args.user_id, args.query)
        for r in resources:
            print(r)

    elif args.command == "mark-read":
        res = mark_resource_as_read(args.resource_id)
        print(f"✅ Marked as read: {res}")

    elif args.command == "toggle-star":
        res = toggle_star_resource(args.resource_id)
        print(f"⭐ Star toggled: {res}")


if __name__ == "__main__":
    main()