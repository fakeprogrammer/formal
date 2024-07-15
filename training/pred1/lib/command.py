from typing import Callable
from lib.inout import *

state = []
history = []

def print_state(gs:list):
    if gs == []:
        print('No subgoals!')
    else:
        for i in range(len(gs)):
            state_str = ''
            a = gs[i]
            ps, qs = a
            state_str += f'{i}. '
            state_str += ', '.join(show_formula_list(ps))
            state_str += ' ' + TURNSTILE + ' '
            state_str += ', '.join(show_formula_list(qs))
            print(state_str)

def sequent(ps:list[Formula], qs:list[Formula]) -> None:
    history = []
    state = [[ps, qs]]
    print_state(state)

def theorem(f:Formula) -> None:
    global state, history
    history = []
    state = [[[], [f]]]
    print_state(state)

def apply(tactic:Callable[[list[Formula], list[Formula]], list]) -> None:
    global state, history
    if len(state) == 0:
        print('No subgoals!')
    else:
        if len(state) == 1:
            [ps, qs], gs = state[0], []
        else:
            [ps, qs], gs = state[0], state[1:]
        xs = tactic(ps, qs)
        history = [[state[0]]] + history
        state = xs + gs
        print_state(state)

def apply2(tactic:Callable[[Term, list[Formula], list[Formula]], list], t:Term) -> None:
    global state, history
    if len(state) == 0:
        print('No subgoals!')
    else:
        if len(state) == 1:
            [ps, qs], gs = state[0], []
        else:
            [ps, qs], gs = state[0], state[1:]
        xs = tactic(t, ps, qs)
        history = [[state[0]]] + history
        state = xs + gs
        print_state(state)

def undo() -> None:
    global state, history
    if len(history) == 0:
        print('no history')
    else:
        state = history[0]
        history = history[1:]
        print_state(state)
