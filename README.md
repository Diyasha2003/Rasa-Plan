# 🍛 RasaPlan | රස Plan
### The Broke Student Sri Lankan Meal Planner — AI Agent

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.16-1C3C3C?style=for-the-badge)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/GPT--4o-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **"Rasai, beli, and healthy!"** — Eat delicious Sri Lankan food without breaking the bank.  
> Built for **LB3114 Data Science Applications & AI** · KDU · Intake 41

---

## 🎬 Demo

> 📹 **YouTube Short Demo**: [Watch on YouTube](#) *(link after submission)*

![RasaPlan Demo](docs/demo.gif) *(add your screen recording here)*

---

## 🧩 Problem Statement

University students in Sri Lanka face a daily challenge: **eating nutritious meals on extremely tight budgets**. With food prices rising (rice up 15%, vegetables fluctuating), and most students having no cooking plan, they default to expensive takeaway or nutritionally poor instant noodles.

**RasaPlan solves this** by providing an AI-powered 7-day meal planner that:
- Works with budgets as low as **LKR 500/week**
- Uses **real 2025 market prices** from Keells, Arpico, Cargills and local Pola markets
- Plans traditional Sri Lankan meals students already know and love
- Generates shopping lists, recipes, and nutrition summaries

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RASAPLAN AGENT                        │
│                                                         │
│  ┌──────────┐    ┌────────────────────────────────┐     │
│  │  User    │───▶│   Streamlit Frontend            │     │
│  │  Input   │    │   (3D Motion Graphic UI)        │     │
│  └──────────┘    └──────────────┬─────────────────┘     │
│                                 │                        │
│                  ┌──────────────▼─────────────────┐     │
│                  │   LangChain ReAct Agent         │     │
│                  │   (GPT-4o backbone)             │     │
│                  └──────────────┬─────────────────┘     │
│                                 │                        │
│         ┌───────────────────────┼───────────────────┐   │
│         │                       │                   │   │
│  ┌──────▼──────┐  ┌─────────────▼───┐  ┌───────────▼─┐ │
│  │   TOOLS     │  │    MEMORY       │  │  PLANNING   │ │
│  │ 7 custom    │  │ Buffer Window   │  │ Chain-of-   │ │
│  │ tools       │  │ Memory (k=10)   │  │ Thought     │ │
│  └─────────────┘  └─────────────────┘  └─────────────┘ │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │               DATA LAYER                        │   │
│  │  groceries_sl.json · recipes_sl.json · nutrition│   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Framework | LangChain ReAct Agent |
| LLM | OpenAI GPT-4o |
| Memory | ConversationBufferWindowMemory |
| Frontend | Streamlit + custom HTML/CSS/JS |
| Motion Graphics | GSAP, CSS 3D Transforms, Canvas Particles |
| Data | Local JSON (50+ Sri Lankan ingredients, LKR prices) |
| Testing | pytest |
| Language | Python 3.10+ |

---

## 🤖 Agent Tools

| Tool | Description |
|------|-------------|
| `budget_calculator_tool` | Analyses weekly budget, calculates per-meal limits, determines tier |
| `grocery_price_tool` | Looks up real LKR prices for 50+ Sri Lankan ingredients |
| `nutrition_estimator_tool` | Estimates calories, protein, carbs, fat per recipe |
| `recipe_generator_tool` | Full step-by-step recipes in English + Sinhala names |
| `weekly_planner_tool` | Creates 7-day breakfast/lunch/dinner/snack plan within budget |
| `meal_swap_tool` | Suggests budget-friendly alternatives to any meal |
| `shopping_list_tool` | Generates organised shopping list grouped by category with totals |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/rasaplan-agent.git
cd rasaplan-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key

# 5. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📱 Using the App

1. **Enter API Key** — Add your OpenAI API key (used only in session)
2. **Set Budget** — Use the LKR slider to set your weekly budget (LKR 500–10,000)
3. **Choose Diet** — Vegetarian, Non-Vegetarian, or Vegan
4. **Cooking Skill** — Beginner or Intermediate
5. **Select Store** — Keells, Arpico, Cargills or Pola Market
6. **Generate Plan** — AI creates your full 7-day meal plan
7. **Chat & Adjust** — Ask for swaps, recipes, shopping lists, nutrition info

### Example Queries
```
"Plan my full week for LKR 2000"
"Swap Tuesday's dinner — I don't like brinjal"
"Show me the Pol Roti recipe step by step"
"Am I within budget this week?"
"Generate my shopping list for Keells"
"What are the nutritional values of my meals?"
"Add more protein to my plan"
```

---

## 🧪 Running Tests

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run specific test class
python -m pytest tests/test_agent.py::TestBudgetCalculator -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=agent --cov-report=html
```

---

## 📁 Project Structure

```
rasaplan-agent/
├── README.md                    ← You are here
├── requirements.txt             ← Python dependencies
├── .env.example                 ← Environment template
├── app.py                       ← Main Streamlit app + 3D hero UI
├── agent/
│   ├── __init__.py
│   ├── meal_agent.py            ← LangChain ReAct agent setup
│   ├── tools.py                 ← 7 custom agent tools
│   ├── memory.py                ← ConversationBufferWindowMemory + StudentProfile
│   └── prompts.py               ← System prompts & few-shot examples
├── data/
│   ├── groceries_sl.json        ← 50+ SL ingredients + LKR prices (2025)
│   ├── recipes_sl.json          ← 10+ traditional SL recipes
│   └── nutrition.json           ← Nutritional data per 100g
└── tests/
    └── test_agent.py            ← 25+ unit tests for all tools
```

---

## 🍛 Sample Meal Plan (LKR 2000/week)

| Day | Breakfast | Lunch | Dinner |
|-----|-----------|-------|--------|
| Monday | Pol Roti (LKR 28) | Rice + Dhal Curry (LKR 40) | Egg Roti (LKR 45) |
| Tuesday | String Hoppers (LKR 35) | Mackerel Curry + Rice (LKR 55) | Gotukola Salad + Roti (LKR 30) |
| Wednesday | Pol Roti (LKR 28) | Rice + Carrot Curry (LKR 38) | Dhal + Bread (LKR 35) |
| Thursday | Bread + Egg (LKR 42) | Rice + Wambatu (LKR 42) | Instant Noodles SL Style (LKR 60) |
| Friday | String Hoppers (LKR 35) | Rice + Dhal + Pol Sambol (LKR 45) | Egg Curry (LKR 50) |
| Saturday | Pol Roti (LKR 28) | Rice + Gotukola Sambol (LKR 35) | Dhal + Rice (LKR 40) |
| Sunday | Bread + Egg (LKR 42) | Full Rice & Curry (LKR 60) | Pol Roti + Sambol (LKR 35) |
| **Total** | | | **≈ LKR 788** |

*Remaining LKR 1,212 goes toward buying bulk ingredients upfront.*

---

## ⚠️ Known Limitations

- Requires an OpenAI API key (costs money per API call)
- Recipe database is curated (10 recipes) — AI generates variations beyond these
- Prices are approximate 2025 averages and may vary by region/season
- No real-time price API — uses pre-built JSON database
- Drag-and-drop meal swapping requires future enhancement

## 🔮 Future Improvements

- [ ] Real-time price scraping from Keells/Arpico websites
- [ ] Meal photo generation using DALL-E
- [ ] Nutritional goal tracking over time
- [ ] WhatsApp integration for daily meal reminders
- [ ] Offline mode with cached meal plans
- [ ] Multi-language support (Tamil, Sinhala UI)
- [ ] Calorie tracking dashboard

---

## 📚 References

- LangChain Documentation: https://python.langchain.com/docs/
- OpenAI API Documentation: https://platform.openai.com/docs/
- Streamlit Documentation: https://docs.streamlit.io/
- Sri Lankan Food Nutrition Data: Sri Lanka Food Composition Tables (MRI)
- Market Prices: Colombo Consumer Price Index 2025

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🔗 Youtube Link

https://youtube.com/shorts/2hMoHOJSKrs?feature=shared

*Built with ❤️ and 🍛 for LB3114 Data Science Applications & AI · General Sir John Kotelawala Defence University · Intake 41*
