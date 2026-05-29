from knowledge_base import (
    TOURIST_PLACES, FOOD_RECOMMENDATIONS, WINE_ONTOLOGY,
    ACCOMMODATION_COSTS, TRANSPORT_COSTS, CITY_TO_CUISINE_MAP
)
class UserProfile:
    def __init__(self, name, budget_per_day_inr, interests, duration_days,
                 travel_month, dietary_restrictions=None, accommodation_pref="mid_range"):
        self.name = name
        self.budget_per_day_inr = budget_per_day_inr
        self.interests = interests
        self.duration_days = duration_days
        self.travel_month = travel_month
        self.dietary_restrictions = dietary_restrictions or []
        self.accommodation_pref = accommodation_pref
    def __repr__(self):
        return (f"UserProfile(name={self.name}, budget={self.budget_per_day_inr}/day, "
                f"interests={self.interests}, days={self.duration_days})")
class TravelPlanner:
    def __init__(self):
        self.places = TOURIST_PLACES
        self.foods = FOOD_RECOMMENDATIONS
        self.wines = WINE_ONTOLOGY
        self.accommodation_costs = ACCOMMODATION_COSTS
        self.transport = TRANSPORT_COSTS
    def estimate_cost(self, place_name, profile):
        place = self.places[place_name]
        region = place["region"]
        transport_info = self.transport.get(region, self.transport["Europe"])
        daily_living = place["avg_daily_cost_inr"]
        accom_cost_per_night = self.accommodation_costs[place_name].get(
            profile.accommodation_pref, 5000
        )
        hours = transport_info.get("avg_travel_hours", 10)
        flight_estimate = transport_info["flight_per_hour"] * hours
        local_transport = transport_info["local_daily"] * profile.duration_days
        food_cost = daily_living * 0.4 * profile.duration_days
        activity_cost = daily_living * 0.3 * profile.duration_days
        accommodation_total = accom_cost_per_night * profile.duration_days
        total = (
            flight_estimate
            + local_transport
            + food_cost
            + activity_cost
            + accommodation_total
        )
        return {
            "flight_estimate_inr": round(flight_estimate, 2),
            "accommodation_total_inr": round(accommodation_total, 2),
            "food_total_inr": round(food_cost, 2),
            "activities_total_inr": round(activity_cost, 2),
            "local_transport_total_inr": round(local_transport, 2),
            "grand_total_inr": round(total, 2),
            "per_day_inr": round(total / profile.duration_days, 2),
        }
    def score_destination(self, place_name, profile, actual_per_day):
        place = self.places[place_name]
        score = 0.0
        interest_matches = sum(
            1 for tag in profile.interests if tag in place["tags"]
        )
        score += interest_matches * 20
        if profile.travel_month in place["best_months"]:
            score += 15
        score += place["safety_rating"] * 5
        budget = profile.budget_per_day_inr
        if actual_per_day <= budget:
            score += 25
        elif actual_per_day <= budget * 1.3:
            score += 10
        else:
            score -= 25
        return round(score, 2)
    def recommend_destinations(self, profile, top_n=3):
        scored = []
        for name in self.places:
            cost_details = self.estimate_cost(name, profile)
            actual_per_day = cost_details["per_day_inr"]
            if actual_per_day > profile.budget_per_day_inr * 1.5:
                continue
            s = self.score_destination(name, profile, actual_per_day)
            scored.append((name, s))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_n]
    def get_food_recommendations(self, place_name, profile):
        cuisine = CITY_TO_CUISINE_MAP.get(place_name)
        if not cuisine or cuisine not in self.foods:
            return None
        food_info = self.foods[cuisine]
        all_dishes = food_info["dishes"]
        filtered_dishes = []
        for dish in all_dishes:
            suitable = True
            for restriction in profile.dietary_restrictions:
                if not dish["dietary"].get(restriction, True):
                    suitable = False
                    break
            if suitable:
                filtered_dishes.append(dish["name"])
        return {
            "cuisine": cuisine,
            "dishes": filtered_dishes,
            "wine_pairing": food_info.get("wine_pairing", []),
            "suitable_for_dietary": len(filtered_dishes) > 0,
        }
    def get_wine_recommendations(self, place_name):
        cuisine = CITY_TO_CUISINE_MAP.get(place_name)
        if not cuisine:
            return []
        food = self.foods.get(cuisine, {})
        wine_names = food.get("wine_pairing", [])
        result = []
        for wname in wine_names:
            if wname in self.wines:
                result.append((wname, self.wines[wname]))
        return result
    def build_itinerary(self, place_name, profile):
        place = self.places[place_name]
        attractions = place["attractions"]
        days = profile.duration_days
        itinerary = {}
        used = set()
        for day in range(1, days + 1):
            if day == 1:
                first_attraction = attractions[0] if attractions else "City walk"
                if attractions:
                    used.add(first_attraction)
                itinerary[f"Day {day}"] = {
                    "theme": "Arrival & Orientation",
                    "activities": [
                        f"Arrive and check into {profile.accommodation_pref.replace('_', ' ')} accommodation",
                        "Explore the neighbourhood around your stay",
                        first_attraction,
                    ],
                    "meal": f"Welcome dinner: try local {CITY_TO_CUISINE_MAP.get(place_name, 'local')} cuisine",
                }
            elif day == days:
                itinerary[f"Day {day}"] = {
                    "theme": "Farewell Day",
                    "activities": [
                        "Morning leisure & souvenir shopping",
                        "Check out and pack",
                        "Departure",
                    ],
                    "meal": "Farewell breakfast at a local café",
                }
            else:
                available = [a for a in attractions if a not in used]
                act1 = "Free exploration"
                act2 = "Relaxation or local market"
                if len(available) > 0:
                    act1 = available[0]
                    used.add(act1)
                available = [a for a in attractions if a not in used]
                if len(available) > 0:
                    act2 = available[0]
                    used.add(act2)
                elif len(available) == 0 and act1 != "Free exploration":
                    act2 = "Free exploration"
                meal_location = (
                    act1 if act1 != "Free exploration"
                    else "your accommodation"
                )
                itinerary[f"Day {day}"] = {
                    "theme": f"Explore {place_name}",
                    "activities": [
                        act1,
                        act2,
                        "Evening stroll and dinner",
                    ],
                    "meal": f"Day {day} meal recommendation: local restaurants near {meal_location}",
                }
        return itinerary
    def generate_tour_plan(self, profile):
        recommendations = self.recommend_destinations(profile)
        plans = []
        for place_name, score in recommendations:
            food = self.get_food_recommendations(place_name, profile)
            wines = self.get_wine_recommendations(place_name)
            cost = self.estimate_cost(place_name, profile)
            itinerary = self.build_itinerary(place_name, profile)
            place_info = self.places[place_name]
            plans.append({
                "destination": place_name,
                "country": place_info["country"],
                "match_score": score,
                "best_for": place_info["tags"],
                "attractions": place_info["attractions"],
                "food_recommendations": food,
                "wine_recommendations": [
                    (n, w["flavor_profile"]) for n, w in wines
                ],
                "cost_breakdown": cost,
                "itinerary": itinerary,
                "safety_rating": place_info["safety_rating"],
                "currency": place_info["currency"],
                "language": place_info["language"],
            })
        return {
            "traveler": profile.name,
            "trip_duration": profile.duration_days,
            "travel_month": profile.travel_month,
            "budget_per_day": profile.budget_per_day_inr,
            "top_destinations": plans,
        }
    def print_plan(self, plan, currency_symbol="₹"):
        print("=" * 70)
        print(f"  PERSONALISED TRAVEL PLAN FOR: {plan['traveler'].upper()}")
        print("=" * 70)
        display_budget = round(plan["budget_per_day"])
        print(
            f"  Duration: {plan['trip_duration']} days | "
            f"Month: {plan['travel_month']} | "
            f"Budget: {currency_symbol}{display_budget}/day"
        )
        print()
        if not plan["top_destinations"]:
            print("  NO DESTINATIONS FOUND WITHIN BUDGET.")
            print(
                "  Based on your preferences, we could not find a suitable destination"
            )
            print(
                "  that fits within 150% of your maximum daily budget."
            )
            print(
                "  Please try increasing your budget or changing your accommodation type."
            )
            print("=" * 70)
            return
        for i, dest in enumerate(plan["top_destinations"], 1):
            print(
                f"  OPTION {i}: {dest['destination']}, "
                f"{dest['country']}  [Score: {dest['match_score']}]"
            )
            print("-" * 70)
            print(f"  Best For:       {', '.join(dest['best_for'])}")
            print(
                f"  Safety Rating:  "
                f"{'*' * dest['safety_rating']}"
                f"{'-' * (5 - dest['safety_rating'])}"
            )
            print(
                f"  Currency:       {dest['currency']}  |  "
                f"Language: {dest['language']}"
            )
            print()
            print("  TOP ATTRACTIONS:")
            for a in dest["attractions"]:
                print(f"    - {a}")
            if dest["food_recommendations"]:
                fr = dest["food_recommendations"]
                print(f"\n  CUISINE: {fr['cuisine']}")
                if fr["suitable_for_dietary"]:
                    print(f"  Dishes:  {', '.join(fr['dishes'][:3])}")
                else:
                    print(
                        "  No local dishes perfectly match your strict dietary restrictions."
                    )
                if fr["wine_pairing"]:
                    print(
                        f"  Wine Pairing: "
                        f"{', '.join(fr['wine_pairing'][:2])}"
                    )
            if dest["wine_recommendations"]:
                print("\n  WINE RECOMMENDATIONS:")
                for wname, flavors in dest["wine_recommendations"]:
                    print(f"    - {wname}: {', '.join(flavors)}")
            cost = dest["cost_breakdown"]
            print(f"\n  ESTIMATED COST ({plan['trip_duration']} days):")
            print(
                f"    Flights:          "
                f"{currency_symbol}{round(cost['flight_estimate_inr'])}"
            )
            print(
                f"    Accommodation:    "
                f"{currency_symbol}{round(cost['accommodation_total_inr'])}"
            )
            print(
                f"    Food:             "
                f"{currency_symbol}{round(cost['food_total_inr'])}"
            )
            print(
                f"    Activities:       "
                f"{currency_symbol}{round(cost['activities_total_inr'])}"
            )
            print(
                f"    Local Transport:  "
                f"{currency_symbol}{round(cost['local_transport_total_inr'])}"
            )
            print(f"    TOTAL:            "
                  f"{currency_symbol}{round(cost['grand_total_inr'])}  "
                  f"(~{currency_symbol}{round(cost['per_day_inr'])}/day)")
            print("\n  SAMPLE ITINERARY:")
            for day, details in dest["itinerary"].items():
                print(f"    {day} - {details['theme']}")
                for act in details["activities"]:
                    print(f"      - {act}")
                print()
        print("=" * 70)
