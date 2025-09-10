from app import app
from database import db
from models import Category

def seed_categories():
    categories = {
        "Foods & Drinks": [
            "Fast Food",
            "Restaurant, fast-food",
            "Groceries"
        ],
        "Shopping": [
            "Drug-store, chemist",
            "Free time",
            "Stationery, tools",
            "Gifts, joy",
            "Electronics, accessories",
            "Pets, animals",
            "Home, garden",
            "Toilertries",
            "Kitchen",
            "Kids",
            "Health and beauty",
            "Jewels, accessories",
            "Men's",
            "Fragrances",
            "Footwear",
            "Clothes"
        ],
        "Housing": [
            "Energy and Utilities"
        ],
        "Transport": [],
        "Vehicle": [],
        "Life & Entertainment": [
            "TV, Streaming",
            "Activeness sport and fitness",
            "Holiday and trips"
        ],
        "Communication and PC": [
            "Internet",
            "Airtime",
            "Bundles"
        ],
        "Financial Expenses": [
            "Charges & fees",
            "Loans & interests"
        ],
        "Investments": [
            "Trade",
            "MMF",
            "Savings"
        ],
        "Income": [],
        "Others": []
    }

    with app.app_context():
        for parent_name, subcats in categories.items():
            # Create parent category
            parent = Category(name=parent_name)
            db.session.add(parent)
            db.session.commit()

            # Create subcategories linked to parent
            for sub in subcats:
                child = Category(name=sub, parent_id=parent.id)
                db.session.add(child)

        db.session.commit()
        print("✅ Categories seeded successfully!")

if __name__ == "__main__":
    seed_categories()
