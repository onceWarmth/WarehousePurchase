from django import forms

class ChangeGoodsForm(forms.Form):
	goodsID = forms.CharField()
	name = forms.CharField()
	amount = forms.IntegerField()
	price = forms.FloatField()
	purchasePrice = forms.FloatField()
	kind = forms.CharField()