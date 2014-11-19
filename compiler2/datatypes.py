#Author: Mayank Mandava
#Jack Compiler


class And:
    def __init__(self, *parts):
        self.name = name
        self.parts = parts
        self.identify = parts[0].identify
    def consume(self,tr):
        sub = []
        for part in self.parts:
            to_append = part.consume(tr)
            if to_append is not None:
                sub.append(to_append)
        return sub

class Or:
    def __init__(self, *options):
        self.options = options
    def consume(self,tr):
        sub = []
        for option in self.options:
            if option.identify(tr):
                sub.append(option.consume(tr))
                break
        return sub
    def identify(self, tr):
        for option in self.options:
            if option.identify(tr):
                return True
        return False


class NamedStruct:
    def __init__(self, name, part):
        self.name = name
        self.part = part
        self.identify = part.identify
    def consume(self,tr):
        return {name: part.consume()}


class Maybe:
    def __init__(self, *parts):
        self.parts = parts
    def consume(self,tr):
        sub = []
        if self.parts[0].identify(tr):
            return And(*self.parts).consume()
        else:
            return None

class Star:
    def __init__(self, part):
        self.part = part
    def consume(self):
        sub = []
        if part.identify(tr):
            while part.identify(tr):
                sub.append(part.consume(tr))
            return sub
        else:
            return None

class Atom:
    def __init__(self, tag, vals=None):
        self.tag = tag
        self.vals = vals
    def consume(self,tr):
        assert self.identify(tr)
        return tr.get()
    def identify(self, tr):
        return tr.is_next_token([self.tag],self.vals)
