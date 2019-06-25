from typing import Set, Any


class RuleItem:
    def __init__(self, dot_pos: int, rule):
        self.dot_pos = dot_pos
        self.rule = rule

    def __str__(self):
        right_hand = [str(symbol) for symbol in self.rule.right_hand]
        right_hand.insert(self.dot_pos, '●')
        return "{0} -> {1}".format(self.rule.left_hand, ' '.join(right_hand))

    def reduce(self):
        if self.dot_pos == len(self.rule.right_hand):
            return True
        else:
            return False

class LookAheadItem:
    def __init__(self, la_symbols: Set[Any]):
        self.symbols = la_symbols

    def __str__(self):
        return "LOOK AHEAD: {0}".format(self.symbols)
