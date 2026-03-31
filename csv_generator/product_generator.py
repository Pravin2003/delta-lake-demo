"""
Product CSV Generator
=====================
Generates a realistic product catalog CSV with 31 columns.
Run from terminal: python product_generator.py
Customize via the CONFIG section below.
"""

import csv
import random
import uuid
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# ══════════════════════════════════════════════════════════════════
#  CONFIG — Edit these to control output
# ══════════════════════════════════════════════════════════════════

CONFIG = {
    "total_rows":   100000,          # How many product rows to generate
    "output_dir":   "/Users/pravinmisal/Developement/delta-lake-demo/data",             # Folder where the file is saved (. = same folder as script)
    "random_seed":  None,            # Set an integer (e.g. 42) for reproducible data, None for fresh data every run
}

# ══════════════════════════════════════════════════════════════════
#  REFERENCE DATA — Customize brands, categories, etc. here
# ══════════════════════════════════════════════════════════════════

BRANDS = [
    "Nike", "Adidas", "Samsung", "Apple", "Sony", "LG", "Philips", "Bosch", "Puma", "Reebok",
    "H&M", "Zara", "Levi's", "Tommy Hilfiger", "Calvin Klein", "Under Armour", "Casio",
    "Canon", "Nikon", "HP", "Dell", "Lenovo", "Asus", "Acer", "Panasonic", "Whirlpool",
    "Havells", "Bajaj", "Crompton", "Prestige", "Titan", "Fastrack", "Woodland", "Bata",
    "VIP", "Wildcraft", "Decathlon", "Lacoste", "Polo", "Fossil",
]

CATEGORIES = {
    "Electronics":       ["Smartphones", "Laptops", "Tablets", "Cameras", "Headphones", "Speakers", "TVs", "Monitors", "Keyboards", "Mice"],
    "Clothing":          ["T-Shirts", "Jeans", "Dresses", "Jackets", "Formal Shirts", "Ethnic Wear", "Activewear", "Shorts", "Skirts", "Coats"],
    "Footwear":          ["Sneakers", "Sandals", "Boots", "Formal Shoes", "Loafers", "Flip Flops", "Sports Shoes", "Heels", "Moccasins", "Slippers"],
    "Home & Kitchen":    ["Cookware", "Appliances", "Furniture", "Bedding", "Lighting", "Decor", "Storage", "Cleaning", "Gardening", "Bath"],
    "Sports & Fitness":  ["Dumbbells", "Yoga Mats", "Resistance Bands", "Treadmills", "Cycles", "Footballs", "Cricket Gear", "Badminton", "Swimming", "Boxing"],
    "Beauty & Health":   ["Skincare", "Haircare", "Makeup", "Fragrances", "Vitamins", "Medical Devices", "Oral Care", "Men's Grooming", "Baby Care", "Ayurvedic"],
    "Books & Stationery":["Fiction", "Non-Fiction", "Textbooks", "Notebooks", "Pens", "Art Supplies", "Planners", "Comics", "Magazines", "Office Supplies"],
    "Toys & Games":      ["Action Figures", "Board Games", "Puzzles", "Remote Control", "Dolls", "Building Blocks", "Outdoor Toys", "Video Games", "Card Games", "Educational"],
    "Bags & Luggage":    ["Backpacks", "Handbags", "Trolleys", "Wallets", "Sling Bags", "Duffel Bags", "Laptop Bags", "Travel Pouches", "Clutches", "Tote Bags"],
    "Automotive":        ["Car Accessories", "Bike Accessories", "Helmets", "Covers", "Cleaning Kits", "GPS", "Dash Cams", "Chargers", "Seat Covers", "Air Fresheners"],
}

COLORS        = ["Black", "White", "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Grey",
                 "Brown", "Navy", "Beige", "Teal", "Maroon", "Silver", "Gold", "Rose Gold", "Olive", "Cyan"]
SIZES         = ["XS", "S", "M", "L", "XL", "XXL", "One Size", "30", "32", "34", "36", "38", "40", "42", "6", "7", "8", "9", "10", "11"]
MATERIALS     = ["Cotton", "Polyester", "Leather", "Nylon", "Wool", "Silk", "Denim", "Linen",
                 "Rubber", "Metal", "Plastic", "Wood", "Glass", "Ceramic", "Aluminium", "Stainless Steel"]
CURRENCIES    = ["INR"] * 8 + ["USD", "EUR"]     # 80% INR, 10% USD, 10% EUR
COUNTRIES     = ["India", "China", "USA", "Germany", "Japan", "South Korea", "Bangladesh", "Vietnam", "Taiwan", "Italy"]
WARRANTIES    = [0, 6, 12, 18, 24, 36]
AVAILABILITIES = ["In Stock", "Out of Stock", "Pre-Order", "Discontinued", "Limited Stock"]
DISCOUNTS     = [0, 0, 0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70]   # 0 weighted higher
TAX_RATES     = [0, 5, 12, 18, 28]

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

