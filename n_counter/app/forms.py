
from django import forms
from .models import HealthGoal, Food


class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['daily_calorie_goal', 'carb_goal', 'protein_goal', 'fat_goal']
        widgets = {
            'daily_calorie_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'carb_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat_goal': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ["name", "carbs", "proteins", "fats", "calories"]