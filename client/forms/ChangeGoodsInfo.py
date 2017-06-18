from django import forms

class ChangeGoodsForm(forms.Form):
	goodsID = forms.CharField()
	name = forms.CharField(required=False)
	amount = forms.IntegerField(required=False)
	price = forms.FloatField(required=False)
	purchasePrice = forms.FloatField(required=False)
	kind = forms.CharField(required=False)