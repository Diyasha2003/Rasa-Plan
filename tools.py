"""
RasaPlan Agent Tools
All custom LangChain tools for the Sri Lankan meal planning agent.
"""

import json
import os
import random
from typing import Optional
from langchain.tools import tool

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _load_groceries():
    with open(os.path.join(DATA_DIR, "groceries_sl.json"), "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = []
    for category, products in raw.items():
        items.extend(products)
    return items


def _load_recipes():
    with open(os.path.join(DATA_DIR, "recipes_sl.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["recipes"]


def _load_nutrition():
    with open(os.path.join(DATA_DIR, "nutrition.json"), "r", encoding="utf-8") as f:
        return json.load(f)


@tool
def budget_calculator_tool(budget_lkr: int) -> str:
    """
    Calculates what meals and groceries are achievable within a weekly budget in LKR.
    Input: weekly budget in LKR (integer).
    Returns: summary of affordable meal categories and spending breakdown.
    """
    daily_budget = budget_lkr / 7
    meal_budget = daily_budget / 3  # per meal

    if budget_lkr < 700:
        tier = "ultra-budget"
        description = "Very tight — rice, dhal, eggs and vegetables only. No meat."
        feasible_meals = ["Dhal Curry + Rice", "Pol Roti", "Egg Roti", "Gotukola Sambol"]
    elif budget_lkr < 1500:
        tier = "budget"
        description = "Good budget — rice meals, eggs, canned fish, basic curries."
        feasible_meals = ["Rice & Curry", "Dhal Curry", "Mackerel Curry", "Egg dishes", "String Hoppers"]
    elif budget_lkr < 3000:
        tier = "moderate"
        description = "Comfortable — all meals possible, occasional chicken, variety."
        feasible_meals = ["All rice dishes", "Chicken curry", "Fish curries", "Kottu Roti", "Hoppers"]
    else:
        tier = "comfortable"
        description = "Great budget — full variety including meat, fresh produce, snacks."
        feasible_meals = ["Full Sri Lankan spread", "Chicken dishes", "Seafood", "Desserts", "Snacks"]

    return (
        f"📊 Budget Analysis for LKR {budget_lkr}/week\n"
        f"• Daily budget: LKR {daily_budget:.0f}\n"
        f"• Per meal budget: LKR {meal_budget:.0f}\n"
        f"• Tier: {tier.upper()}\n"
        f"• {description}\n"
        f"• Recommended meals: {', '.join(feasible_meals)}"
    )


@tool
def grocery_price_tool(ingredient_name: str) -> str:
    """
    Looks up the current price of a Sri Lankan grocery item in LKR.
    Input: ingredient name (string).
    Returns: price, unit and store availability.
    """
    groceries = _load_groceries()
    ingredient_lower = ingredient_name.lower()

    matches = [
        g for g in groceries
        if ingredient_lower in g["name"].lower() or g["name"].lower() in ingredient_lower
    ]

    if not matches:
        return f"Item '{ingredient_name}' not found in database. Try common SL ingredients."

    results = []
    for item in matches[:3]:
        results.append(
            f"• {item['emoji']} {item['name']} ({item['unit']}): LKR {item['price_lkr']}"
        )

    return "🛒 Price Lookup Results:\n" + "\n".join(results)


@tool
def nutrition_estimator_tool(recipe_name: str) -> str:
    """
    Estimates the nutritional content of a Sri Lankan recipe or meal.
    Input: recipe name (string).
    Returns: calories, protein, carbs, fat per serving.
    """
    recipes = _load_recipes()
    recipe_lower = recipe_name.lower()

    match = next(
        (r for r in recipes if recipe_lower in r["name"].lower() or r["id"] in recipe_lower),
        None
    )

    if not match:
        return (
            f"Recipe '{recipe_name}' not in database. "
            f"Estimated average Sri Lankan meal: ~350-450 calories, 12-20g protein."
        )

    cal = match.get("calories", "N/A")
    return (
        f"🥗 Nutrition for {match['name']} (per serving):\n"
        f"• Calories: ~{cal} kcal\n"
        f"• Diet type: {', '.join(match['diet'])}\n"
        f"• Prep time: {match['time_min']} minutes\n"
        f"• Cost per serving: LKR {match['cost_lkr'] // match['servings']}"
    )


@tool
def recipe_generator_tool(meal_name: str) -> str:
    """
    Generates a step-by-step recipe for a Sri Lankan meal.
    Input: meal name (string).
    Returns: full recipe with ingredients, steps and cost.
    """
    recipes = _load_recipes()
    recipe_lower = meal_name.lower()

    match = next(
        (r for r in recipes if recipe_lower in r["name"].lower() or r["id"] in recipe_lower),
        None
    )

    if not match:
        return (
            f"Recipe for '{meal_name}' not in local database. "
            f"The AI will generate one based on Sri Lankan cooking traditions."
        )

    ingredients_str = "\n".join(
        [f"  • {i['item']}: {i['quantity']} (~LKR {i['cost']})" for i in match["ingredients"]]
    )
    steps_str = "\n".join([f"  {i+1}. {s}" for i, s in enumerate(match["steps"])])

    return (
        f"👨‍🍳 Recipe: {match['name']} ({match['name_si']})\n"
        f"⏱️ Time: {match['time_min']} mins | Serves: {match['servings']} | "
        f"Cost: LKR {match['cost_lkr']}\n\n"
        f"📦 Ingredients:\n{ingredients_str}\n\n"
        f"📝 Steps:\n{steps_str}"
    )


@tool
def weekly_planner_tool(input_data: str) -> str:
    """
    Creates a 7-day meal plan within a budget. 
    Input: JSON string with keys: budget_lkr (int), diet (str: vegetarian/non-vegetarian), skill (str: beginner/intermediate).
    Returns: complete 7-day meal plan with daily costs.
    """
    try:
        data = json.loads(input_data)
        budget = int(data.get("budget_lkr", 2000))
        diet = data.get("diet", "vegetarian").lower()
        skill = data.get("skill", "beginner").lower()
    except (json.JSONDecodeError, ValueError):
        budget = 2000
        diet = "vegetarian"
        skill = "beginner"

    recipes = _load_recipes()

    # Filter by diet and skill
    filtered = [
        r for r in recipes
        if (diet == "non-vegetarian" or "vegetarian" in r["diet"] or "vegan" in r["diet"])
        and (skill == "intermediate" or r["difficulty"] == "beginner")
    ]

    breakfast_options = [r for r in filtered if r["category"] == "breakfast"]
    lunch_options = [r for r in filtered if r["category"] == "lunch"]
    dinner_options = [r for r in filtered if r["category"] == "dinner"]
    side_options = [r for r in filtered if r["category"] == "side"]

    # Fallback defaults
    if not breakfast_options:
        breakfast_options = [r for r in recipes if r["category"] == "breakfast"]
    if not lunch_options:
        lunch_options = [r for r in recipes if r["category"] == "lunch"]
    if not dinner_options:
        dinner_options = [r for r in recipes if r["category"] == "dinner"]

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = []
    total_cost = 0

    for day in days:
        bf = random.choice(breakfast_options)
        lu = random.choice(lunch_options)
        di = random.choice(dinner_options)
        side = random.choice(side_options) if side_options else None

        day_cost = (bf["cost_lkr"] // bf["servings"]) + \
                   (lu["cost_lkr"] // lu["servings"]) + \
                   (di["cost_lkr"] // di["servings"])
        if side:
            day_cost += (side["cost_lkr"] // side["servings"])

        total_cost += day_cost
        side_str = f" + {side['emoji']} {side['name']}" if side else ""
        plan.append(
            f"📅 {day} (LKR {day_cost})\n"
            f"  🌅 Breakfast: {bf['emoji']} {bf['name']}\n"
            f"  ☀️  Lunch: {lu['emoji']} {lu['name']}\n"
            f"  🌙 Dinner: {di['emoji']} {di['name']}{side_str}"
        )

    remaining = budget - total_cost
    status = "✅ Within budget!" if remaining >= 0 else "⚠️ Slightly over budget"

    return (
        f"🗓️ 7-Day Sri Lankan Meal Plan\n"
        f"Budget: LKR {budget} | Total Cost: LKR {total_cost} | {status}\n"
        f"Remaining: LKR {max(0, remaining)}\n\n"
        + "\n\n".join(plan)
    )


@tool
def meal_swap_tool(input_data: str) -> str:
    """
    Suggests a budget-friendly alternative meal swap.
    Input: JSON string with keys: current_meal (str), reason (str: too_expensive/dont_like/dietary), budget_per_meal_lkr (int).
    Returns: 2-3 alternative meal suggestions.
    """
    try:
        data = json.loads(input_data)
        current = data.get("current_meal", "")
        reason = data.get("reason", "dont_like")
        meal_budget = int(data.get("budget_per_meal_lkr", 100))
    except (json.JSONDecodeError, ValueError):
        current = ""
        reason = "dont_like"
        meal_budget = 100

    recipes = _load_recipes()
    affordable = [
        r for r in recipes
        if (r["cost_lkr"] // r["servings"]) <= meal_budget
        and r["name"].lower() != current.lower()
    ]

    if not affordable:
        affordable = recipes[:5]

    suggestions = random.sample(affordable, min(3, len(affordable)))
    lines = [
        f"• {r['emoji']} {r['name']} — LKR {r['cost_lkr'] // r['servings']}/serving, {r['time_min']} mins"
        for r in suggestions
    ]

    return (
        f"🔄 Meal Swap Suggestions (replacing: {current or 'current meal'})\n"
        f"Reason: {reason.replace('_', ' ')}\n\n"
        + "\n".join(lines)
    )


@tool
def shopping_list_tool(input_data: str) -> str:
    """
    Generates an organized shopping list from a meal plan.
    Input: JSON string with keys: meals (list of meal names), budget_lkr (int).
    Returns: grouped shopping list with estimated total cost.
    """
    try:
        data = json.loads(input_data)
        meals = data.get("meals", [])
        budget = int(data.get("budget_lkr", 2000))
    except (json.JSONDecodeError, ValueError):
        meals = []
        budget = 2000

    recipes = _load_recipes()
    groceries = _load_groceries()

    all_ingredients = {}
    for meal_name in meals:
        match = next(
            (r for r in recipes if meal_name.lower() in r["name"].lower()),
            None
        )
        if match:
            for ing in match["ingredients"]:
                name = ing["item"]
                if name not in all_ingredients:
                    all_ingredients[name] = {"quantity": ing["quantity"], "cost": ing["cost"]}
                else:
                    all_ingredients[name]["cost"] += ing["cost"]

    # Group by category
    categories = {"🥬 Produce": [], "🌾 Dry Goods": [], "🐟 Protein": [], "🫙 Spices": [], "🥛 Other": []}

    for name, details in all_ingredients.items():
        grocery = next((g for g in groceries if name.lower() in g["name"].lower()), None)
        cat = grocery["category"] if grocery else "other"
        line = f"• {name}: {details['quantity']} (~LKR {details['cost']})"

        if cat == "vegetables":
            categories["🥬 Produce"].append(line)
        elif cat in ["staples"]:
            categories["🌾 Dry Goods"].append(line)
        elif cat == "protein":
            categories["🐟 Protein"].append(line)
        elif cat == "spices":
            categories["🫙 Spices"].append(line)
        else:
            categories["🥛 Other"].append(line)

    total_est = sum(d["cost"] for d in all_ingredients.values())
    list_str = ""
    for cat, items in categories.items():
        if items:
            list_str += f"\n{cat}\n" + "\n".join(items) + "\n"

    if not list_str:
        list_str = "\n(No specific meals matched — showing general weekly essentials)\n"
        list_str += "• Rice 2kg — LKR 380\n• Dhal 500g — LKR 165\n• Eggs 10pk — LKR 300\n"
        list_str += "• Coconut x3 — LKR 300\n• Mixed vegetables — LKR 300\n"
        total_est = 1445

    return (
        f"🛒 Shopping List\n"
        f"Budget: LKR {budget} | Estimated cost: LKR {total_est}\n"
        f"Remaining: LKR {max(0, budget - total_est)}"
        + list_str
    )
