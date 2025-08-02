import os
from pathlib import Path
import re

CHAPTER_DIR = "./manuscript/chapters"
OUTPUT_FILE = "./output/holiday-in-ohio.html"
STYLESHEET_PATH = "../../config/comic.css"
TITLE = "Holiday in Ohio"
LANG = "de"

def combine_html_chapters(chapter_dir, output_file, title, lang, stylesheet_path):
    def chapter_sort_key(path):
        match = re.match(r"(\d+)", path.stem)
        return int(match.group(1)) if match else 0

    chapter_files = sorted(Path(chapter_dir).glob("*.html"), key=chapter_sort_key)
    if not chapter_files:
        print(f"❌ Keine .html-Dateien in {chapter_dir} gefunden.")
        return

    os.makedirs(Path(output_file).parent, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n')
        outfile.write('  <meta charset="UTF-8">\n')
        outfile.write(f'  <title>{title}</title>\n')
        outfile.write(f'  <link rel="stylesheet" href="{stylesheet_path}">\n')
        outfile.write('</head>\n<body>\n')

        for chapter_file in chapter_files:
            with open(chapter_file, "r", encoding="utf-8") as infile:
                inside_body = False
                for line in infile:
                    if "<body" in line:
                        inside_body = True
                        continue
                    if inside_body:
                        if "</body>" in line:
                            break
                        outfile.write(line)

        outfile.write('</body>\n</html>\n')
    print(f"✅ HTML kombiniert in: {output_file}")

def main():
    combine_html_chapters(
        chapter_dir=CHAPTER_DIR,
        output_file=OUTPUT_FILE,
        title=TITLE,
        lang=LANG,
        stylesheet_path=STYLESHEET_PATH
    )


if __name__ == "__main__":
    main()