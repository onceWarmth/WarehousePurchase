from django import forms

class AddGoodsForm(forms.Form):
	name = forms.CharField()
	amount = forms.IntegerField()
	price = forms.FloatField()
	purchasePrice = forms.FloatField()
	kind = forms.CharField()