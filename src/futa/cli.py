import sys
from futa.ai_runner import process_command

def main():
    if len(sys.argv) < 2:
        print("Usage: futa <command>")
        sys.exit(1)

    command = " ".join(sys.argv[1:])
    response = process_command(command)
    print(response)

