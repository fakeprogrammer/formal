from functools import reduce
from lib.syntax import *

def prec_conn(c:Conn) -> int:
    match(c):
        case Conn.Not:
            return 1
        case Conn.And:
            return 2
        case Conn.Or:
            return 3
        case Conn.Imp:
            return 4

def prec_formula(f:Formula) -> int:
    match(f.formula):
        case Predicate():
            return 0
        case Connective(conn=c, lhf=_, rhf=_):
            return prec_conn(c)
        case Quantified():
            return 6

def show_conn(c:Conn) -> str:
    match(c):
        case Conn.Not:
            return '~'
        case Conn.And:
            return '&'
        case Conn.Or:
            return '|'
        case Conn.Imp:
            return '-->'

def show_quant(q:Quant) -> str:
    match(q):
        case Quant.All:
            return 'All '
        case Quant.Ex:
            return 'Ex '

def show_term(t:Term) -> str:
    match(t):
        case Var(var_name=x):
            return x
        case Fun(fun_name=f, term_lst=ts):
            if ts == []:
                return f
            else:
                return f + f'({show_term_list(ts)})'
        case _:
            return '<unknown term>'

def show_term_list(ts:list['Term']) -> str:
    match(ts):
        case []:
            return ''
        case _:
            thdr, trst = ts[0], ts[1:]
            return(reduce(lambda s, t: s + ', ' + show_term(t), trst, show_term(thdr)))

def show_formula(formula:Formula) -> str:
    result = ''

    try:
        f = formula.formula
        match (f):
            case Predicate(predicate_name=p, term_lst=ts):
                if ts == []:
                    result = p
                else:
                    result = p + f'({show_term_list(ts)})'
            case Connective(conn=c, lhf=f1, rhf=f2):
                match (c):
                    case Conn.Not:
                        if prec_conn(Conn.Not) < prec_formula(f1):
                            result = f'{show_conn(Conn.Not)}({show_formula(f1)})'
                        else:
                            result = f'{show_conn(Conn.Not)}{show_formula(f1)}'
                    case _:
                        if prec_conn(c) <= prec_formula(f1):
                            result += f'({show_formula(f1)}) '
                        else:
                            result += f'{show_formula(f1)} '
                        result += show_conn(c)
                        if prec_conn(c) < prec_formula(f2):
                            result += f' ({show_formula(f2)})'
                        else:
                            result += f' {show_formula(f2)}'
            case Quantified(quant=q, var_name=x, formula=f):
                result += f'{show_quant(q)}{show_term(x)}. {show_formula(f)}'
            case _:
                result = '<unknown-formula>'
    except:
        result = '<unknown-formula>'
    finally:
        return result

def show_formula_list(fs:list[Formula]) -> list[str]:
    result = []
    for f in fs:
        result.append(show_formula(f))
    return result
