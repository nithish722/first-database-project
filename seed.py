import sqlite3
import os
import random

DB_PATH = 'server/db/tastehub.db'
SCHEMA_PATH = 'server/db/schema.sql'

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(SCHEMA_PATH, 'r') as f:
        schema_script = f.read()
    
    cursor.executescript(schema_script)
    conn.commit()
    print("Database initialized and schema applied.")
    return conn

def seed_db(conn):
    cursor = conn.cursor()
    
    # 1. Create Admins
    cursor.execute("INSERT INTO admins (admin_name, email, password) VALUES ('Super Admin', 'admin@tastehub.com', 'admin123')")
    
    # 2. Create Users
    cursor.execute("INSERT INTO users (name, email, password, phone, address) VALUES ('Test User', 'user@tastehub.com', 'user123', '1234567890', '123 Glassy St, Cybertown')")
    
    # 3. Create Kitchens (10 Veg, 10 Mixed)
    # You can edit the names, descriptions, locations, and images here!
    kitchens = [
        # --- Vegetarian Kitchens (First 10) ---
        ("Pure Veg Delights", "Exclusive vegetarian dishes, healthy and fresh.", "North", "1.jpg"),
        ("Green Leaf Bowl", "Fresh salads and natural ingredients.", "South", "2.jpg"),
        ("The Veggie Station", "Your daily stop for vegetarian fast food.", "East", "3.jpg"),
        ("Nature's Kitchen", "Organic and wholesome plant-based food.", "West", "4.jpg"),
        ("Herb & Spices Veg", "Aromatic vegetarian curries and more.", "Central", "5.jpg"),
        ("Paneer Paradise", "Everything paneer, made with love.", "North", "6.jpg"),
        ("Evergreen Bites", "Snacks and quick bites for vegetarians.", "South", "7.jpg"),
        ("Vegan Vibes", "100% vegan cafe and kitchen.", "East", "8.jpg"),
        ("Sattvic Food House", "Traditional pure vegetarian meals.", "West", "9.jpg"),
        ("The Salad Bar", "Freshly chopped salads and healthy bowls.", "Central", "10.jpg"),
        
        # --- Mixed (Veg & Non-Veg) Kitchens (Next 10) ---
        ("Mixed Spices Palace", "A mix of non-veg and veg meals for everyone.", "North", "11.jpg"),
        ("The Roasting Grill", "BBQ ribs, chicken, and grilled veggies.", "South", "12.jpg"),
        ("Urban Bites", "Modern street food fusion.", "East", "13.jpg"),
        ("Ocean & Earth Hub", "Seafood specialties and vegetarian classics.", "West", "14.jpg"),
        ("The Chicken Co.", "Fried, grilled, and roasted chicken.", "Central", "15.jpg"),
        ("Spice Route", "Multi-cuisine restaurant with global flavors.", "North", "16.jpg"),
        ("Midnight Munchies", "Late-night delivery for all your cravings.", "South", "17.jpg"),
        ("Comfort Food Express", "Warm, hearty meals prepared fresh.", "East", "18.jpg"),
        ("Wok This Way", "Chinese and Asian fusion cuisine.", "West", "19.jpg"),
        ("Gourmet Kitchen", "Premium ingredients, masterfully cooked.", "Central", "20.jpg")
    ]
        
    cursor.executemany("INSERT INTO kitchens (kitchen_name, descriptions, location, image_url) VALUES (?, ?, ?, ?)", kitchens)
    conn.commit()
    
    print("Seeded 20 Kitchens.")
    
    # 4. Create 30 Menu Items per Kitchen
    veg_dishes = [
        ("Paneer Butter Masala", "21.jpg"), ("Dal Makhani", "22.jpg"),
        ("Aloo Gobi", "23.jpg"), ("Palak Paneer", "24.jpg"),
        ("Veg Biryani", "25.jpg"), ("Mushroom Risotto", "26.jpg"),
        ("Veg Burger", "27.jpg"), ("Pasta Primavera", "28.jpg"),
        ("Greek Salad", "29.jpg"), ("Margherita Pizza", "30.jpg"),
        ("Chole Bhature", "31.jpg"), ("Rajma Chawal", "32.jpg"),
        ("Malai Kofta", "33.jpg"), ("Bhindi Masala", "34.jpg"),
        ("Veg Fried Rice", "35.jpg"), ("Hakka Noodles", "36.jpg"),
        ("Pani Puri", "37.jpg"), ("Pav Bhaji", "38.jpg"),
        ("Masala Dosa", "39.jpg"), ("Idli Sambar", "40.jpg"),
        ("Veg Spring Roll", "41.jpg"), ("Manchurian", "42.jpg"),
        ("Gobi 65", "43.jpg"), ("Tandoori Roti", "44.jpg"),
        ("Garlic Naan", "45.jpg"), ("Gulab Jamun", "46.jpg"),
        ("Rasgulla", "47.jpg"), ("Kheer", "48.jpg"),
        ("Mango Lassi", "49.jpg"), ("Fruit Chaat", "50.jpg")
    ]
                  
    non_veg_dishes = [
        ("Chicken Tikka Masala", "51.jpg"), ("Butter Chicken", "52.jpg"),
        ("Mutton Curry", "53.jpg"), ("Fish and Chips", "54.jpg"),
        ("Chicken Biryani", "55.jpg"), ("Beef Burger", "56.jpg"),
        ("Pepperoni Pizza", "57.jpg"), ("BBQ Ribs", "58.jpg"),
        ("Grilled Salmon", "59.jpg"), ("Chicken Wings", "60.jpg"),
        ("Egg Curry", "61.jpg"), ("Prawn Masala", "62.jpg"),
        ("Chicken Fried Rice", "63.jpg"), ("Chicken Noodles", "64.jpg"),
        ("Chicken Shawarma", "65.jpg"), ("Tandoori Chicken", "66.jpg"),
        ("Chicken 65", "67.jpg"), ("Fish Curry", "68.jpg"),
        ("Pork Belly", "69.jpg"), ("Lamb Chop", "70.jpg"),
        ("Chicken Momo", "71.jpg"), ("Keema Pav", "72.jpg"),
        ("Chicken Sausages", "73.jpg"), ("Turkey Roast", "74.jpg"),
        ("Crab Masala", "75.jpg"), ("Squid Rings", "76.jpg"),
        ("Omelette", "77.jpg"), ("Chicken Wrap", "78.jpg"),
        ("Mutton Biryani", "79.jpg"), ("Chicken Salad", "80.jpg")
    ]
    
    menu_items = []
    
    # Categories
    categories = ["Main Course", "Starter", "Dessert", "Beverage"]
    
    for k_id in range(1, len(kitchens) + 1):
        is_veg_kitchen = k_id <= 10
        for i in range(30):
            if is_veg_kitchen:
                dish, image_url = veg_dishes[i]
                category = "Main Course" if "Biryani" in dish or "Masala" in dish else "Starter"
            else:
                # Mix of veg and non veg
                dish, image_url = veg_dishes[i] if i % 2 == 0 else non_veg_dishes[i]
                category = "Main Course" if "Biryani" in dish or "Chicken" in dish else "Starter"
                
            price = round(random.uniform(5.0, 25.0), 2)
            
            menu_items.append((k_id, dish, f"Delicious {dish} carefully prepared.", category, price, image_url))
            
    cursor.executemany("INSERT INTO menu_items (kitchen_id, item_name, description, category, price, image_url) VALUES (?, ?, ?, ?, ?, ?)", menu_items)
    conn.commit()
    print(f"Seeded {len(menu_items)} Menu Items.")

    conn.close()
    
if __name__ == '__main__':
    conn = init_db()
    seed_db(conn)
    print("Database seeding successfully completed!")
