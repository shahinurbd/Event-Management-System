from django import forms
from events.models import Event,Category,Participant


class StyleFormMixin:

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_style_widgets()

    default_class = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 m-2"

    def apply_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_class,
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_class,
                    'placeholder': f"Enter {field.label.lower()}",
                    'row': 5
                })
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300 p-1 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 mt-2 form-control ",
                    'type': 'datetime-local'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "mt-1"
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_class,
                    'placeholder': "Enter Email"
                })
            
            
            


class EventModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Event

        fields = ['Event_Name','description','Date_and_Time','location','category'] 

        widgets = {
            'Date_and_Time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            
        }

        def __init__(self, *arg, **kwarg):
            super().__init__(*arg, **kwarg)
            self.apply_style_widgets()


           
        

class ParticipantModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Participant

        fields = ['Participant_Name','email','event']

        widgets = {
            'email': forms.EmailInput(attrs={

            }),
            'event': forms.CheckboxSelectMultiple(attrs={

            })
            
        }

        def __init__(self, *arg, **kwarg):
            super().__init__(*arg, **kwarg)
            self.apply_style_widgets()



class CategoryModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Category

        fields = ['Category_Name','description']



        def __init__(self, *arg, **kwarg):
            super().__init__(*arg, **kwarg)
            self.apply_style_widgets()


class categoryModel(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False, 
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control border border-yellow-500 p-2 text-md bg-yellow-600 text-white rounded-sm'})
    )
    


    



        

        





    



