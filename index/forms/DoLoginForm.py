from django import forms

class DoLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()