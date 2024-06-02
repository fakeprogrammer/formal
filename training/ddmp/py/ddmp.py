from collections import deque

class Process:
    def __init__(self, status=[], transitions=[]):
        self._status = status
        self._transitions = transitions

def concurrent_composition(a: Process, b: Process, sync_events: list) -> Process:
    s = set()
    for tr in a._transitions:
        s.add(tr[0])
    for tr in b._transitions:
        s.add(tr[0])
    all_events = sorted(s)

    visited_set = set()
    visited = []
    transitions = []
    q = deque([(a._status[0], b._status[0])])
    while q:
        sa, sb = q.popleft()
        state = (sa, sb)
        if state in visited_set:
            continue
        visited_set.add(state)
        visited.append(state)
        for ev in all_events:
            if ev in sync_events:
                for _, a1, a2 in filter(lambda x: x[0] == ev, a._transitions):
                    if a1 != sa:
                        continue
                    for _, b1, b2 in filter(lambda x: x[0] == ev, b._transitions):
                        if b1 != sb:
                            continue
                        q.append((a2, b2))
                        transitions.append([ev, f'{sa}{sb}', f'{a2}{b2}'])
            else:
                for _, a1, a2 in filter(lambda x: x[0] == ev, a._transitions):
                    if a1 != sa:
                        continue
                    q.append((a2, sb))
                    transitions.append([ev, f'{sa}{sb}', f'{a2}{sb}'])
                for _, b1, b2 in filter(lambda x: x[0] == ev, b._transitions):
                    if b1 != sb:
                        continue
                    q.append((sa, b2))
                    transitions.append([ev, f'{sa}{sb}', f'{sa}{b2}'])
        
    print(visited)
    print(transitions)
