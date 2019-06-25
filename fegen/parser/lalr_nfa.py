from fegen.common import NFA, NFAState, NFAItems


class LALRNFAStateItems(NFAItems):
    def __init__(self):
        self.rule = None
        self.look_ahead = None


class LALRNFAState(NFAState):
    count = 0
    ItemStorageClass = LALRNFAStateItems


class LALRNFA(NFA):
    StateClass = LALRNFAState
