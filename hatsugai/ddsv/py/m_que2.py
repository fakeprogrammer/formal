import ddsv 

MAX_QUE_LENGTH = 2

class StateVarsImp(ddsv.StateVars):
    def __init__(self, c0=0, c1=0):
        self.c = [c0, c1]
    
    def __eq__(self, other) -> bool:
        for i in range(ddsv.NUM_PROCESSES):
            return (self.c[i] == other.c[i])

    def __str__(self):
        s = ''
        for i in range(ddsv.NUM_PROCESSES):
            s += f'c[{i}]={self.c[i]} '
        return s

    def hash_sv(self) -> int:
        hv = 0
        for i in range(ddsv.NUM_PROCESSES):
            hv = (hv << 2) ^ self.c[i]
        return hv

def guard_que_not_empty(prop: int, p: StateVarsImp) -> bool:
    return p.c[prop] > 0

def guard_que_not_full(prop: int, p: StateVarsImp) -> bool:
    j = (prop + 1) % ddsv.NUM_PROCESSES
    return p.c[j] < MAX_QUE_LENGTH

def action_deque(prop: int, q: StateVarsImp, p: StateVarsImp):
    q.c[prop] = p.c[prop] - 1

def action_enque(prop: int, q: StateVarsImp, p: StateVarsImp):
    j = (prop + 1) % ddsv.NUM_PROCESSES
    q.c[j] = p.c[j] + 1

P0 = [{"label":"deque", "target":1, "guard":guard_que_not_empty, "action":action_deque}]
P1 = [{"label":"enque", "target":0, "guard":guard_que_not_full, "action":action_enque}]

P_trans = [P0, P1, None]

Q0 = [{"label":"deque", "target":1, "guard":guard_que_not_empty, "action":action_deque}]
Q1 = [{"label":"enque", "target":2, "guard":guard_que_not_full, "action":action_enque}]
Q2 = [{"label":"enque", "target":0, "guard":guard_que_not_full, "action":action_enque}]

Q_trans = [Q0, Q1, Q2, None]

def main():
    shared_vars = StateVarsImp(1, 0)
    s0 = ddsv.State(shared_vars)

    P = ddsv.Process("P", 0, P_trans)
    Q = ddsv.Process("Q", 1, Q_trans)

    process_def = [P, Q]

    lts = ddsv.concurrent_composition(process_def, s0)

    ddsv.vis_lts("m_que2", lts)


if __name__== "__main__":
    main()
