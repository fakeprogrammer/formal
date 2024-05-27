import ddsv

MAX_COUNT = 2

class StateVarsImp(ddsv.StateVars):
    def __init__(self, mutex=0, cond=0, count=0):
        self.mutex = mutex
        self.cond = cond
        self.count = count
    
    def __eq__(self, other) -> bool:
        return (self.mutex == other.mutex and
                self.cond == other.cond and
                self.count == other.count)

    def __str__(self):
        return (f'm={self.mutex} cv={self.cond} c={self.count}')

    def hash_sv(self) -> int:
        hv = ((((self.mutex << 2) ^ self.cond) << 2) ^ self.count) % ddsv.HASH_LEN
        return hv

def guard_lock(prop, p: StateVarsImp) -> bool:
    return p.mutex == 0

def action_lock(prop, q: StateVarsImp, p: StateVarsImp):
    q.mutex = 1

def action_unlock(prop, q: StateVarsImp, p: StateVarsImp):
    q.mutex = 0

def guard_not_empty(prop, p: StateVarsImp) -> bool:
    return p.count > 0

def guard_not_full(prop, p: StateVarsImp) -> bool:
    return p.count < MAX_COUNT

def guard_empty(prop, p: StateVarsImp) -> bool:
    return p.count == 0

def guard_full(prop, p: StateVarsImp) -> bool:
    return p.count == MAX_COUNT

def guard_ready(process_id_bit, p: StateVarsImp) -> bool:
    return (p.cond & process_id_bit) == 0

def action_wait(process_id_bit, q: StateVarsImp, p: StateVarsImp):
    q.mutex = 0
    q.cond = (p.cond | process_id_bit)

def action_signal(process_id_bit, q: StateVarsImp, p: StateVarsImp):
    q.cond = (p.cond & (p.cond - 1))

def action_inc(prop, q: StateVarsImp, p: StateVarsImp):
    q.count = p.count + 1

def action_dec(prop, q: StateVarsImp, p: StateVarsImp):
    q.count = p.count - 1

P0 = [{"label":"lock", "target":1, "guard":guard_lock, "action":action_lock}]
P1 = [{"label":"wait", "target":2, "guard":guard_full, "action":action_wait},
      {"label":"produce", "target":3, "guard":guard_not_full, "action":action_inc}]
P2 = [{"label":"wakeup", "target":0, "guard":guard_ready, "action":ddsv.action_nop}]
P3 = [{"label":"signal", "target":4, "guard":ddsv.guard_true, "action":action_signal}]
P4 = [{"label":"unlock", "target":0, "guard":ddsv.guard_true, "action":action_unlock}]

P_trans = [P0, P1, P2, P3, P4, None]

Q0 = [{"label":"lock", "target":1, "guard":guard_lock, "action":action_lock}]
Q1 = [{"label":"wait", "target":2, "guard":guard_empty, "action":action_wait},
      {"label":"consume", "target":3, "guard":guard_not_empty, "action":action_dec}]
Q2 = [{"label":"wakeup", "target":0, "guard":guard_ready, "action":ddsv.action_nop}]
Q3 = [{"label":"signal", "target":4, "guard":ddsv.guard_true, "action":action_signal}]
Q4 = [{"label":"unlock", "target":0, "guard":ddsv.guard_true, "action":action_unlock}]

Q_trans = [Q0, Q1, Q2, Q3, Q4, None]

def main():
    shared_vars = StateVarsImp(0, 0, 0)
    s0 = ddsv.State(shared_vars)

    P = ddsv.Process("P", 1, P_trans)
    Q = ddsv.Process("Q", 2, Q_trans)

    process_def = [P, Q]
        
    lts = ddsv.concurrent_composition(process_def, s0)

    ddsv.vis_lts("m_prod_cons1", lts)


if __name__== "__main__":
    main()
