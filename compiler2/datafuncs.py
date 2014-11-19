APPLY = 1
CHECK = 2

LD = 2 #Lookup distance


def Atom(tag, vals=None):
    def call(tr, func = APPLY, ld=0):
        if func == APPLY:
            try:
                assert call(tr, CHECK)
            except:
                print tag, vals
                print tr.current()
                raise
            return tr.get()
        else:
            return tr.is_next_token([tag], vals, ld)
    return call

def And(*parts):
    def call(tr, func = APPLY, ld=0):
        if func == APPLY:
            sub = []
            for part in parts:
                to_append = part(tr)
                if isinstance(to_append, list):
                    sub += to_append
                else:
                    sub.append(to_append)
            return sub
        else:
            check = True
            for i in range(LD):
                check = check and parts[i](tr, CHECK, i+ld)
            return check
    return call

def Or(*options):
    def call(tr, func=APPLY, ld=0):
        if func==APPLY:
            for option in options:
                if option(tr, CHECK):
                    return option(tr)
        else:
            for option in options:
                if option(tr,CHECK, ld):
                    return True
            return False
    return call

def NamedStruct(name, part):
    def call(tr, func=APPLY, ld=0):
        if func == APPLY:
            ret = part(tr)
            if isinstance(ret, list):
                return {name:ret}
            else:
                return {name:[ret]}
        else:
            return part(tr, CHECK, ld)
    return call

def Maybe(part):
    def call(tr, func=APPLY, ld=0):
        if func==APPLY:
            if part(tr,CHECK):
                return part(tr)
            else:
                return []
        else:
            return True
    return call

def Star(part):
    def call(tr, func=APPLY, ld=0):
        if func==APPLY:
            sub = []
            while part(tr, CHECK):
                to_append = part(tr)
                if isinstance(to_append, list):
                    sub += to_append
                else:
                    sub.append(to_append)
            return sub
        else:
            return True
    return call


