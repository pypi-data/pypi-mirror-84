import shlex


def get(directives, name):
    for d in directives:
        if d.name == name:
            return d


def get_all(directives, name):
    results = []
    for d in directives:
        if d.name == name:
            results.append(d)
    return results


class Directive:
    name = None
    params = None
    children = None

    def __init__(self, name, params, children=None):
        self.name = name
        self.params = params
        self.children = children or []

    def __str__(self):
        return f"{self.name}: {self.params}"

    def get(self, name):
        return get(self.children, name)

    def get_all(self, name):
        return get_all(self.children, name)


class Config:
    directives = None

    def __init__(self, filename):
        self.filename = filename

    def load(self):
        # Let Python raise the exception if there's an issue with filename
        with open(self.filename) as fp:
            directives, closing_brace = self.read_block(fp)
        self.directives = directives

    def read_block(self, fp):
        blocks = []
        closing_brace = False

        for line in fp:
            line = line.strip()
            if line.startswith("#"):
                continue

            words = shlex.split(line)
            if not len(words):
                continue

            if len(words) == 1 and line[-1] == "}":
                closing_brace = True
                break

            if words[-1] == "{" and line[-1] == "{":
                words = words[:-1]

                name = ""
                params = words

                if len(words) > 0:
                    name, params = words[0], words[1:]

                child_block, child_closing_brace = self.read_block(fp)
                if not child_closing_brace:
                    raise ValueError("Unexpected EOF")
                d = Directive(name, params, child_block)
            else:
                d = Directive(words[0], words[1:])

            blocks.append(d)

        return blocks, closing_brace

    def get(self, name):
        return get(self.directives, name)

    def get_all(self, name):
        return get_all(self.directives, name)
