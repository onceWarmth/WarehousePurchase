from django import forms

class PurchaseGoodsForm(forms.Form):
	goodsID = forms.CharField()
	num = forms.IntegerField()