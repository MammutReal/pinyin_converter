# This Python file uses the following encoding: utf-8

import json
import re

class PinyinConverter:
    POPULAR = "h1"
    ACADEMIC = "h2"
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"

    def __init__(self, method=POPULAR, filename="syllables.json"):
        self._map = {}
        self._syllables = ""

        self.setup(method, filename)

    def setup(self, method=POPULAR, filename="syllables.json"):
        file = open(filename, encoding="utf-8")
        data = json.load(file)

        self._map = {}
        syllables = []
        for s in data:
            self._map[s["p"]] = s[method]
            syllables.append(s["p"])

        # ! the sorting is only needed if the json file was edited and the order of syllables changed
        # ! it's important that the longer syllables come first

        # desc_data = sorted(data, key=lambda item: item["length"], reverse=True)
        # syllables = []
        # for s in desc_data:
        #     syllables.append(s["p"])

        self._syllables = "|".join(syllables) + "|[a-z]"

    def convert(self, name, hyphen_options={"use_hyphen": True, "one_word": True}):
        words = name.split(" ")

        new_words = []
        for i in range(0, len(words)):
            word = words[i]
            word = word.lower()

            if "'" in word:
                result = word.split("'")
            elif "-" in word:
                result = word.split("-")
            else:
                word = re.sub(r'\W+', '', word)
                result = re.findall(self._syllables, word, re.IGNORECASE)

            res = ""
            # result[0] = result[0].title()
            for r in result:
                r = re.sub(r'\W+', '', r)
                if r in self._map.keys():
                    if type(self._map[r]) == list:
                        res += self._map[r][0]
                    else:
                        res += self._map[r]
                else:
                    res += r

                if hyphen_options["use_hyphen"] and i == len(words) - 1:
                    if not hyphen_options["one_word"] and len(words) > 1 or hyphen_options["one_word"]:
                        res += "-"

            if len(res) > 0 and res[-1] == "-":
                res = res[:-1]
            res = res.capitalize()
            new_words.append(res)

        new_name = " ".join(new_words).strip()

        return new_name

if __name__ == "__main__":
    import sys
    import subprocess
    import os
    import platform

    # read the config file
    config = json.load(open("config.json"))

    # read arguments and override config data
    save = False
    argv = sys.argv
    valid_methods = [v["code"] for v in config["valid_methods"]] # we create a list from the valid methods list of dictionaries
    for i in range(1, len(argv)):
        if argv[i] in valid_methods:
            config["method"] = argv[i]

        elif argv[i] == "copy":
            config["copy"] = True
        elif argv[i] == "nocopy":
            config["copy"] = False

        elif ".json" in argv[i]:
            config["filename"] = argv[i]

        elif argv[i] == "hyphen":
            config["hyphen_options"]["use_hyphen"] = True
        elif argv[i] == "nohyphen":
            config["hyphen_options"]["use_hyphen"] = False
        elif argv[i] == "oneword":
            config["hyphen_options"]["one_word"] = True # we use hyphen even if the name is only one word
        elif argv[i] == "lastword":
            config["hyphen_options"]["one_word"] = False # we use hyphen only at the last word

        elif argv[i] == "save":
            save = True

    # we write the modified config dict to the config file if user added the "save" command line option
    if save:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    # init the converter
    converter = PinyinConverter(config["method"], config["filename"])

    while True:
        # we ask for a name
        try:
            name = input("Enter a name (to quit press Ctrl+Z + Enter or Ctrl+C on Windows or Ctrl+D on Linux/MacOSX): ")
        except EOFError:   # Ctrl+Z + Enter on Windows, Ctrl+D on Linux/MacOSX
            break
        except KeyboardInterrupt:  # Ctrl + C - will exit program immediately if not caught
            break

        # convert it
        name = converter.convert(name, config["hyphen_options"])

        # copy the converted name to the clipboard if it's enabled
        if config["copy"]:
            # send the converted name to the clipboard
            if platform.system() == "Windows":
                os.system('echo ' + name + '| clip')
            elif platform.system() == "Linux":
                p = subprocess.Popen(['xsel','-pi'], stdin=PIPE)
                p.communicate(input=name)
            elif platform.system() == "Darwin":
                subprocess.run("pbcopy", text=True, input=name)

        # print the converted name
        print (name)
