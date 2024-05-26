import ddsv

class StateVarsImp(ddsv.StateVars):
    def __init__(self, x=0, t1=0, t2=0, mutex=0):
        self.x = x
        self.t1 = t1
        self.t2 = t2
    
    def __eq__(self, other) -> bool:
        return (self.x == other.x and self.t1 == other.t1 and self.t2 == other.t2)

    def __str__(self):
        return (f'x={self.x} t1={self.t1} t2={self.t2}')

    def hash_sv(self) -> int:
        hv = ((((self.x << 2) ^ self.t1) << 2) ^ self.t2) % ddsv.HASH_LEN
        return hv

def action_P_read(prop, q: StateVarsImp, p: StateVarsImp):
    q.t1 = p.x

def action_P_inc(prop, q: StateVarsImp, p: StateVarsImp):
    q.t1 = p.t1 + 1

def action_P_write(prop, q: StateVarsImp, p: StateVarsImp):
    q.x = p.t1

P0 = [{"label":"read", "target":1, "guard":ddsv.guard_true, "action":action_P_read}]
P1 = [{"label":"inc", "target":2, "guard":ddsv.guard_true, "action":action_P_inc}]
P2 = [{"label":"write", "target":3, "guard":ddsv.guard_true, "action":action_P_write}]

P_trans = [P0, P1, P2, None]

def action_Q_read(prop, q: StateVarsImp, p: StateVarsImp):
    q.t2 = p.x

def action_Q_inc(prop, q: StateVarsImp, p: StateVarsImp):
    q.t2 = p.t2 + 1

def action_Q_write(prop, q: StateVarsImp, p: StateVarsImp):
    q.x = p.t2

Q0 = [{"label":"read", "target":1, "guard":ddsv.guard_true, "action":action_Q_read}]
Q1 = [{"label":"inc", "target":2, "guard":ddsv.guard_true, "action":action_Q_inc}]
Q2 = [{"label":"write", "target":3, "guard":ddsv.guard_true, "action":action_Q_write}]

Q_trans = [Q0, Q1, Q2, None]

def main():
    shared_vars = StateVarsImp()
    s0 = ddsv.State(shared_vars)

    P = ddsv.Process("P", 0, P_trans)
    Q = ddsv.Process("Q", 0, Q_trans)

    process_def = [P, Q]
        
    lts = ddsv.concurrent_composition(process_def, s0)

    ddsv.vis_lts("m_inc2", lts)


if __name__== "__main__":
    main()
