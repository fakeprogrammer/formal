from dataclasses import dataclass
from enum import IntFlag, auto
from typing import Optional

class Conn(IntFlag):
    Not = auto()
    And = auto()
    Or = auto()
    Imp = auto()

class Quant(IntFlag):
    All = auto()
    Ex = auto()

@dataclass(frozen=True)
class Var:
    var_name: str

@dataclass
class Fun:
    fun_name: str
    term_lst: list['Term']

@dataclass
class Term:
    term: 'Var | Fun'

@dataclass
class Predicate:
    predicate_name: str
    term_lst: list['Term']

@dataclass
class Connective:
    conn: Conn
    lhf: 'Formula'
    rhf: Optional['Formula']

@dataclass
class Quantified:
    quant: 'Quant'
    var_name: 'Var'
    formula: 'Formula'

@dataclass
class Formula:
    formula: 'Predicate | Connective | Quantified'

@dataclass(frozen=True)
class Sequent:
    lhflst: list['Formula']
    rhflst: list['Formula']

TURNSTILE = '|-'
