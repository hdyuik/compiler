class Epsilon:
    def __str__(self):
        return "ε"
epsilon = Epsilon()
EOF = "@@@"


class StringBuilder:
    def __init__(self, sigma: set):
        self.sigma = sigma

    def not_include(self, removal_cs: set):
        s = set()
        for c in self.sigma:
            if c not in removal_cs:
                s.add(c)
        return s
