from bmcs_utils.trait_types import \
    Float, Int, Bool, FloatRangeEditor, Range
from bmcs_utils.interactive_model import InteractiveModel
from bmcs_utils.item import Item
from bmcs_utils.view import View
import numpy as np

class ExampleModel(InteractiveModel):
    name = 'Example'

    a = Float(0, desc=r'first material parameter')
    b = Int(5, desc='input parameter')
    c = Bool(True)
    t = Float(0)

    ipw_view = View(
        Item('a', editor=FloatRangeEditor(low=0, high=10)),
        Item('b', latex=r'\beta', readonly=True),
        Item('t', latex=r'\theta', editor=FloatRangeEditor(low=0, high=1)),
        Item('c', latex=r'\gamma'),
        simulator='run',
        reset_simulator='reset'
    )

    def run(self, update_progress=lambda t:t):
        print('where are you')
        self.a += 1
        t_arr = np.linspace(0, 1, 10)
        for t in t_arr:
            self.t = t
            update_progress(t)

    def reset(self):
        print('reset called')
        self.trait_set(a=0, b=5, c=True, t=0)

    def update_plot(self, axes):
        print('update_plot called')
        trait_names = self.trait_names()
        print(self.trait_get(trait_names))

# ex = ExampleModel()
# ex.interact()
# ex.run()
