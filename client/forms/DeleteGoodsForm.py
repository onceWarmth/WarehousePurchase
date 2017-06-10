from django import forms

class DeleteGoodsForm(forms.Form):
	goodsID = forms.CharField()