def generate_ean13():
    """Generate a valid EAN-13 barcode with correct check digit."""
    digits = [random.randint(0, 9) for _ in range(12)]
    check  = (10 - sum((3 if i % 2 else 1) * d for i, d in enumerate(digits)) % 10) % 10
    return "".join(map(str, digits + [check]))


def random_datetime(start_year=2022, end_year=2025):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
    return start + delta


def build_output_filename():
    """Generates filename like: products-31032025.csv"""
    today = datetime.today().strftime("%d%m%Y")
    return f"products-{today}.csv"


# ══════════════════════════════════════════════════════════════════
#  ROW GENERATOR
# ══════════════════════════════════════════════════════════════════

def generate_row(index: int) -> dict:
    category     = random.choice(list(CATEGORIES.keys()))
    subcategory  = random.choice(CATEGORIES[category])
    brand        = random.choice(BRANDS)
    color        = random.choice(COLORS)
    size         = random.choice(SIZES)
    material     = random.choice(MATERIALS)
    currency     = random.choice(CURRENCIES)
    base_price   = round(random.uniform(99, 99_999), 2)
    discount     = random.choice(DISCOUNTS)
    final_price  = round(base_price * (1 - discount / 100), 2)
    created_at   = random_datetime(2022, 2024)
    updated_at   = created_at + timedelta(days=random.randint(0, 365))
    internal_id  = f"PROD-{uuid.uuid4().hex[:8].upper()}"
    sku          = f"{brand[:3].upper()}-{category[:3].upper()}-{str(index).zfill(6)}"

    return {
        "Index":             index,
        "Name":              f"{brand} {subcategory} {color} {size}",
        "Description":       fake.sentence(nb_words=random.randint(10, 18)),
        "Brand":             brand,
        "Category":          category,
        "Subcategory":       subcategory,
        "Price":             base_price,
        "Currency":          currency,
        "Discount_Pct":      discount,
        "Final_Price":       final_price,
        "Tax_Rate":          random.choice(TAX_RATES),
        "Stock":             random.randint(0, 5000),
        "EAN":               generate_ean13(),
        "SKU":               sku,
        "Internal_ID":       internal_id,
        "Color":             color,
        "Size":              size,
        "Material":          material,
        "Weight_kg":         round(random.uniform(0.1, 30.0), 2),
        "Length_cm":         round(random.uniform(2.0, 200.0), 1),
        "Width_cm":          round(random.uniform(2.0, 150.0), 1),
        "Height_cm":         round(random.uniform(1.0, 100.0), 1),
        "Rating":            round(random.uniform(1.0, 5.0), 1),
        "Review_Count":      random.randint(0, 25_000),
        "Availability":      random.choice(AVAILABILITIES),
        "Supplier":          fake.company(),
        "Country_of_Origin": random.choice(COUNTRIES),
        "Warranty_Months":   random.choice(WARRANTIES),
        "Tags":              f"{category}|{subcategory}|{brand}|{color}|{material}",
        "Image_URL":         f"https://cdn.example.com/products/{internal_id.lower()}.jpg",
        "Created_At":        created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Updated_At":        updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════

FIELDNAMES = [
    "Index", "Name", "Description", "Brand", "Category", "Subcategory",
    "Price", "Currency", "Discount_Pct", "Final_Price", "Tax_Rate",
    "Stock", "EAN", "SKU", "Internal_ID",
    "Color", "Size", "Material",
    "Weight_kg", "Length_cm", "Width_cm", "Height_cm",
    "Rating", "Review_Count", "Availability",
    "Supplier", "Country_of_Origin", "Warranty_Months",
    "Tags", "Image_URL", "Created_At", "Updated_At",
]


def main():
    # Apply seed if set
    if CONFIG["random_seed"] is not None:
        random.seed(CONFIG["random_seed"])
        Faker.seed(CONFIG["random_seed"])

    # Build output path
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    filename    = build_output_filename()
    output_path = os.path.join(CONFIG["output_dir"], filename)

    total = CONFIG["total_rows"]
    print(f"Generating {total:,} rows → {output_path}")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

        for i in range(1, total + 1):
            writer.writerow(generate_row(i))

            # Progress indicator every 1000 rows
            if i % 1_000 == 0:
                print(f"  ✓ {i:,} / {total:,} rows written...")

    print(f"\nDone! File saved: {output_path}")
    print(f"Columns : {len(FIELDNAMES)}")
    print(f"Rows    : {total:,}")


if __name__ == "__main__":
    main()