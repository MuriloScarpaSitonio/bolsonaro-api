from taggit_labels.widgets import LabelWidget

from django.forms import ModelForm

from .models import QuoteTags


class QuoteAdminForm(ModelForm):
    class Meta:
        widgets = {"tags": LabelWidget(model=QuoteTags)}
