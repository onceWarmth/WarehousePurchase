from django import forms

class PurchaseGoodsForm(forms.Form):
	username = forms.CharField()
	goodsID = forms.CharField()
	num = forms.IntegerField()