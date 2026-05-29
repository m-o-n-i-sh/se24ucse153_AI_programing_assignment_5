TOURIST_PLACES = {
    "Paris": {
        "country": "France",
        "region": "Europe",
        "climate": "temperate",
        "best_months": [4, 5, 6, 9, 10],
        "tags": ["culture", "art", "romance", "history", "food"],
        "avg_daily_cost_inr": 16600,
        "currency": "EUR",
        "language": "French",
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre Dame", "Versailles", "Montmartre"],
        "safety_rating": 4,
    },
    "Tokyo": {
        "country": "Japan",
        "region": "Asia",
        "climate": "temperate",
        "best_months": [3, 4, 10, 11],
        "tags": ["technology", "culture", "food", "anime", "shopping"],
        "avg_daily_cost_inr": 12450,
        "currency": "JPY",
        "language": "Japanese",
        "attractions": ["Shibuya Crossing", "Senso-ji Temple", "Akihabara", "Shinjuku", "Mount Fuji"],
        "safety_rating": 5,
    },
    "Bali": {
        "country": "Indonesia",
        "region": "Asia",
        "climate": "tropical",
        "best_months": [4, 5, 6, 7, 8, 9],
        "tags": ["beach", "nature", "wellness", "culture", "adventure"],
        "avg_daily_cost_inr": 6640,
        "currency": "IDR",
        "language": "Bahasa Indonesia",
        "attractions": ["Ubud Rice Terraces", "Tanah Lot Temple", "Mount Batur", "Seminyak Beach", "Sacred Monkey Forest"],
        "safety_rating": 4,
    },
    "New York": {
        "country": "USA",
        "region": "North America",
        "climate": "temperate",
        "best_months": [4, 5, 6, 9, 10],
        "tags": ["culture", "food", "shopping", "entertainment", "art"],
        "avg_daily_cost_inr": 20750,
        "currency": "USD",
        "language": "English",
        "attractions": ["Central Park", "Times Square", "Metropolitan Museum", "Statue of Liberty", "Broadway"],
        "safety_rating": 4,
    },
    "Cape Town": {
        "country": "South Africa",
        "region": "Africa",
        "climate": "mediterranean",
        "best_months": [11, 12, 1, 2, 3],
        "tags": ["nature", "adventure", "wine", "beach", "culture"],
        "avg_daily_cost_inr": 8300,
        "currency": "ZAR",
        "language": "English",
        "attractions": ["Table Mountain", "Cape of Good Hope", "Robben Island", "Stellenbosch Winery", "Boulders Beach"],
        "safety_rating": 3,
    },
    "Rome": {
        "country": "Italy",
        "region": "Europe",
        "climate": "mediterranean",
        "best_months": [4, 5, 6, 9, 10],
        "tags": ["history", "culture", "food", "art", "romance"],
        "avg_daily_cost_inr": 14940,
        "currency": "EUR",
        "language": "Italian",
        "attractions": ["Colosseum", "Vatican Museums", "Trevi Fountain", "Roman Forum", "Sistine Chapel"],
        "safety_rating": 4,
    },
    "Machu Picchu": {
        "country": "Peru",
        "region": "South America",
        "climate": "highland",
        "best_months": [5, 6, 7, 8, 9],
        "tags": ["adventure", "history", "nature", "trekking"],
        "avg_daily_cost_inr": 7470,
        "currency": "PEN",
        "language": "Spanish",
        "attractions": ["Machu Picchu Citadel", "Inca Trail", "Sun Gate", "Huayna Picchu", "Aguas Calientes"],
        "safety_rating": 4,
    },
    "Dubai": {
        "country": "UAE",
        "region": "Middle East",
        "climate": "desert",
        "best_months": [11, 12, 1, 2, 3],
        "tags": ["luxury", "shopping", "architecture", "adventure", "food"],
        "avg_daily_cost_inr": 24900,
        "currency": "AED",
        "language": "Arabic",
        "attractions": ["Burj Khalifa", "Dubai Mall", "Palm Jumeirah", "Desert Safari", "Gold Souk"],
        "safety_rating": 5,
    },
}

