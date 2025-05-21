import random
import time

def christian_blessing_app_with_categories():
    verses = {
        "Peace": [
            "John 14:27 — 'Peace I leave with you; my peace I give you...'",
            "Philippians 4:7 — 'And the peace of God, which transcends all understanding...'",
            "Psalm 4:8 — 'In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.'"
        ],
        "Strength": [
            "Isaiah 41:10 — 'Do not fear, for I am with you... I will strengthen you and help you.'",
            "Philippians 4:13 — 'I can do all things through Christ who strengthens me.'",
            "2 Corinthians 12:9 — 'My grace is sufficient for you, for my power is made perfect in weakness.'"
        ],
        "Healing": [
            "Jeremiah 30:17 — 'But I will restore you to health and heal your wounds, declares the Lord.'",
            "James 5:15 — 'And the prayer offered in faith will make the sick person well...'",
            "Exodus 15:26 — 'I am the Lord, who heals you.'"
        ],
        "Gratitude": [
            "1 Thessalonians 5:18 — 'Give thanks in all circumstances; for this is God's will for you.'",
            "Psalm 107:1 — 'Give thanks to the Lord, for he is good; his love endures forever.'",
            "Colossians 3:15 — 'Be thankful.'"
        ]
    }

    blessings = {
        "Peace": [
            "May God's peace cover your mind and calm your spirit today.",
            "May you rest knowing God is in control.",
            "May peace flood your heart and silence your worries."
        ],
        "Strength": [
            "May the Lord be your strength when you feel weak.",
            "May you rise today with courage and resilience.",
            "May God empower you to endure and overcome."
        ],
        "Healing": [
            "May the healing touch of Jesus restore you fully.",
            "May God's grace bring comfort to your body and soul.",
            "May you be wrapped in divine healing and love."
        ],
        "Gratitude": [
            "May you see blessings in every small moment today.",
            "May your heart overflow with thankfulness.",
            "May you always find a reason to praise."
        ]
    }

    categories = list(verses.keys())

    print("🕊️ Welcome to the Daily Verse & Blessing 🕊️")
    print("Choose a category to receive a verse and blessing.\n")

    while True:
        print("Available Categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        choice = input("\nEnter the number of the category (or type 'exit' to quit): ")

        if choice.lower() in ['exit', 'quit']:
            print("May God bless your journey ahead! ✝️")
            break

        if not choice.isdigit() or int(choice) not in range(1, len(categories) + 1):
            print("Invalid choice. Please enter a number from the list.\n")
            continue

        selected = categories[int(choice) - 1]
        verse = random.choice(verses[selected])
        blessing = random.choice(blessings[selected])

        print("\n📖 Verse:")
        time.sleep(1)
        print(f"   {verse}\n")

        time.sleep(1)
        print("🙏 Blessing:")
        print(f"   {blessing}\n")
        print("-" * 50)

# Run it
christian_blessing_app_with_categories()
