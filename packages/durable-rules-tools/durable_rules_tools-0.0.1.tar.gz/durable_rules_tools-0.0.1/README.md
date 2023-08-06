# `durable_rules_magic`

[![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/innovationOUtside/durable_rules_magic/master?filepath=demo.ipynb)

Magic to simplify working with durable.rules in educational contexts, initially when working with "subject, predicate, object" triple style reasoning.

Install as:

`pip install --upgrade git+https://github.com/innovationOUtside/durable_rules_magic.git`

See the `demo.ipynb` for usage.


## Additional Notes

If we define:

```python
from IPython.display import Javascript

class Speech():
    def say(self, txt):
        display(Javascript(f'speechSynthesis.speak(new SpeechSynthesisUtterance("{txt}"))'))
```

then we can get Python to speak...

For example:

```python
speaker = Speech()
speaker.say('hello')
```

This means we can hear the reasoning using rules of the form:

```python
   @when_all(Subject('eats', 'worms'))
    def bird(c):
        speaker.say(f'if {c.m.subject} eats worms')
        Set(c, '? : is : bird')
        speaker.say(f'{c.m.subject} is a bird')
```

which would make the rules both accessible and easier to follow.

Could we perhaps create a decorator to the rules that would provide such spoken annotations?