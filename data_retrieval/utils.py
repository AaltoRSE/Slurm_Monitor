import subprocess


def run_command(command: str) -> str:
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout  # Return the standard output
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        return None
