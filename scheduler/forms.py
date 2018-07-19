from datetime import datetime
from django import forms

from .models import Scheduler

NAME_ERROR_LIST = {'required': 'Введите Ваше имя',
                   'min_length': 'Слишком короткое имя',
                   'max_length': 'Слишком длинное имя'
                   }


# def time_choices_validator(date=datetime.now().date()):
#     schedulers = Scheduler.objects.filter(repair_date=date)
#     busy_time = []
#     for sched in schedulers:
#         busy_time.append(sched.repair_time)
#     valid_time = [(tag.name, tag.value) for tag in TimeChoice if tag.name not in busy_time]
#
#     return valid_time

class SchedulerForm(forms.ModelForm):
    class Meta:
        model = Scheduler
        fields = ('username', 'honeypot', 'address', 'telephone', 'comment', 'repair_date', 'repair_time')

    username = forms.CharField(label='Имя',
                               min_length=3,
                               max_length=20,
                               help_text='Введите Ваше имя',
                               error_messages=NAME_ERROR_LIST,
                               widget=forms.TextInput(attrs={'id': 'username_input',
                                                             'required': True,
                                                             'placeholder': 'Ваше имя...'}))
    honeypot = forms.CharField(required=False,
                               label="",
                               widget=forms.TextInput(attrs={'style': "display: None",}))
    address = forms.CharField(label='Адрес',
                              help_text='Ваш адрес',
                              error_messages='',
                              widget=forms.TextInput(attrs={'id': 'address_input',
                                                            'required': True,
                                                            'placeholder': 'Ваше имя...'}))
    telephone = forms.IntegerField(label='Телефон',
                                   required=True,
                                   help_text='Ваш номер телефона',
                                   error_messages='',
                                   widget=forms.TextInput(attrs={'id': 'telephone_input',
                                                                 'required': True,
                                                                 'placeholder': 'Ваше номер телефона...'}))
    comment = forms.CharField(label='Комментарий',
                              help_text='Введите дополнительную информацию',
                              error_messages='',
                              widget=forms.Textarea(attrs={'rows': 5,
                                                           'cols': 20,
                                                           'id': 'comment_input',
                                                           'placeholder': 'Введите дополнительную информацию...'}),
                              required=False)
    repair_date = forms.DateField(label='Дата',
                                  help_text='Выберите дату ремонта',
                                  error_messages='',
                                  widget=forms.DateInput(attrs={'type': 'Date',
                                                                'id': 'date_input'}),
                                  initial=datetime.now().date().strftime('%Y-%m-%d'))
    repair_time = forms.ChoiceField(choices=Scheduler.TimeChoice.choices(),
                                    widget=forms.RadioSelect())

    # def clean(self):
    #     cleaned_data = super(SchedulerForm, self).clean()
    #     if cleaned_data['username'] == 'JAGGER':
    #         raise ValidationError('Опять ты приперся?', code='invalid')
    #
    #     # Проверка и возврат.
    #     return cleaned_data

    # SUBJECT_ERROR_MESSAGE = 'Subject cant be named subject'
    # def clean_username(self):
    #     cleaned_data = self.cleaned_data['username']
    #     if cleaned_data == 'JAGGER':
    #         raise forms.ValidationError(self.SUBJECT_ERROR_MESSAGE)
    #     else:
    #         print('subject is clear')
    #     return self.cleaned_data['username']
