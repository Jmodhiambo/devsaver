#!/usr/bin/env python3
"""
DevSaver unified entrypoint.
Usage:
  python run.py api            # Run the FastAPI app
  python run.py cli <command>  # Run a CLI command
"""

import sys
# import uvicorn
from app.cli.command import main as cli_main

"""def run_api() -> None:
    ""Run FastAPI server.""
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=True)
"""

def run_cli() -> None:
    """Run CLI commands."""
    # Drop "cli" from sys.argv so argparse in command.py works
    sys.argv.pop(1)
    cli_main()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python devsaver.py [api|cli] ...")
        sys.exit(1)

    # if sys.argv[1] == "api":
    #     run_api()
    elif sys.argv[1] == "cli":
        run_cli()
    else:
        print(f"❌ Unknown command: {sys.argv[1]}")
        print("Usage: python devsaver.py [api|cli] ...")