def demo():
    print("\n" + "=" * 60)
    print("        AI TRAVEL PLANNER")
    print("=" * 60)
    name = input("Enter your name: ").strip()
    if not name:
        name = "Traveler"
    try:
        budget_inr = float(
            input(
                "Enter your maximum daily budget in INR (e.g., 20000): "
            )
        )
    except ValueError:
        print("Invalid input. Defaulting to ₹20000/day.")
        budget_inr = 20000.0
    interests_input = input(
        "Enter your interests separated by commas "
        "(e.g., food, history, nature): "
    )
    if interests_input.strip():
        interests = [
            item.strip().lower()
            for item in interests_input.split(",")
        ]
    else:
        interests = ["culture"]
    try:
        duration = int(
            input("Enter your trip duration in days (e.g., 7): ")
        )
    except ValueError:
        print("Invalid input. Defaulting to 7 days.")
        duration = 7
    try:
        month = int(
            input("Enter your travel month as a number (1-12): ")
        )
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        print("Invalid input. Defaulting to June (6).")
        month = 6
    dietary_input = input(
        "Enter dietary restrictions separated by commas "
        "(e.g., veg, vegan, gluten_free) or press enter for none: "
    )
    if dietary_input.strip():
        dietary = [
            item.strip().lower()
            for item in dietary_input.split(",")
        ]
    else:
        dietary = []
    print("\nAccommodation Options: budget, mid_range, luxury, ultra_luxury")
    accom_input = input(
        "Enter your accommodation preference: "
    ).strip().lower()
    if accom_input not in [
        "budget",
        "mid_range",
        "luxury",
        "ultra_luxury",
    ]:
        print("Invalid choice. Defaulting to 'mid_range'.")
        accom_input = "mid_range"
    print("\nThank you!Generating your personalized travel plan now...\n")
    planner = TravelPlanner()
    profile = UserProfile(
        name=name,
        budget_per_day_inr=budget_inr,
        interests=interests,
        duration_days=duration,
        travel_month=month,
        dietary_restrictions=dietary,
        accommodation_pref=accom_input,
    )
    plan = planner.generate_tour_plan(profile)
    planner.print_plan(plan, currency_symbol="₹")
if __name__ == "__main__":
    demo()