
import traits.api as tr
from bmcs_utils.interactive_window import InteractiveWindow
from bmcs_utils.i_interactive_model import IInteractiveModel

@tr.provides(IInteractiveModel)
class InteractiveModel(tr.HasTraits):
    """Base class for interactive bmcs_utils
    """

    name = tr.Str("<unnamed>")

    def subplots(self, fig):
        return fig.subplots(1, 1)

    def plot(self, axes):
        '''Alias to update plot - to be overloaded by subclasses'''
        self.update_plot(axes)

    def update_plot(self, axes):
        raise NotImplementedError()

    def interact(self):
        return InteractiveWindow(self).interact()
