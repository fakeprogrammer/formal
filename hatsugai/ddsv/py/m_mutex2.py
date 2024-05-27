import ddsv

NUM_PROCESSES = 2

class StateVarsImp(ddsv.StateVars):
    def __init__(self, m0=0, m1=0):
        self.m0 = 0
        self.m1 = 0
    
    def __eq__(self, other) -> bool:
        return (self.m0 == other.m0 and self.m1 == other.m1)

    def __str__(self):
        return (f'm0={self.m0} m1={self.m1}')

    def hash_sv(self) -> int:
        hv = ((self.m0 << 1) + self.m1) % ddsv.HASH_LEN
        return hv

def guard_lock0(prop, p: StateVarsImp) -> bool:
    return p.m0 == 0

def guard_lock1(prop, p: StateVarsImp) -> bool:
    return p.m1 == 0

def action_lock0(prop, q: StateVarsImp, p: StateVarsImp):
    q.m0 = 1

def action_lock1(prop, q: StateVarsImp, p: StateVarsImp):
    q.m1 = 1

def action_unlock0(prop, q: StateVarsImp, p: StateVarsImp):
    q.m0 = 0

def action_unlock1(prop, q: StateVarsImp, p: StateVarsImp):
    q.m1 = 0

P0 = [{"label":"lock0", "target":1, "guard":guard_lock0, "action":action_lock0}]
P1 = [{"label":"lock1", "target":2, "guard":guard_lock1, "action":action_lock1}]
P2 = [{"label":"unlock1", "target":3, "guard":ddsv.guard_true, "action":action_unlock1}]
P3 = [{"label":"unlock0", "target":0, "guard":ddsv.guard_true, "action":action_unlock0}]

P_trans = [P0, P1, P2, P3, None]

Q0 = [{"label":"lock1", "target":1, "guard":guard_lock1, "action":action_lock1}]
Q1 = [{"label":"lock0", "target":2, "guard":guard_lock0, "action":action_lock0}]
Q2 = [{"label":"unlock0", "target":3, "guard":ddsv.guard_true, "action":action_unlock0}]
Q3 = [{"label":"unlock1", "target":0, "guard":ddsv.guard_true, "action":action_unlock1}]

Q_trans = [Q0, Q1, Q2, Q3, None]

def main():
    shared_vars = StateVarsImp()
    s0 = ddsv.State(shared_vars, NUM_PROCESSES)

    P = ddsv.Process("P", 0, P_trans)
    Q = ddsv.Process("Q", 0, Q_trans)

    process_def = [P, Q]
        
    lts = ddsv.concurrent_composition(process_def, s0)

    ddsv.vis_lts("m_lock2", lts)


if __name__== "__main__":
    main()
