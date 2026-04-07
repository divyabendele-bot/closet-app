import streamlit as st
from closet import Closet
from models import Top, Bottom, Shoes, Jacket
from outfit import OutfitGenerator

# Push everything lower
st.markdown("<div style='margin-top: 140px;'></div>", unsafe_allow_html=True)

# Centered huge logo
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", use_container_width=True)

# Subtitle
st.markdown(
    "<p style='text-align: center; font-size:18px; color: #6b7280;'>Organize your closet and generate outfits!</p>",
    unsafe_allow_html=True
)
# run:
# source .venv/bin/activate
# python -m streamlit run app.py

if "closet" not in st.session_state:
    st.session_state.closet = Closet()

if "generator" not in st.session_state:
    st.session_state.generator = OutfitGenerator()

if "save_counter" not in st.session_state:
    st.session_state.save_counter = 0

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

CATEGORY_OPTIONS = [
    "Top",
    "Bottom",
    "Shoes",
    "Jacket"
]


def clean_item_name(raw_name):
    cleaned_name = raw_name.strip()

    if " (" in cleaned_name:
        cleaned_name = cleaned_name.split(" (")[0].strip()

    return cleaned_name



option = st.selectbox(
    "Menu",
    ["Add Item", "View Closet", "Generate Outfit"]
)

# ------------------------
# ADD ITEM SECTION
# ------------------------
if option == "Add Item":
    st.subheader("Add New Item")

    with st.form(key=f"add_item_form_{st.session_state.save_counter}", clear_on_submit=True):
        name = st.text_input("Item name")

        category = st.selectbox(
            "Category",
            CATEGORY_OPTIONS
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

        save_clicked = st.form_submit_button("Save Item")

        if save_clicked:
            cleaned_name = clean_item_name(name)

            if cleaned_name == "":
                st.warning("Please enter an item name.")
            elif len(occasions) == 0:
                st.warning("Please choose at least one occasion.")
            elif len(weather_categories) == 0:
                st.warning("Please choose at least one weather category.")
            else:
                final_name = st.session_state.closet.generate_unique_name(cleaned_name)

                image_data = None
                if image is not None:
                    image_data = image.getvalue()

                if category == "Top":
                    item = Top(final_name, occasions, weather_categories, image_data)
                elif category == "Bottom":
                    item = Bottom(final_name, occasions, weather_categories, image_data)
                elif category == "Shoes":
                    item = Shoes(final_name, occasions, weather_categories, image_data)
                else:
                    item = Jacket(final_name, occasions, weather_categories, image_data)

                st.session_state.closet.add_item(item)
                st.success(f"Saved: {item.display()}")
                st.session_state.save_counter += 1

# ------------------------
# VIEW CLOSET SECTION
# ------------------------
elif option == "View Closet":
    st.subheader("Your Closet")

    item_count = st.session_state.closet.count_items()
    st.write(f"Total items in closet: {item_count}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        filter_category = st.selectbox(
            "Category",
            ["All"] + CATEGORY_OPTIONS
        )

    with col2:
        filter_occasion = st.selectbox(
            "Occasion",
            ["All"] + OCCASION_OPTIONS
        )

    with col3:
        filter_weather = st.selectbox(
            "Weather",
            ["All"] + WEATHER_OPTIONS
        )

    with col4:
        sort_order = st.selectbox(
            "Sort",
            ["A-Z", "Z-A"]
        )

    filtered_items = st.session_state.closet.get_filtered_items(
        category=filter_category,
        occasion=filter_occasion,
        weather=filter_weather
    )

    filtered_items = sorted(
        filtered_items,
        key=lambda item: item.get_name().lower(),
        reverse=(sort_order == "Z-A")
    )

    if not filtered_items:
        st.info("No matching items found.")
    else:
        for item in filtered_items:
            st.markdown("---")

            image_col, info_col, button_col = st.columns([1, 2, 1])

            with image_col:
                if item.get_image_data() is not None:
                    st.image(item.get_image_data(), width=180)
                else:
                    st.write("No image uploaded")

            with info_col:
                st.markdown(f"### {item.get_name()}")
                st.write(f"**Category:** {item.get_category()}")
                st.write(f"**Occasions:** {', '.join(item.get_occasions())}")
                st.write(f"**Weather:** {', '.join(item.get_weather_categories())}")

            with button_col:
                st.write("")
                st.write("")
                if st.button("Remove", key=f"remove_{item.get_name()}"):
                    removed_item = st.session_state.closet.remove_item_by_name(item.get_name())
                    if removed_item is not None:
                        st.success(f"Removed: {removed_item.get_name()}")
                        st.rerun()

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
                st.write("You need at least a top, bottom, and shoes that all fit the selected occasion and weather.")
            else:
                st.write("Suggested outfit:")
                for category, item in outfit.items():
                    st.markdown("---")
                    st.write(f"**{category}: {item.get_name()}**")
                    st.write(f"Occasions: {', '.join(item.get_occasions())}")
                    st.write(f"Weather: {', '.join(item.get_weather_categories())}")

                    if item.get_image_data() is not None:
                        st.image(item.get_image_data(), width=180)
                    else:
                        st.write("No image uploaded")

    else:
        item_names = st.session_state.closet.get_item_names()

        if not item_names:
            st.write("Your closet is empty. Add some items first.")
        else:
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
                        st.markdown("---")
                        st.write(f"**{category}: {item.get_name()}**")
                        st.write(f"Occasions: {', '.join(item.get_occasions())}")
                        st.write(f"Weather: {', '.join(item.get_weather_categories())}")

                        if item.get_image_data() is not None:
                            st.image(item.get_image_data(), width=180)
                        else:
                            st.write("No image uploaded")