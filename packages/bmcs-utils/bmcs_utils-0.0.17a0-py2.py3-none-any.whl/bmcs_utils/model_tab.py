
import traits.api as tr
from bmcs_utils.i_interactive_model import IInteractiveModel
import ipywidgets as ipw

class ModelTab(tr.HasTraits):
    '''Base class for tabs within an interaction window.'''

    index = tr.Int

    model = tr.Instance(IInteractiveModel)

    interactor = tr.WeakRef

    def set_interactor(self, interactor):
        self.interactor = interactor

    n_steps = tr.Int(20)

    # @todo: an alternative implementation - analogy to traitsui.View
    def get_editors(self):
        ipw_view = self.model.ipw_view
        item_names = ipw_view.item_names
        items = ipw_view.content
        # The traits named in ipw_view are fetched from the model
        # one could directly call `traits` - but then also transient
        # traits like properties would be be accessed. This would disable
        # lazy evaluation of properties.
        # Using the self.traits(transient=is_none) does not work either
        # as then no Buttons could be used - they are also transient.
        # The result is a three step reteirval
        # 1) - use trait_get to obtain the values, transient values are empty
        values = [self.model.trait_get(name) for name in item_names]
        # 2) - convert the list of dictionaries to a single dictionary
        val_dict = {k: v for d in values for k, v in d.items()}
        # 3) - construct a list ordered according to `item_names` with
        #      values of transient traits set to none
        values_ = [val_dict.get(name, None) for name in item_names]
        # 4) - order the corresponding traits according item_names
        traits_ = [self.model.trait(name) for name in item_names]
        # construct a dictionary of editors that can be rendered
        editors = {
            item.name: item.get_editor(value_, trait_, self.model)
            for (item, trait_, value_) in
            zip(items, traits_, values_)
        }
        return editors

    freeze_editors = tr.Bool(False)

    def ipw_editor_changed(self, change):
        if self.freeze_editors:
            return

        name = change.owner.name
        val = change.new
        keyval = {name: val}
        self.model.trait_set(**keyval)
        ipw_view = self.model.ipw_view
        if not ipw_view.simulator:
            # If there is a simulater defined within the model
            # do not automatically update the plot. The plotting
            # is then handled by the simulator itself.
            self.interactor.update_plot(self.index)

    def notify_change(self, event):
        value = event.new
        ipw_editor = self.ipw_editors[event.name]
        # ipw_editor.unobserve(self.ipw_editor_changed,'value')
        self.freeze_editors = True
        ipw_editor.value = value
        self.freeze_editors = False
        # ipw_editor.observe(self.ipw_editor_changed, 'value')

    def widget_layout(self):

        vlist = []

        ipw_view = self.model.ipw_view
        if ipw_view.simulator:

            progress_bar_widgets = []
            run_sim = getattr(self.model, ipw_view.simulator)
            button = ipw.Button(description=ipw_view.simulator,
                                tooltip='Run the simulation with a progress bar',
                                layout=ipw.Layout(width='20%', height='30px'))
            button.style.button_color = 'darkgray'

            progress_bar = ipw.FloatProgress(min=0, max=1,
                                             layout=ipw.Layout(width='80%', height='30px'))
            def update_progress(value):
                progress_bar.value = value
            def button_clicked(change):
                run_sim(update_progress)
                self.interactor.update_plot(self.index)
            button.on_click(button_clicked)

            progress_bar_widgets.append(button)
            progress_bar_widgets.append(progress_bar)
            # define the reset action
            if ipw_view.reset_simulator:
                reset_sim = getattr(self.model, ipw_view.reset_simulator)
                reset_button = ipw.Button(description=ipw_view.reset_simulator,
                                    tooltip='Reset the simulation',
                                    layout=ipw.Layout(width='20%', height='30px'))
                reset_button.style.button_color = 'darkgray'
                def reset_button_clicked(change):
                    reset_sim()
                    self.interactor.update_plot(self.index)
                    progress_bar.value = 0
                reset_button.on_click(reset_button_clicked)
                progress_bar_widgets.append(reset_button)

            progress_box = ipw.HBox(progress_bar_widgets, layout=ipw.Layout(padding='5px'))
            vlist.append(progress_box)

        editors = self.get_editors()
        self.ipw_editors = {}

        for name, editor in editors.items():
            ipw_editor = editor.render()
            ipw_editor.name = name
            ipw_editor.observe(self.ipw_editor_changed, 'value')
            self.ipw_editors[name] = ipw_editor
            editor.model.observe(self.notify_change, name)

        # Originally, the interactive_ouput widget was used
        # here. But in this way, the update method was called
        # earlier than the tab change observer of the interactor
        # This caused problems if axes object did not correspond
        # to the model's update_plot method. Therefore,
        # slider observer is now used , augmented with the trait name.
        # out = ipw.interactive_output(self.update, sliders);

        layout = ipw.Layout(grid_template_columns='1fr 1fr', padding='6px', width='100%')
        ipw_view = self.model.ipw_view
        item_names = ipw_view.item_names
        item_editors_list = [self.ipw_editors[name] for name in item_names]
        grid = ipw.GridBox(item_editors_list, layout=layout)

        vlist.append(grid)
        frame = ipw.VBox(vlist)
        return frame

    def subplots(self, fig):
        return self.model.subplots(fig)

    def update_plot(self, axes):
        self.model.update_plot(axes)
