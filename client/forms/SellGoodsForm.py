from django import forms

class SellGoodsForm(forms.Form):
	goodsID = forms.CharField()
	num = forms.IntegerField()