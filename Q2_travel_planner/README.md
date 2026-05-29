# Travel Planner System
This repository contains the implementation of a knowledge based AI travel planner that generates personalized vacation recommendations. 
## Problem statement:
*"Design an AI based Travel Planner that reuses the Existing Knowledge bases in the domain (Eg. Wine ontology, Tourist Places, Food Recommendation; Personalised Tour Plans; Cost assessment, etc.)"*
## File Structure
The project is divided into 2 distinct files:
* `knowledge_base.py`: Contains the structured ontology and domain knowledge, including tourist destinations, food and wine mappings, dietary flags at the dish level, destination-specific accommodation costs, and regional transport rates.
* `travel_planner.py`: The main execution script containing the `UserProfile`, the `TravelPlanner` logic (scoring, filtering, cost estimation), and the interactive command-line interface.
---
## How the Code Works
### 1. User Profiling
The script begins by collecting dynamic inputs via the CLI (name, budget, interests, duration, travel month, dietary restrictions, and accommodation preference). These are instantiated into a `UserProfile` object which acts as the core state constraint for the algorithm.

### 2. Cost Estimation (`estimate_cost`)
Before any scoring happens, the AI calculates the actual total cost of visiting a destination. It pulls regional flight rates, multiplies them by the destination's average travel hours, and adds local transit, food, activities, and destination-specific accommodation costs. This yields a highly accurate `actual_per_day` cost.

### 3. Hard Pruning & Intelligent Scoring (`recommend_destinations`)
The system iterates through all available destinations in the knowledge base:
* **The 1.5x Budget Filter:** Any destination where the estimated daily cost exceeds 150% of the user's stated budget is immediately pruned (skipped) to prevent unrealistic recommendations.
* **Scoring Algorithm:** Surviving destinations are assigned a score based on a weighted formula:
  * Interest Match: +20 points per matching tag.
  * Seasonality: +15 points if traveling during the destination's best months.
  * Safety: +5 points per star.
  * Budget Adherence: +25 points if fully under budget, +10 if within a 30% margin, and -25 if severely over budget.

### 4. Ontology-Based Dietary Filtering (`get_food_recommendations`)
For the top ranked destinations, the planner looks up the local cuisine. It then iterates through the dish level ontology in the knowledge base, cross referencing the user's restrictions (e.g., vegetarian, gluten free) against the specific boolean flags of each dish. Only compliant dishes are appended to the final output.

### 5. Dynamic Itinerary Generation (`build_itinerary`)
The system constructs a day by day plan mapping the trip duration. It initializes a `used = set()` to track attractions. Day 1 is hardcoded for arrival, the final day for departure, and the intermediate days dynamically pull unused attractions from the knowledge base. If the trip is longer than the available attractions, the system intelligently defaults to "Free exploration" to prevent repetitions.

---
## How to Run the Code
Open your terminal and clone this repository to your local machine using the following command:
```bash
git clone https://github.com/m-o-n-i-sh/se24ucse153_AI_programing_assignment_5.git
```
Move into the cloned directory:
```bash
cd se24ucse153_AI_programing_assignment_5/Q2_travel_planner
```
Run the script:
```bash
python travel_planner.py

```
