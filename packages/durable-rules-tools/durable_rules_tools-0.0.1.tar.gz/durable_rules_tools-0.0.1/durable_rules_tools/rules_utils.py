from IPython.core.magic import magics_class, line_cell_magic, Magics
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

import uuid
from durable.lang import assert_fact, retract_fact, post, delete_state, m, c
from durable.engine import MessageObservedException
import warnings


def new_ruleset(name=None):
    """Optionally create, then set, new ruleset name."""
    #TO DO - add in rules to check a name is well-formed
    if name and isinstance(name, str):
        return name
    return f'rs_{uuid.uuid4()}'

def Subject(pred, obj):
    """Clause where subject is assumed and predicate and object tested."""
    return (m.predicate == pred) & (m.object == obj)

def Predicate(subj, obj):
    """Clause where predicate is assumed and subject and object tested."""
    return  (m.subject == subj) & (m.object == obj)

def Object(subj, pred):
    """Clause where object is assumed and subject and predicate tested."""
    return  (m.subject == subj) & (m.predicate == pred)

def _delete_state(rs):
    """Clear the state associated with a ruleset."""
    try:
        delete_state(rs, None)
    except:
        pass

def SPO(subj, pred, obj):
    """Return subject-predicate-object dict."""
    if not isinstance(subj, str):
        subj = subj.m.subject
    if not isinstance(obj, str):
        obj = subj.m.object
    if not isinstance(pred, str):
        pred = subj.m.predicate
    return { 'subject': subj, 'predicate': pred, 'object': obj }

def Set(c, statement):
    _statement = [x.strip() for x in statement.split(':')]
    subj = _statement[0] if  _statement[0]!='?' else c.m.subject
    pred = _statement[1] if  _statement[1]!='?' else c.m.predicate
    obj = _statement[2] if  _statement[2]!='?' else c.m.object
    try:
        c.assert_fact( SPO(subj, pred, obj ) )
    except MessageObservedException:
        warnings.warn(f"Assertion error: is {statement} already asserted?")
    

def quick_assert_fact(r, f):
    """
    Assert a fact from a colon separated triple string.
    Triple strings of the form: "a subject: predicate : and object"
    """
    _statement = [t.strip() for t in f.split(':')]
    
    if len(_statement) == 3:
        subj = _statement[0]
        pred = _statement[1]
        obj = _statement[2]
        #print('..', r, spo(subj, pred, obj ),'..' )
        try:
            assert_fact(r, SPO(subj, pred, obj ) )
        except MessageObservedException:
            warnings.warn(f"Assertion error: is {_statement} already asserted?")
    elif len(_statement) == 2:
        assert_fact(r, {_statement[0]: _statement[1]})

def quick_retract_fact(r, f):
    """
    Retract a fact from a colon separated triple string.
    Triple strings of the form: "a subject: predicate : and object"
    """
    _statement = [t.strip() for t in f.split(':')]
    
    if len(_statement) == 3:
        subj = _statement[0]
        pred = _statement[1]
        obj = _statement[2]
        #print('..', r, spo(subj, pred, obj ),'..' )
        try:
            retract_fact(r, SPO(subj, pred, obj ) )
        except MessageObservedException:
            warnings.warn(f"Retraction error with {_statement}.")

    elif len(_statement) == 2:
        retract_fact(r, {_statement[0]: _statement[1]})

def quick_post_event(r, f):
    """
    Post an event from a colon separated triple string.
    Triple strings of the form: "a subject: predicate : and object"
    """
    _statement = [t.strip() for t in f.split(':')]
    
    if len(_statement) == 3:
        subj = _statement[0]
        pred = _statement[1]
        obj = _statement[2]
        #print('..', r, spo(subj, pred, obj ),'..' )
        try:
            post(r, SPO(subj, pred, obj ) )
        except MessageObservedException:
            warnings.warn(f"Post event error with {_statement}.")
    elif len(_statement) == 2:
        post(r, {_statement[0]: _statement[1]})