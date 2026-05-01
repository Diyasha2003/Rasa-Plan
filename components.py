"""
RasaPlan Frontend Components
Custom Streamlit HTML component helpers.
"""

import streamlit as st
from streamlit.components.v1 import html as st_html
import json
import os


def render_meal_card(name: str, name_si: str, cost: int, time_min: int,
                     emoji: str, color_class: str = "gold-bg") -> str:
    """Renders a single HTML meal card string."""
    return f"""
    <div style="
        background:white; border-radius:16px; overflow:hidden;
        box-shadow:0 8px 25px rgba(0,0,0,0.1); transition:transform 0.3s;
        cursor:pointer;
    " onmouseover="this.style.transform='translateY(-6px)'"
       onmouseout="this.style.transform='translateY(0)'">
        <div style="
            height:140px; display:flex; align-items:center;
            justify-content:center; font-size:4rem;
            background:{'linear-gradient(135deg,#F5C842,#f0b020)' if color_class == 'gold-bg'
                        else 'linear-gradient(135deg,#1C2C6B,#2a4090)'};
            position:relative;
        ">{emoji}</div>
        <div style="padding:1rem;">
            <h4 style="color:#1C2C6B;margin:0 0 2px;font-size:0.95rem">{name}</h4>
            <p style="color:#999;font-size:0.75rem;margin:0 0 8px;
                      font-family:'DM Mono',monospace">{name_si}</p>
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="color:#F5C842;font-weight:700;font-size:1rem">
                    LKR {cost//2}<small style="color:#999;font-weight:400">/serving</small>
                </span>
                <span style="color:#999;font-size:0.75rem;font-family:'DM Mono',monospace">
                    ⏱ {time_min} min
                </span>
            </div>
        </div>
    </div>
    """


def render_week_grid(plan: list) -> str:
    """
    Renders the weekly meal plan as an HTML grid.
    plan: list of 7 dicts with keys: day, breakfast, lunch, dinner
    """
    days_html = ""
    for day_data in plan:
        days_html += f"""
        <div style="
            background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
            border-radius:12px; overflow:hidden; min-width:120px;
        ">
            <div style="
                padding:8px; text-align:center;
                font-family:'DM Mono',monospace; font-size:0.68rem;
                letter-spacing:1px; color:#F5C842;
                border-bottom:1px solid rgba(255,255,255,0.06);
            ">{day_data['day']}</div>
            <div style="padding:8px;border-bottom:1px solid rgba(255,255,255,0.04)">
                <div style="font-size:0.6rem;color:#F5C842;font-family:'DM Mono',monospace;margin-bottom:4px">☀️ BF</div>
                <div style="font-size:0.75rem;color:white;font-weight:600">{day_data['breakfast']}</div>
                <div style="font-size:0.65rem;color:rgba(255,255,255,0.35)">LKR {day_data.get('bf_cost',40)}</div>
            </div>
            <div style="padding:8px;border-bottom:1px solid rgba(255,255,255,0.04)">
                <div style="font-size:0.6rem;color:#79f2b0;font-family:'DM Mono',monospace;margin-bottom:4px">🌤 LU</div>
                <div style="font-size:0.75rem;color:white;font-weight:600">{day_data['lunch']}</div>
                <div style="font-size:0.65rem;color:rgba(255,255,255,0.35)">LKR {day_data.get('lu_cost',60)}</div>
            </div>
            <div style="padding:8px">
                <div style="font-size:0.6rem;color:#9db8ff;font-family:'DM Mono',monospace;margin-bottom:4px">🌙 DI</div>
                <div style="font-size:0.75rem;color:white;font-weight:600">{day_data['dinner']}</div>
                <div style="font-size:0.65rem;color:rgba(255,255,255,0.35)">LKR {day_data.get('di_cost',50)}</div>
            </div>
        </div>
        """

    return f"""
    <div style="
        display:grid;
        grid-template-columns:repeat(7,1fr);
        gap:0.75rem;
        background:#0d0d1a;
        padding:1.5rem;
        border-radius:16px;
        font-family:'Syne',sans-serif;
    ">
        {days_html}
    </div>
    """


