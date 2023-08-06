from IPython.core.magic import magics_class, line_cell_magic, Magics
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import warnings

from .rules_utils import quick_assert_fact, quick_retract_fact, quick_post_event, _delete_state


# TO DO - things are passed in from the magic as strings
# Should we try to cast them to eg int, float, list, tuple, dict?


@magics_class
class DurableRulesMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(DurableRulesMagic, self).__init__(shell)
        self.graph = None
        self.RULESET = None

    @line_cell_magic
    @magic_arguments()
    @argument('--ruleset', '-r', default='', help='Ruleset name.')
    @argument('--no-reset', action='store_false', help='Disable automatic state deletion.')
    def assert_facts(self, line, cell):
        "Assert and/or retract several facts."
        args = parse_argstring(self.assert_facts, line)
        if not args.ruleset and self.RULESET is None:
            warnings.warn("You must provide a ruleset reference (--ruleset/-r RULESET).")
            return
        elif args.ruleset:
            self.RULESET = self.shell.user_ns[args.ruleset]

        _ruleset = self.RULESET
        #print(_ruleset)

        if args.no_reset:
            _delete_state(_ruleset)

        for _assertion in cell.split('\n'):
            if _assertion.startswith('-'):
                quick_retract_fact(_ruleset, _assertion.lstrip('-'))
            elif not _assertion.startswith('#'):
                quick_assert_fact(_ruleset, _assertion)

    @line_cell_magic
    @magic_arguments()
    @argument('--ruleset', '-r', default='', help='Ruleset name.')
    @argument('--no-reset', action='store_false', help='Disable automatic state deletion.')
    def retract_facts(self, line, cell):
        "Retract and/or assert several facts."
        args = parse_argstring(self.retract_facts, line)
        if not args.ruleset and self.RULESET is None:
            warnings.warn("You must provide a ruleset reference (--ruleset/-r RULESET).")
            return
        elif args.ruleset:
            self.RULESET = self.shell.user_ns[args.ruleset]

        _ruleset = self.RULESET
        #print(_ruleset)

        if args.no_reset:
            _delete_state(_ruleset)

        for _assertion in cell.split('\n'):
            if _assertion.startswith('*'):
                quick_assert_fact(_ruleset, _assertion.lstrip('-'))
            elif not _assertion.startswith('#'):
                quick_retract_fact(_ruleset, _assertion)

    @line_cell_magic
    @magic_arguments()
    @argument('--ruleset', '-r', default='', help='Ruleset name.')
    @argument('--no-reset', action='store_false', help='Disable automatic state deletion.')
    def post_events(self, line, cell):
        "Post several events."
        args = parse_argstring(self.post_events, line)
        if not args.ruleset and self.RULESET is None:
            warnings.warn("You must provide a ruleset reference (--ruleset/-r RULESET).")
            return
        elif args.ruleset:
            self.RULESET = self.shell.user_ns[args.ruleset]

        _ruleset = self.RULESET
        #print(_ruleset)

        if args.no_reset:
            _delete_state(_ruleset)

        for _assertion in cell.split('\n'):
            if not _assertion.startswith('#'):
                quick_post_event(_ruleset, _assertion)

    @line_cell_magic
    @magic_arguments()
    @argument('--ruleset', '-r', default='', help='Ruleset name.')
    @argument('--no-reset', action='store_false', help='Disable automatic state deletion.')
    def facts_and_events(self, line, cell):
        "Assert and/or retract several facts and/or post several events."
        args = parse_argstring(self.facts_and_events, line)
        if not args.ruleset and self.RULESET is None:
            warnings.warn("You must provide a ruleset reference (--ruleset/-r RULESET).")
            return
        elif args.ruleset:
            self.RULESET = self.shell.user_ns[args.ruleset]

        _ruleset = self.RULESET
        #print(_ruleset)

        if args.no_reset:
            _delete_state(_ruleset)

        for _assertion in cell.split('\n'):
            if _assertion.startswith('-'):
                quick_retract_fact(_ruleset, _assertion.lstrip('-'))
            elif _assertion.startswith('*'):
                quick_assert_fact(_ruleset, _assertion.lstrip('*'))
            elif _assertion.startswith('%'):
                quick_post_event(_ruleset, _assertion.lstrip('%'))