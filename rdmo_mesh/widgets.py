from rdmo.questions.widgets import Widget


class DescriptorWidget(Widget):
    widget_class = 'autocomplete'
    template_name = 'mesh/project_questions_form_group_descriptor.html'
    js_files = ('mesh/js/mesh.js', )


class QualifierWidget(Widget):
    template_name = 'mesh/project_questions_form_group_qualifier.html'
    widget_class = 'select'
