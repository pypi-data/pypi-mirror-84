import os
import re
from pathlib import Path


def loadenv(*args):
    for arg in args:
        envfile = Path(arg).resolve()
        if not envfile.exists():
            continue

        with open(envfile, "rt") as fobj:
            for line in fobj:
                line = line.strip()

                if line and not line.startswith("#"):
                    key, value = re.split(r"\s?=\s?", line, 1)

                    quoted = re.match(r'''[^"]*"(.+)"''', value)

                    if quoted:
                        value = str(quoted.groups()[0])
                    elif value in {"true", "on", "yes"}:
                        value = "True"
                    elif value in {"false", "off", "no"}:
                        value = "False"

                    for match_replace in re.findall(r"(\${([\w\d\-_]+)})", value):
                        # Reference variables in values
                        # ej: DB_DEBUG = ${DEBUG}

                        replace, name = match_replace
                        value = value.replace(replace, os.environ.get(name, ""))

                    os.environ[key] = value

