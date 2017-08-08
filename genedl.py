#!/usr/bin/env python3

import os
import subprocess
import sys


def main(argv):
    filename = argv[1]
    output_filename = filename.rpartition(".")[0] + ".edl"
    chapter_data = subprocess.check_output(["/usr/bin/mp4chaps", "-l", filename])
    chapters = []
    has_commercials = False
    # mp4chaps sometimes spits out non-utf8 characters when it encounters an error
    for line in chapter_data.decode("unicode_escape").split("\n"):
        if not "Chapter #" in line:
            continue
        (chapter, start, name) = map(str.strip, line.split(" - "))
        if len(chapters) > 0:
            chapters[-1]["end"] = start
        commercial = name == "\"Advertisement\""
        has_commercials = has_commercials or commercial
        chapters.append({"chapter": chapter, "start": start, "name": name, "commercial": commercial})
    if has_commercials and not os.path.exists(output_filename):
        print("writing to: " + output_filename)
        with open(output_filename, "w") as out:
            for chapter in chapters:
                if chapter["commercial"]:
                    line = chapter["start"] + "\t" + chapter["end"] + "\t" + "3\n"
                    out.write(line)
                    print(line, end="")
if __name__ == "__main__":
    main(sys.argv)