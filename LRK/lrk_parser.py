
class LRK:
    def __init__(self, grammar) -> None:
        self.grammar=grammar
        self.first= grammar.first
        self.follow= grammar.follow
        self.P= grammar.P
        self.S=grammar.start
        pass
