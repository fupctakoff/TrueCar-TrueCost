from django import forms

from auction.models import Car, Manufacturer

#в разработке
class NameForm(forms.ModelForm):
    CHOICES = []
    manufacturers_queryset = Manufacturer.objects.all()
    cnt = 0
    for i in manufacturers_queryset:
        CHOICES.append((cnt, i.name))
        cnt+=1

    manufacturer = forms.CharField(widget=forms.Select(choices=CHOICES))

    class Meta:
        model = Car
        fields = ['manufacturer', 'car_model', 'release_date', 'mileage', 'sell_price']

# class NameForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)
