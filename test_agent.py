"""
RasaPlan Agent Tests
Basic unit tests for all agent tools.
Run with: python -m pytest tests/ -v
"""

import json
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agent.tools import (
    budget_calculator_tool,
    grocery_price_tool,
    nutrition_estimator_tool,
    recipe_generator_tool,
    weekly_planner_tool,
    meal_swap_tool,
    shopping_list_tool,
)
from agent.memory import StudentProfile


class TestBudgetCalculator:
    def test_ultra_budget(self):
        result = budget_calculator_tool.invoke("600")
        assert "ultra-budget" in result.lower() or "LKR 600" in result

    def test_budget_tier(self):
        result = budget_calculator_tool.invoke("1500")
        assert "LKR 1500" in result

    def test_comfortable_tier(self):
        result = budget_calculator_tool.invoke("5000")
        assert "comfortable" in result.lower()

    def test_daily_budget_calculation(self):
        result = budget_calculator_tool.invoke("2000")
        assert "285" in result or "286" in result  # 2000/7


class TestGroceryPrice:
    def test_find_rice(self):
        result = grocery_price_tool.invoke("rice")
        assert "LKR" in result

    def test_find_eggs(self):
        result = grocery_price_tool.invoke("eggs")
        assert "300" in result or "LKR" in result

    def test_not_found(self):
        result = grocery_price_tool.invoke("sushi")
        assert "not found" in result.lower()

    def test_find_dhal(self):
        result = grocery_price_tool.invoke("dhal")
        assert "LKR" in result


class TestNutritionEstimator:
    def test_pol_roti_nutrition(self):
        result = nutrition_estimator_tool.invoke("pol roti")
        assert "calories" in result.lower() or "Calories" in result

    def test_unknown_recipe(self):
        result = nutrition_estimator_tool.invoke("pizza")
        assert "not in database" in result.lower() or "estimated" in result.lower()


class TestRecipeGenerator:
    def test_pol_roti_recipe(self):
        result = recipe_generator_tool.invoke("Pol Roti")
        assert "flour" in result.lower() or "coconut" in result.lower()
        assert "Step" in result or "1." in result

    def test_dhal_curry_recipe(self):
        result = recipe_generator_tool.invoke("Dhal Curry")
        assert "lentil" in result.lower() or "dhal" in result.lower()

    def test_unknown_recipe(self):
        result = recipe_generator_tool.invoke("spaghetti bolognese")
        assert "not in local database" in result.lower()


class TestWeeklyPlanner:
    def test_vegetarian_beginner(self):
        input_data = json.dumps({
            "budget_lkr": 2000,
            "diet": "vegetarian",
            "skill": "beginner"
        })
        result = weekly_planner_tool.invoke(input_data)
        assert "Monday" in result
        assert "Sunday" in result
        assert "Breakfast" in result
        assert "Dinner" in result

    def test_non_veg_plan(self):
        input_data = json.dumps({
            "budget_lkr": 3000,
            "diet": "non-vegetarian",
            "skill": "intermediate"
        })
        result = weekly_planner_tool.invoke(input_data)
        assert "7-Day" in result

    def test_low_budget_plan(self):
        input_data = json.dumps({
            "budget_lkr": 700,
            "diet": "vegetarian",
            "skill": "beginner"
        })
        result = weekly_planner_tool.invoke(input_data)
        assert "Monday" in result

    def test_invalid_json_fallback(self):
        result = weekly_planner_tool.invoke("not valid json at all")
        assert "7-Day" in result  # should use defaults


class TestMealSwap:
    def test_swap_expensive(self):
        input_data = json.dumps({
            "current_meal": "Chicken Curry",
            "reason": "too_expensive",
            "budget_per_meal_lkr": 80
        })
        result = meal_swap_tool.invoke(input_data)
        assert "LKR" in result or "Swap" in result

    def test_swap_dont_like(self):
        input_data = json.dumps({
            "current_meal": "Wambatu curry",
            "reason": "dont_like",
            "budget_per_meal_lkr": 100
        })
        result = meal_swap_tool.invoke(input_data)
        assert "Swap" in result or "alternative" in result.lower()


class TestShoppingList:
    def test_basic_shopping_list(self):
        input_data = json.dumps({
            "meals": ["Pol Roti", "Dhal Curry", "Rice & Curry"],
            "budget_lkr": 2000
        })
        result = shopping_list_tool.invoke(input_data)
        assert "Shopping List" in result
        assert "LKR" in result

    def test_empty_meals_fallback(self):
        input_data = json.dumps({
            "meals": [],
            "budget_lkr": 1500
        })
        result = shopping_list_tool.invoke(input_data)
        assert "Shopping List" in result

    def test_invalid_json_fallback(self):
        result = shopping_list_tool.invoke("bad json")
        assert "Shopping List" in result


class TestStudentProfile:
    def test_default_profile(self):
        p = StudentProfile()
        assert p.budget_lkr == 2000
        assert p.diet == "vegetarian"
        assert p.skill == "beginner"

    def test_update_profile(self):
        p = StudentProfile()
        p.update(budget_lkr=3000, diet="non-vegetarian")
        assert p.budget_lkr == 3000
        assert p.diet == "non-vegetarian"

    def test_to_dict(self):
        p = StudentProfile()
        d = p.to_dict()
        assert "budget_lkr" in d
        assert "diet" in d

    def test_to_context_string(self):
        p = StudentProfile()
        s = p.to_context_string()
        assert "LKR" in s
        assert "vegetarian" in s


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
