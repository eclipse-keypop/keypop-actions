import subprocess

tags = [
    "build-and-test-v1",
    "publish-release-v1",
    "publish-snapshot-v1",
    "dash-licenses-v1",
    "update-documentation-v1"
]

def run(cmd):
    """Run a shell command and return its output. Raise on error."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        raise Exception(f"Command failed: {' '.join(cmd)}")
    return result.stdout.strip()

def tag_exists(tag):
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}"],
        capture_output=True
    )
    return result.returncode == 0

def main():
    head = run(["git", "rev-parse", "HEAD"])
    print(f"HEAD commit: {head}")

    for tag in tags:
        if tag_exists(tag):
            run(["git", "tag", "-d", tag])
        subprocess.run(["git", "push", "origin", f":refs/tags/{tag}"])
        run(["git", "tag", tag, head])
        run(["git", "push", "origin", tag])

    print("All tags have been aligned to HEAD and pushed.")

if __name__ == "__main__":
    main()
