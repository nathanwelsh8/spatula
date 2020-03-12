from django.forms import ModelChoiceField

class NameChoiceField(ModelChoiceField):
    # display the category name in the form,
    # not the name of the object
    def label_from_instance(self, obj):
        return '{n}'.format(n=obj.name)