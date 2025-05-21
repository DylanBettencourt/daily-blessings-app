import streamlit as st
import random

# Bible verses by category
categories = {
    "Peace": [
        ("John 14:27", "Peace I leave with you; my peace I give you."),
        ("Philippians 4:7", "The peace of God will guard your hearts and minds."),
        ("Psalm 4:8", "In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.")
    ],
    "Strength": [
        ("Isaiah 41:10", "Do not fear, for I am with you... I will strengthen you."),
        ("Philippians 4:13", "I can do all things through Christ who strengthens me."),
        ("2 Corinthians 12:9", "My grace is sufficient for you, for my power is made perfect in weakness.")
    ],
    "Healing": [
        ("Jeremiah 30:17", "I will restore you to health and heal your wounds."),
        ("James 5:15", "The prayer offered in faith will make the sick person well."),
        ("Exodus 15:26", "I am the Lord, who heals you.")
    ],
    "Gratitude": [
        ("1 Thessalonians 5:18", "Give thanks in all circumstances."),
        ("Psalm 107:1", "Give thanks to the Lord, for he is good."),
        ("Colossians 3:15", "Be thankful.")
    ]
}

# Blessings by category
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

# App UI
st.title("🙏 Daily Blessings & Bible Verse")
st.write("Choose a theme to receive today's scripture and blessing:")

category = st.selectbox("Category", list(categories.keys()))

if st.button("Show me the Word"):
    verse = random.choice(categories[category])
    prayer = random.choice(blessings[category])
    
    st.markdown(f"### 📖 {verse[0]}")
    st.success(f"“{verse[1]}”")
    
    st.markdown("### 🙏 Blessing")
    st.info(prayer)
