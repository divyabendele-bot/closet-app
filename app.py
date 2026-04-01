import os
import streamlit as st
from closet import Closet
from models import Top, Bottom, Shoes, Jacket
from outfit import OutfitGenerator

# run:
# source .venv/bin/activate
# python -m streamlit run app.py

if "closet" not in st.session_state:
    st.session_state.closet = Closet()

if "generator" not in st.session_state:
    st.session_state.generator = OutfitGenerator()

IMAGE_FOLDER = "images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

OCCASION_OPTIONS = [
    "Business",
    "Going out / Party",
    "Casual",
    "Formal / Evening wear"
]

WEATHER_OPTIONS = [
    "Hot",
    "Mild",
    "Cold"
]

st.title("My Closet App 👕")
st.write("Organize your closet and generate outfits.")

option = st.selectbox(
    "Menu",
    ["Add Item", "View Closet", "Remove Item", "Generate Outfit"]
)

# ------------------------
# ADD ITEM SECTION
# ------------------------
if option == "Add Item":
    st.subheader("Add New Item")

    name = st.text_input("Item name")

    category = st.selectbox(
        "Category",
        ["Top", "Bottom", "Shoes", "Jacket"]
    )

    occasions = st.multiselect(
        "Occasions",
        OCCASION_OPTIONS
    )

    weather_categories = st.multiselect(
        "Weather",
        WEATHER_OPTIONS
    )

    image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    if st.button("Save Item"):
        if name.strip() == "":
            st.warning("Please enter an item name.")
        elif len(occasions) == 0:
            st.warning("Please choose at least one occasion.")
        elif len(weather_categories) == 0:
            st.warning("Please choose at least one weather category.")
        else:
            image_path = None

            if image is not None:
                image_path = os.path.join(IMAGE_FOLDER, image.name)

                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            if category == "Top":
                item = Top(name, occasions, weather_categories, image_path)
            elif category == "Bottom":
                item = Bottom(name, occasions, weather_categories, image_path)
            elif category == "Shoes":
                item = Shoes(name, occasions, weather_categories, image_path)
            else:
                item = Jacket(name, occasions, weather_categories, image_path)

            st.session_state.closet.add_item(item)
            st.success(f"{item.display()} saved!")

# ------------------------
# VIEW CLOSET SECTION
# ------------------------
# ------------------------
# VIEW CLOSET SECTION
# ------------------------
elif option == "View Closet":
    st.subheader("Your Closet")

    item_count = st.session_state.closet.count_items()
    st.write(f"Total items in closet: {item_count}")

    filter_category = st.selectbox(
        "Filter by category",
        ["All", "Top", "Bottom", "Shoes", "Jacket"]
    )

    filter_occasion = st.selectbox(
        "Filter by occasion",
        ["All"] + OCCASION_OPTIONS
    )

    filter_weather = st.selectbox(
        "Filter by weather",
        ["All"] + WEATHER_OPTIONS
    )

    items = st.session_state.closet.get_all_items()
    filtered_items = []

    for item in items:
        category_match = False
        occasion_match = False
        weather_match = False

        if filter_category == "All" or item.get_category() == filter_category:
            category_match = True

        if filter_occasion == "All" or filter_occasion in item.get_occasions():
            occasion_match = True

        if filter_weather == "All" or filter_weather in item.get_weather_categories():
            weather_match = True

        if category_match and occasion_match and weather_match:
            filtered_items.append(item)

    if not filtered_items:
        st.write("No matching items found.")
    else:
        for item in filtered_items:
            st.write(item.display())

            if item.get_image_path():
                st.image(item.get_image_path(), width=150)

# ------------------------
# REMOVE ITEM SECTION
# ------------------------
elif option == "Remove Item":
    st.subheader("Remove Item")

    remove_name = st.text_input("Enter the name of the item to remove")

    if st.button("Remove"):
        if remove_name.strip() == "":
            st.warning("Please enter an item name.")
        else:
            removed_item = st.session_state.closet.remove_item_by_name(remove_name)

            if removed_item is None:
                st.write("Item not found.")
            else:
                st.success(f"Removed: {removed_item.display()}")

# ------------------------
# GENERATE OUTFIT SECTION
# ------------------------
else:
    st.subheader("Generate Outfit")

    generation_mode = st.radio(
        "Choose outfit generation mode",
        ["Generate from occasion + weather", "Build around one item"]
    )

    if generation_mode == "Generate from occasion + weather":
        occasion_choice = st.selectbox(
            "Choose an occasion",
            OCCASION_OPTIONS
        )

        weather_choice = st.selectbox(
            "Choose a weather category",
            WEATHER_OPTIONS
        )

        if st.button("Generate New Outfit"):
            outfit = st.session_state.generator.generate_new_outfit(
                occasion_choice,
                weather_choice,
                st.session_state.closet
            )

            if not outfit:
                st.write("No matching outfit could be generated.")
                st.write("You need at least a top, bottom, and shoes that fit the same occasion and weather.")
            else:
                st.write("Suggested outfit:")
                for category, item in outfit.items():
                    st.write(f"{category}: {item.display()}")

                    if item.get_image_path():
                        st.image(item.get_image_path(), width=150)

    else:
        items = st.session_state.closet.get_all_items()

        if not items:
            st.write("Your closet is empty. Add some items first.")
        else:
            item_names = st.session_state.closet.get_item_names()

            selected_item_name = st.selectbox(
                "Choose an item you want to wear",
                item_names
            )

            if st.button("Build Outfit Around Item"):
                outfit = st.session_state.generator.generate_outfit_from_item(
                    selected_item_name,
                    st.session_state.closet
                )

                if not outfit:
                    st.write("No matching outfit could be generated from that item.")
                    st.write("Make sure your closet has other items with overlapping occasion and weather tags.")
                else:
                    st.write("Suggested outfit:")
                    for category, item in outfit.items():
                        st.write(f"{category}: {item.display()}")

                        if item.get_image_path():
                            st.image(item.get_image_path(), width=150)