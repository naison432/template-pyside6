import os
import re

ICON_DIR = r"d:/proyectos_python/pyside6.python/assets/icons"
PLACEHOLDER = "#COLOR_PLACEHOLDER"


def replace_colors():
    count = 0
    # Regex to capture fill="#..."
    # We look for fill=" followed by # and 3 to 6 hex chars, then end quote
    fill_pattern = re.compile(r'fill="#[a-fA-F0-9]{3,6}"')

    for filename in os.listdir(ICON_DIR):
        if not filename.lower().endswith(".svg"):
            continue

        filepath = os.path.join(ICON_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if it has a fill color that needs replacing
        # We replace any hex fill with the placeholder
        new_content, num_subs = fill_pattern.subn(f'fill="{PLACEHOLDER}"', content)

        if num_subs > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {filename} ({num_subs} replacements)")
            count += 1
        else:
            print(f"Skipped: {filename} (no match found)")

    print(f"\nTotal files updated: {count}")


if __name__ == "__main__":
    replace_colors()
