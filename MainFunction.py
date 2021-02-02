import json

# Set Path
path_config = "bin/locales/language.json"


class MainFunction:

    def __init__(self):
        print("Calling parent constructor")

    def __del__(self):
        print('Object was destroyed')

    def getLanuage(self, request):
        try:
            # Get language form cliant
            lang = request.headers["language"]
            if not lang:
                lang = "th"
        except Exception as e:
            lang = "th"
        return lang

    def getMessage(self, lang, input):
        try:
            with open(path_config, "r", encoding="utf8") as conf:
                d = json.loads(conf.read())
                res = d[lang][input]
        except Exception as e:
            res = ""
        return res
