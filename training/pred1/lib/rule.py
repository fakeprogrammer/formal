from lib.syntax import *
from lib.inout import *

def find_connective(connective:Conn, formula_list:list[Formula]) -> list[list[Formula]]:
    r1, r2 = [], []
    
    for f in formula_list:
        match (f.formula):
            case Connective(conn=c, lhf=f1, rhf=f2):
                if c == connective:
                    r2 = [f1, f2]
                    formula_idx = formula_list.index(f)
                    if formula_idx < len(formula_list) - 1:
                        r1 += formula_list[formula_idx + 1:]
                    break
                else:
                    r1.append(f)
            case _:
                raise Exception

    return [r1, r2]

def find_quantified(quantifier:Quant, fs:list[Formula]) -> tuple[list[Formula], Var|None, Formula|None]:
    other_formula = []

    if fs == []:
        raise Exception
    for f in fs:
        match (f.formula):
            case Quantified(quant=q, var_name=x, formula=f1):
                if q == quantifier:
                    formula_idx = fs.index(f)
                    if formula_idx < len(fs) - 1:
                        other_formula += fs[formula_idx + 1:]
                    return (other_formula, x, f1)
                else:
                    other_formula.append(f)
            case _:
                other_formula.append(f)

    return ([], None, None)


def collect_vars_in_term(acc:list[Var], t:Term) -> list[Var]:
    result = acc.copy()
    match(t):
        case Var(var_name=x):
            result.append(t)
        case Fun(fun_name=_, term_lst=ts):
            result = reduce(collect_vars_in_term, ts, result)
    return list(set(result))

def collect_vars_in_formula(acc:list[Var], f:Formula) -> list[Var]:
    result = acc.copy()
    match(f.formula):
        case Predicate(predicate_name=_, term_lst=ts):
            result = reduce(collect_vars_in_term, ts, result)
        case Connective(conn=_, lhf=fs1, rhf=fs2):
            if fs2 is not None:
                result = reduce(collect_vars_in_formula, [fs1, fs2], result)
            else:
                result = reduce(collect_vars_in_formula, [fs1], result)               
        case Quantified(quant=_, var_name=x, formula=f):
            vs = reduce(collect_vars_in_formula, [f], [])
            result += [v for v in vs if v != x]
    return list(set(result))

def collect_vars_in_formula_list(acc:list[Var], fs:list[Formula]) -> list[Var]:
    return reduce(collect_vars_in_formula, fs, acc)

def rename(xs:list[Var], x:Var) -> Var:
    if x not in xs:
        return x
    else:
        i = 2
        while True:
            y = f'{x.var_name}{i}'
            if Var(y) not in xs:
                return Var(y)
            i = i + 1

def subst_term(x:str, u:Term, t:Term) -> Term:
    match(t):
        case Var(var_name=y):
            if x == y: return u
            else: return t
        case Fun(fun_name=f, term_lst=ts):
            return Fun(f, [subst_term(x, u, t) for t in ts])

def subst_formula(x:str, t:Term, f:Formula) -> Formula:
    xs = collect_vars_in_term([], t)

    def subst(x:str, t:Term, f:Formula) -> Formula:
        nonlocal xs
        match(f.formula):
            case Predicate(predicate_name=p, term_lst=ts):
                return Formula(Predicate(p, [subst_term(x, t, t2) for t2 in ts]))
            case Connective(conn=c, lhf=fs1, rhf=fs2):
                if fs2 is not None:
                    return Formula(Connective(c, subst(x, t, fs1), subst(x, t, fs2)))
                else:
                    return Formula(Connective(c, subst(x, t, fs1), None))
            case Quantified(quant=q, var_name=y, formula=f2):
                if Var(x) == y:
                    return f
                elif y in xs:
                    ys = collect_vars_in_formula(xs, f2)
                    z = rename(ys, y)
                    return Formula(Quantified(q, z, subst(x, t, (subst(y.var_name, z, f2)))))
                else:
                    return Formula(Quantified(q, y, subst(x, t, f2)))
    
    return subst(x, t, f)

def conjL(ps:list[Formula], qs:list[Formula]) -> list:
    ps, [f1, f2] = find_connective(Conn.And, ps)
    result = [[[f1, f2] + ps, qs]]
    return result

def conjR(ps:list[Formula], qs:list[Formula]) -> list:
    qs, [f1, f2] = find_connective(Conn.And, qs)
    result = [[ps, [f1] + qs], [ps, [f2] + qs]]
    return result

def disjL(ps:list[Formula], qs:list[Formula]) -> list:
    ps, [f1, f2] = find_connective(Conn.Or, ps)
    result = [[[f1] + ps, qs], [[f2] + ps, qs]]
    return result

def disjR(ps:list[Formula], qs:list[Formula]) -> list:
    qs, [f1, f2] = find_connective(Conn.Or, qs)
    result = [[ps, [f1, f2] + qs]]
    return result

def impL(ps:list[Formula], qs:list[Formula]) -> list:
    ps, [f1, f2] = find_connective(Conn.Imp, ps)
    result = [[ps, [f1] + qs], [[f2] + ps, qs]]
    return result

def impR(ps:list[Formula], qs:list[Formula]) -> list:
    qs, [f1, f2] = find_connective(Conn.Imp, qs)
    result = [[[f1] + ps, [f2] + qs]]
    return result

def negL(ps:list[Formula], qs:list[Formula]) -> list:
    ps, [f, _] = find_connective(Conn.Not, ps)
    result = [[ps, [f] + qs]]
    return result

def negR(ps:list[Formula], qs:list[Formula]) -> list:
    qs, [f, _] = find_connective(Conn.Not, qs)
    result = [[[f] + ps, qs]]
    return result

def allL(t:Term, ps:list[Formula], qs:list[Formula]) -> list:
    (ps2, x, f) = find_quantified(Quant.All, ps)
    if x is not None:
        return [[[subst_formula(x.var_name, t, f), Formula(Quantified(Quant.All, x, f))], qs]]
    return []

def allR(ps:list[Formula], qs:list[Formula]) -> list:
    xs = collect_vars_in_formula_list([], ps + qs)
    (qs2, x, f) = find_quantified(Quant.All, qs)
    if x is not None:
        z = rename([x] + xs, x)
        return [[ps, [subst_formula(x.var_name, z, f)]]]
    return []

def exL(ps:list[Formula], qs:list[Formula]) -> list:
    xs = collect_vars_in_formula_list([], ps + qs)
    (ps2, x, f) = find_quantified(Quant.Ex, ps)
    if x is not None:
        y = rename([x] + xs, x)
        return [[[subst_formula(x.var_name, y, f)], qs]]
    return []

def exR(t:Term, ps:list[Formula], qs:list[Formula]) -> list:
    (qs2, x, f) = find_quantified(Quant.Ex, qs)
    if x is not None:
        return [[ps, [subst_formula(x.var_name, t, f), Formula(Quantified(Quant.Ex, x, f))]]]
    return []

def assumption(ps:list[Formula], qs:list[Formula]) -> list:
    for q in qs:
        if q in ps:
            return []
    raise Exception