def render_thinking_animation() -> str:
    """Returns HTML for the AI thinking animation."""
    return """
    <div style="
        display:flex; align-items:center; gap:12px;
        padding:1rem 1.25rem;
        background:rgba(245,200,66,0.06);
        border:1px solid rgba(245,200,66,0.15);
        border-radius:12px; margin-bottom:8px;
        font-family:'DM Mono',monospace; font-size:0.8rem;
        color:rgba(255,255,255,0.6);
    ">
        <span>🧠 RasaPlan is thinking</span>
        <span style="display:flex;gap:4px">
            <span style="display:inline-block;width:8px;height:8px;background:#F5C842;
                  border-radius:50%;animation:bounce 1.2s infinite">
            </span>
            <span style="display:inline-block;width:8px;height:8px;background:#F5C842;
                  border-radius:50%;animation:bounce 1.2s 0.2s infinite">
            </span>
            <span style="display:inline-block;width:8px;height:8px;background:#F5C842;
                  border-radius:50%;animation:bounce 1.2s 0.4s infinite">
            </span>
        </span>
        <style>
            @keyframes bounce {
                0%,80%,100% { transform:scale(0.5); opacity:0.3; }
                40% { transform:scale(1); opacity:1; }
            }
        </style>
    </div>
    """


def render_shopping_list(items: dict, budget: int, total: int) -> str:
    """
    Renders an interactive shopping list.
    items: dict of category -> list of (name, price) tuples
    """
    remaining = budget - total
    groups_html = ""
    for cat, item_list in items.items():
        items_html = "".join([
            f"""<div onclick="this.classList.toggle('checked');
                    this.querySelector('.cb').textContent=this.classList.contains('checked')?'✓':'';"
                style="display:flex;align-items:center;gap:10px;padding:6px 0;
                       border-bottom:1px solid rgba(255,255,255,0.04);cursor:pointer">
                <div class="cb" style="width:18px;height:18px;border:2px solid rgba(255,255,255,0.2);
                     border-radius:4px;display:flex;align-items:center;justify-content:center;
                     font-size:0.7rem;color:#F5C842;flex-shrink:0;"></div>
                <span style="font-size:0.85rem;color:rgba(255,255,255,0.8)">{it[0]}</span>
                <span style="margin-left:auto;font-size:0.75rem;font-family:'DM Mono',monospace;
                      color:#F5C842">LKR {it[1]}</span>
            </div>"""
            for it in item_list
        ])
        groups_html += f"""
        <div style="margin-bottom:1.25rem">
            <div style="font-family:'DM Mono',monospace;font-size:0.72rem;
                  letter-spacing:2px;text-transform:uppercase;
                  color:rgba(255,255,255,0.4);margin-bottom:8px">{cat}</div>
            {items_html}
        </div>"""

    color = "#F5C842" if remaining >= 0 else "#dc3545"
    sign  = "+" if remaining >= 0 else ""

    return f"""
    <div style="
        background:#0d0d1a; border:1px solid rgba(255,255,255,0.08);
        border-radius:16px; padding:1.5rem;
        font-family:'Syne',sans-serif; color:white;
    ">
        <h4 style="color:#F5C842;margin-bottom:1.25rem">🛒 Your Shopping List</h4>
        {groups_html}
        <div style="display:flex;justify-content:space-between;align-items:center;
             padding-top:1rem;border-top:1px solid rgba(255,255,255,0.1);">
            <span style="font-family:'DM Mono',monospace;font-size:0.8rem;
                  color:rgba(255,255,255,0.5)">Estimated total:</span>
            <strong style="color:#F5C842;font-size:1.1rem">LKR {total:,}</strong>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
            <span style="font-family:'DM Mono',monospace;font-size:0.8rem;
                  color:rgba(255,255,255,0.5)">Remaining budget:</span>
            <strong style="color:{color};font-size:1rem">{sign}LKR {abs(remaining):,}</strong>
        </div>
    </div>
    """
