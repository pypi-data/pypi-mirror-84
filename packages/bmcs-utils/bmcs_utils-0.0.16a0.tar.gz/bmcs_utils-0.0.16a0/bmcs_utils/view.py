
import traits.api as tr
from bmcs_utils.item import Item

class View(tr.HasTraits):
    """Container of IPWItems
    """
    content = tr.List(Item)
    item_names = tr.List(tr.Str)

    # -------------------------------------------------------------------------
    #  Initializes the object:
    # -------------------------------------------------------------------------

    def __init__(self, *values, **traits):
        """ Initializes the object.
        """
        tr.HasTraits.__init__(self, **traits)
        for item in values:
            self.content.append(item)
            self.item_names.append(item.name)

    simulator = tr.Str
    """Name of the method running the model simulation
    """

    reset_simulator = tr.Str
    """Name of the method resetting the model simulation
    """


