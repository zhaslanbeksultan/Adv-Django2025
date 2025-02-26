from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import HealthGoalForm, FoodForm
from .models import Food, Consume, HealthGoal


def index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/')  # Redirect to login if not authenticated

    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consume)
        consume.save()

    foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    try:
        health_goal = HealthGoal.objects.get(user=request.user)
    except HealthGoal.DoesNotExist:
        health_goal = None  # Handle case where no goal exists yet

    return render(request, 'app/index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'health_goal': health_goal
    })

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'app/delete.html')

def nutrient_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    consumed = Consume.objects.filter(user=request.user)
    try:
        goal = HealthGoal.objects.get(user=request.user)
        data = {
            'calories': sum(c.food_consumed.calories for c in consumed),
            'carbs': sum(c.food_consumed.carbs for c in consumed),
            'proteins': sum(c.food_consumed.proteins for c in consumed),
            'fats': sum(c.food_consumed.fats for c in consumed),
            'calorie_goal': goal.daily_calorie_goal,
            'carb_goal': goal.carb_goal,
            'protein_goal': goal.protein_goal,
            'fat_goal': goal.fat_goal
        }
    except HealthGoal.DoesNotExist:
        data = {
            'calories': sum(c.food_consumed.calories for c in consumed),
            'carbs': sum(c.food_consumed.carbs for c in consumed),
            'proteins': sum(c.food_consumed.proteins for c in consumed),
            'fats': sum(c.food_consumed.fats for c in consumed),
            'calorie_goal': 2000,  # Default if no goal
            'carb_goal': 50,
            'protein_goal': 50,
            'fat_goal': 50
        }
    return JsonResponse(data)

def set_health_goal(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/set-goal/')

    try:
        health_goal = HealthGoal.objects.get(user=request.user)
    except HealthGoal.DoesNotExist:
        health_goal = None

    if request.method == 'POST':
        form = HealthGoalForm(request.POST, instance=health_goal)
        if form.is_valid():
            health_goal = form.save(commit=False)
            health_goal.user = request.user
            health_goal.save()
            return redirect('/')
    else:
        form = HealthGoalForm(instance=health_goal)
    return render(request, 'app/set_goal.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "app/register.html", {"form": form})

def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the food to the global registry
            return redirect("index")  # Redirects back to the homepage
    else:
        form = FoodForm()

    return render(request, "app/add_food.html", {"form": form})


@login_required
def chart_data(request):
    consumed = Consume.objects.filter(user=request.user)

    goal, _ = HealthGoal.objects.get_or_create(user=request.user)

    data = {

        "labels": [c.food_consumed.name for c in consumed],

        "carbs": [c.food_consumed.carbs for c in consumed],

        "proteins": [c.food_consumed.proteins for c in consumed],

        "fats": [c.food_consumed.fats for c in consumed],

        "calories": [c.food_consumed.calories for c in consumed],

        "goal_carbs": goal.carb_goal,

        "goal_proteins": goal.protein_goal,

        "goal_fats": goal.fat_goal,

        "goal_calories": goal.daily_calorie_goal,

    }

    return JsonResponse(data)