# New Destination-Specific Accommodation Costs (INR/Night)
ACCOMMODATION_COSTS = {
    "Paris":        {"budget": 8000, "mid_range": 15000, "luxury": 35000, "ultra_luxury": 80000},
    "Tokyo":        {"budget": 6000, "mid_range": 12000, "luxury": 30000, "ultra_luxury": 70000},
    "Bali":         {"budget": 1500, "mid_range": 4000,  "luxury": 15000, "ultra_luxury": 40000},
    "New York":     {"budget": 10000, "mid_range": 20000, "luxury": 45000, "ultra_luxury": 100000},
    "Cape Town":    {"budget": 2500, "mid_range": 6000,  "luxury": 18000, "ultra_luxury": 45000},
    "Rome":         {"budget": 7000, "mid_range": 13000, "luxury": 32000, "ultra_luxury": 75000},
    "Machu Picchu": {"budget": 2000, "mid_range": 5000,  "luxury": 16000, "ultra_luxury": 40000},
    "Dubai":        {"budget": 5000, "mid_range": 12000, "luxury": 40000, "ultra_luxury": 120000},
}

FOOD_RECOMMENDATIONS = {
    "French": {
        "tags": ["romance", "culture", "food"],
        "dishes": [
            {"name": "Croissant", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
            {"name": "Coq au Vin", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Crème Brûlée", "dietary": {"veg": True, "vegan": False, "gluten_free": True}},
            {"name": "Baguette", "dietary": {"veg": True, "vegan": True, "gluten_free": False}},
            {"name": "Ratatouille", "dietary": {"veg": True, "vegan": True, "gluten_free": True}},
        ],
        "wine_pairing": ["Bordeaux", "Burgundy", "Champagne"]
    },
    "Japanese": {
        "tags": ["food", "technology", "culture"],
        "dishes": [
            {"name": "Sushi", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Ramen", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
            {"name": "Tempura", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
            {"name": "Sashimi", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Matcha desserts", "dietary": {"veg": True, "vegan": False, "gluten_free": True}},
        ],
        "wine_pairing": ["Sake", "Japanese Whisky"]
    },
    "Balinese": {
        "tags": ["beach", "wellness", "culture"],
        "dishes": [
            {"name": "Nasi Goreng", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
            {"name": "Satay", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Babi Guling", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Lawar", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Pisang Goreng", "dietary": {"veg": True, "vegan": True, "gluten_free": False}},
        ],
        "wine_pairing": ["Bintang Beer", "Arak"]
    },
    "American": {
        "tags": ["food", "culture", "entertainment"],
        "dishes": [
            {"name": "New York Pizza", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
            {"name": "Bagels", "dietary": {"veg": True, "vegan": True, "gluten_free": False}},
            {"name": "Cheesecake", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
            {"name": "BBQ Ribs", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Clam Chowder", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
        ],
        "wine_pairing": ["Napa Valley Cabernet", "Oregon Pinot Noir"]
    },
    "South African": {
        "tags": ["wine", "nature", "adventure"],
        "dishes": [
            {"name": "Braai", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Bobotie", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
            {"name": "Biltong", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Boerewors", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Malva Pudding", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
        ],
        "wine_pairing": ["Stellenbosch Shiraz", "Chenin Blanc", "Pinotage"]
    },
    "Italian": {
        "tags": ["history", "food", "romance", "culture"],
        "dishes": [
            {"name": "Pasta Carbonara", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
            {"name": "Margherita Pizza", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
            {"name": "Gelato", "dietary": {"veg": True, "vegan": False, "gluten_free": True}},
            {"name": "Tiramisu", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
            {"name": "Risotto", "dietary": {"veg": True, "vegan": False, "gluten_free": True}},
        ],
        "wine_pairing": ["Chianti", "Barolo", "Pinot Grigio"]
    },
    "Peruvian": {
        "tags": ["adventure", "history", "nature"],
        "dishes": [
            {"name": "Ceviche", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Lomo Saltado", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
            {"name": "Anticuchos", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Aji de Gallina", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
            {"name": "Pisco Sour", "dietary": {"veg": True, "vegan": True, "gluten_free": True}},
        ],
        "wine_pairing": ["Pisco", "Peruvian Beer"]
    },
    "Emirati": {
        "tags": ["luxury", "shopping", "food"],
        "dishes": [
            {"name": "Machboos", "dietary": {"veg": False, "vegan": False, "gluten_free": True}},
            {"name": "Harees", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
            {"name": "Luqaimat", "dietary": {"veg": True, "vegan": True, "gluten_free": False}},
            {"name": "Shawarma", "dietary": {"veg": False, "vegan": False, "gluten_free": False}},
            {"name": "Manousheh", "dietary": {"veg": True, "vegan": False, "gluten_free": False}},
        ],
        "wine_pairing": ["Mocktails", "Arabic Coffee", "Date Juice"]
    },
}

WINE_ONTOLOGY = {
    "Bordeaux": {
        "region": "France",
        "type": "red",
        "grapes": ["Cabernet Sauvignon", "Merlot", "Cabernet Franc"],
        "flavor_profile": ["blackcurrant", "cedar", "tobacco"],
        "food_pairing": ["lamb", "beef", "aged cheese"],
        "price_tier": "premium",
    },
    "Burgundy": {
        "region": "France",
        "type": "red/white",
        "grapes": ["Pinot Noir", "Chardonnay"],
        "flavor_profile": ["cherry", "earthy", "floral"],
        "food_pairing": ["duck", "mushroom risotto", "soft cheese"],
        "price_tier": "luxury",
    },
    "Champagne": {
        "region": "France",
        "type": "sparkling",
        "grapes": ["Chardonnay", "Pinot Noir", "Pinot Meunier"],
        "flavor_profile": ["yeast", "citrus", "brioche"],
        "food_pairing": ["oysters", "caviar", "light appetizers"],
        "price_tier": "premium",
    },
    "Chianti": {
        "region": "Italy",
        "type": "red",
        "grapes": ["Sangiovese"],
        "flavor_profile": ["cherry", "herbs", "leather"],
        "food_pairing": ["pasta", "pizza", "tomato-based dishes"],
        "price_tier": "mid",
    },
    "Stellenbosch Shiraz": {
        "region": "South Africa",
        "type": "red",
        "grapes": ["Shiraz"],
        "flavor_profile": ["dark fruit", "spice", "smoke"],
        "food_pairing": ["braai", "lamb", "dark chocolate"],
        "price_tier": "mid",
    },
    "Napa Valley Cabernet": {
        "region": "USA",
        "type": "red",
        "grapes": ["Cabernet Sauvignon"],
        "flavor_profile": ["blackberry", "vanilla", "oak"],
        "food_pairing": ["steak", "grilled meats", "aged cheese"],
        "price_tier": "premium",
    },
}

TRANSPORT_COSTS = {
    "Europe": {"flight_per_hour": 6640, "train_per_hour": 2490, "local_daily": 1245, "avg_travel_hours": 9},
    "Asia": {"flight_per_hour": 5810, "train_per_hour": 1660, "local_daily": 830, "avg_travel_hours": 6},
    "North America": {"flight_per_hour": 8300, "train_per_hour": 4150, "local_daily": 1660, "avg_travel_hours": 15},
    "South America": {"flight_per_hour": 7470, "train_per_hour": 2075, "local_daily": 996, "avg_travel_hours": 18},
    "Africa": {"flight_per_hour": 7885, "train_per_hour": 2490, "local_daily": 830, "avg_travel_hours": 10},
    "Middle East": {"flight_per_hour": 7055, "train_per_hour": 1660, "local_daily": 1494, "avg_travel_hours": 4},
}

CITY_TO_CUISINE_MAP = {
    "Paris": "French",
    "Tokyo": "Japanese",
    "Bali": "Balinese",
    "New York": "American",
    "Cape Town": "South African",
    "Rome": "Italian",
    "Machu Picchu": "Peruvian",
    "Dubai": "Emirati",
}