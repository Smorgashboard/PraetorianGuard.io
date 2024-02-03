from django import forms


##### I havent fleshed this out... it mgiht be better to do the html form....  
class AddPhishingCampaign(forms.Form):
    campaign_nam = forms.CharField(max_length=32)