from taggit_labels.widgets import LabelWidget

from django.forms import ModelForm

from .models import ActionTags


class ActionAdminForm(ModelForm):
    class Meta:
        widgets = {"tags": LabelWidget(model=ActionTags)}
