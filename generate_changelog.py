import subprocess
from datetime import datetime

def get_git_log():
    result = subprocess.run(
        ["git", "log", "--pretty=format:%s"],
        capture_output=True,
        text=True
    )
    return result.stdout.split("\n")

def categorize(commits):
    categories = {
        "Features": [],
        "Fixes": [],
        "Performance": [],
        "Refactoring": [],
        "Documentation": [],
        "Other": []
    }

    for commit in commits:
        if commit.startswith("feat:"):
            categories["Features"].append(commit[5:].strip())
        elif commit.startswith("fix:"):
            categories["Fixes"].append(commit[4:].strip())
        elif commit.startswith("perf:"):
            categories["Performance"].append(commit[5:].strip())
        elif commit.startswith("refactor:"):
            categories["Refactoring"].append(commit[9:].strip())
        elif commit.startswith("docs:"):
            categories["Documentation"].append(commit[5:].strip())
        else:
            categories["Other"].append(commit)

    return categories

def write_changelog(categories):
    with open("CHANGELOG.md", "w", encoding="utf-8") as f:
        f.write("# CHANGELOG\n\n")
        f.write(f"Last updated: {datetime.now()}\n\n")

        for section, items in categories.items():
            if items:
                f.write(f"## {section}\n")
                for item in items:
                    f.write(f"- {item}\n")
                f.write("\n")

if __name__ == "__main__":
    commits = get_git_log()
    categorized = categorize(commits)
    write_changelog(categorized)
    print("CHANGELOG.md updated.")
