import django_filters
from django import forms
from Developer.models import DB_Fees,CustomUser
from django_filters import DateFilter
from django.forms import DateInput


class DueFees_Filter(django_filters.FilterSet):
    start_date = DateFilter(field_name='due_date', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='due_date', lookup_expr='lte', widget=DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(DueFees_Filter, self).__init__(*args, **kwargs)
        self.filters['due_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['due_date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = DB_Fees
        fields = ['due_date','student_class']
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'})
        }




class Student_name_Filter(django_filters.FilterSet):
     class Meta:
        model = CustomUser
        fields = ['student_class']
        # widgets = {
        #     'due_date': DateInput(attrs={'type': 'date'})
        # }