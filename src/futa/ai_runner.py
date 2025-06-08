import subprocess
import random
import os

def extract_command(text):
    lines = text.strip().splitlines()

    commands = [
        line.strip()
        for line in lines
        if line.strip() and
           not any(kw in line.lower() for kw in ['thinking', 'okay', 'user', 'let me', 'explain', 'done']) and
           not line.startswith("#") and
           not line.startswith("```")
    ]

    return "\n".join(commands)

def process_command(prompt: str):
    try:
        # Model Pull, NEED TO ADD MORE VERSIONS LATER
        subprocess.run(["sudo", "ollama", "pull", "qwen3:0.6b"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        system_prompt = "Answering ONLY in UNIX commands. Do not explain, no output, no markdown, no formatting, no commentary. One command per line. If the question is unrelated to UNIX commands or answering in a UNIX command is impossible, the respond with a one line denial in an obnoxious way."
        full_prompt = f"{system_prompt}\n{prompt}"

        # Run LLM
        result = subprocess.run(
            ["ollama", "run", "qwen3:0.6b"],
            input=full_prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            return f"LLM Error: {result.stderr.decode()}"

        # Extract raw command output
        output = result.stdout.decode().strip()
        commands = extract_command(output)

        # If extraction yields nothing, assume it’s a denial or joke, and print raw model output
        if not commands:
            return output

        # Command Execution
        exec_result = subprocess.run(
            commands,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stderr_text = exec_result.stderr.decode()
        stdout_text = exec_result.stdout.decode()

        # Check for "command not found" error in stderr
        if "command not found" in stderr_text.lower():
            # Get absolute path to denials.txt relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            denials_path = os.path.join(script_dir, "denials.txt")
            
            # Read denial lines from denials.txt
            try:
                with open(denials_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    denials = [line.strip() for line in content.splitlines() if line.strip()]
                if denials:
                    return "Command couldn't be generated. " + random.choice(denials)
                else:
                    return "Command could not be generated and the denial file is empty!"
            except FileNotFoundError:
                return "Command could not be found and the denial file missing!"


        # Otherwise, return combined stdout and stderr
        return stdout_text + stderr_text

    except Exception as e:
        return f"Exception: {str(e)}"
