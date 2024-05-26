import ddsv 

MAX_QUE_LENGTH = 3

class StateVarsImp(ddsv.StateVars):
    def __init__(self):
        self.c = [0] * ddsv.NUM_PROCESSES
    
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

def main():
    shared_vars = StateVarsImp()
    s0 = ddsv.State(shared_vars)

    P = ddsv.Process("P", 0, P_trans)
    Q = ddsv.Process("Q", 0, Q_trans)

    process_def = [P, Q]
        
    lts = ddsv.concurrent_composition(process_def, s0)

    ddsv.vis_lts("m_lock2", lts)


if __name__== "__main__":
    main()
