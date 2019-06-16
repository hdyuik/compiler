from collections.abc import MutableMapping


class SymbolTranslation(MutableMapping):
    def __init__(self):
        self.sigma = set()
        self.translation_table = {}
        self._values = set()

    def concat(self, translation: "SymbolTranslation"):
        new_translation = SymbolTranslation()
        for key, value in self.items():
            true_value = translation[value]
            new_translation[key] = true_value
        return new_translation

    def clear(self):
        self.translation_table.clear()

    def __len__(self):
        return len(self.translation_table)

    def __getitem__(self, item):
        return self.translation_table.__getitem__(item)

    def __delitem__(self, key):
        self.translation_table.__delitem__(key)

    def __setitem__(self, key, value):
        self.translation_table.__setitem__(key, value)
        if value not in self._values:
            self._values.add(value)
            self.sigma.add(key)

    def __iter__(self):
        return self.translation_table.__iter__()
