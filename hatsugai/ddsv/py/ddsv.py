import sys
import copy
from collections import deque, defaultdict

HASH_LEN = 10007

class StateVars:
    def hash_sv(self) -> int:
        return 0

class Process:
    def __init__(self, name = '', prop = 0, trans = None):
        self._name = name
        self._prop = prop
        self._trans = trans

class Trans:
    def __init__(self, link = None, who = '', label = '', state = None, on_deadlock_path = False):
        self._link = link
        self._who = who
        self._label = label
        self._state = state
        self._on_deadlock_path = on_deadlock_path

class State:
    def __init__(self, sv: StateVars = None, num_process = 1):
        if sv is not None:
            self._shared_vars = copy.deepcopy(sv)
        else:
            self._shared_vars = None
        self._id = 0
        self._location = [0] * num_process
        self._trans = None

    def equal(self, other) -> bool:
        return (self._shared_vars == other._shared_vars and self._location == other._location)

    def clone_state(self):
        s = State(self._shared_vars)
        s._location = copy.deepcopy(self._location)
        return s
    
    def hash_state(self) -> int:
        hval = self._shared_vars.hash_sv()
        for l in self._location:
            hval = ((hval << 1) ^ l) % HASH_LEN
        return hval

class Path:
    def __init__(self, path = None, trans = None):
        self._link = path
        if path is not None:
            path._refcount += 1
        self._refcount = 0
        self._trans = trans

class Lts:
    def __init__(self, process = None, num_states = 0):
        self._process = process
        self._num_states = num_states
        self._v = [None] * num_states

class SetIO():
    """with構文でI/Oを切り替えるためのクラス"""
    def __init__(self, filename: str):
        self.filename = filename

    def __enter__(self):
        sys.stdout = open(self.filename, "w")

    def __exit__(self, *args):
        sys.stdout = sys.__stdout__

def guard_true(prop: int, p) -> bool:
    return True

def action_nop(prop: int, q, p):
    pass

def ht_reg(ht: defaultdict, data: State) -> State:
    """Stateオブジェクトのハッシュテーブル"""
    hval = data.hash_state()
    if ht[hval] is not None:
        # ハッシュ値の衝突
        for d in ht[hval]:
            if data.equal(d):
                return d
        ht[hval].append(data)
    else:
        ht[hval] = [data]
    return data

def print_locations_str(process: list[Process], state: State) -> str:
    s = ''
    for j in range(len(process)):
        s += f'{process[j]._name}{state._location[j]} '
    return s

def print_state_str(process: Process, state: State) -> str:
    s = ''
    s += print_locations_str(process, state)
    s += str(state._shared_vars)
    return s

def path_add(path: Path, trans: Trans):
    p = Path()
    p._link = path
    if path is not None:
        path._refcount += 1
    p._refcount = 1
    p._trans = trans
    return p

def path_rev(p: Path) -> Path:
    q: Path = None
    while p is not None:
        t = path_add(q, p._trans)
        q = t
        p = p._link
    return q

def print_path(process: list[Process], path: Path):
    q = path_rev(path)
    i = 0
    while q is not None:
        s = ''
        s += f'{i:2d} {q._trans._who:<6} {q._trans._label:<10}'
        s += print_state_str(process, q._trans._state)
        print(s)
        q = q._link
        i += 1

def mark_path(path: Path):
    p = path
    while p is not None:
        trans: Trans = p._trans
        trans._on_deadlock_path = True
        p = p._link

def bfs(process: list[Process], s0: State) -> defaultdict:
    state_id = 1
    ht = defaultdict(list[State])
    s0._id = 0
    ht_reg(ht, s0)
    dq = deque()
    trans0 = Trans(None, "---", "---", s0)
    dq.append(Path(None, trans0))

    while len(dq) > 0:
        path: Path = dq.popleft()
        trans: Trans = path._trans
        s: State = trans._state

        for i in range(len(process)):
            loc = s._location[i]
            plist = process[i]._trans[loc]
            if plist is not None:
                for p in plist:
                    if (p['guard'])(process[i]._prop, s._shared_vars):
                        t: State = s.clone_state()
                        t._location[i] = p['target']
                        (p['action'])(process[i]._prop, t._shared_vars, s._shared_vars)

                        u = ht_reg(ht, t)
                        s._trans = Trans(s._trans, process[i]._name, p['label'], u)

                        if id(u) == id(t):
                            u._id = state_id
                            state_id += 1
                            dq.append(Path(path, s._trans))                    

        if s._trans == None:
            print("--------------------")
            print_path(process, path)
            mark_path(path)
    
    return ht

def concurrent_composition(process, state) -> Lts:
    ht = bfs(process, state)
    num_states = 0
    for vlst in ht.values():
        num_states += len(vlst)

    lts = Lts(process, num_states)
    for vlst in ht.values():
        for p in vlst:
            assert p._id >= 0 and p._id < num_states
            lts._v[p._id] = p

    return lts

def vis_lts(filename: str, lts: Lts):
    with SetIO(f'{filename}.dot'):
        print('digraph {')

        for i in range(lts._num_states):
            p: State = lts._v[i]

            outstr = f'{p._id} [label="{p._id}\\n'
            for j in range(len(lts._process)):
                outstr += f'{lts._process[j]._name}{p._location[j]} '
            outstr += '\\n'
            outstr += str(p._shared_vars)
            if p._trans is None:
                outstr += '",color=pink,style=filled];'
            elif p._id == 0:
                outstr += '",color=cyan,style=filled];'
            else:
                outstr += '"];'
            print(outstr)

            trans: Trans = p._trans
            while trans is not None:
                outstr = f'{p._id} -> {trans._state._id} [label="{trans._who}.{trans._label}"'
                if trans._on_deadlock_path:
                    outstr += ',color=red,fontcolor=red,weight=2,penwidth=2'
                outstr += '];'
                print(outstr)

                trans = trans._link

        print('}')
