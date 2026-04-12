import streamlit as st
from closet import Closet
from models import Top, Bottom, Shoes, Jacket
from outfit import OutfitGenerator

#CSS code that will be plugged into Streamlit to edit the UI 
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e6f2ff;
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span {
        color: #2f3b52;
    }

    section[data-testid="stSidebar"] {
        background-color: #f5f9fc;
    }

    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #ffffff !important;
        color: #2f3b52 !important;
        border: none !important;
        border-radius: 10px !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #f3f4f6 !important;
    }

    .stTextInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stFileUploader label {
        color: #2f3b52 !important;
        font-weight: 500;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="column"]:last-child .stButton > button {
        background-color: #e74c3c !important;
        color: white !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="column"]:last-child .stButton > button:hover {
        background-color: #c0392b !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='margin-top: 140px;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", use_container_width=True)

st.markdown(
    "<p style='text-align: center; font-size:18px; color: #2f3b52;'>Organize your closet and generate outfits!</p>",
    unsafe_allow_html=True
)

# to run the app, run:
# python -m streamlit run app.py

#keep info between reruns 
if "closet" not in st.session_state:
    st.session_state.closet = Closet()
    st.session_state.closet.load_from_file()

if "generator" not in st.session_state:
    st.session_state.generator = OutfitGenerator()

if "save_counter" not in st.session_state:
    st.session_state.save_counter = 0

if "save_message" not in st.session_state:
    st.session_state.save_message = ""

if "selected_build_item" not in st.session_state:
    st.session_state.selected_build_item = None

if "build_outfit_result" not in st.session_state:
    st.session_state.build_outfit_result = None

if "show_outfit_dialog" not in st.session_state:
    st.session_state.show_outfit_dialog = False

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

#cleans up user input
def clean_item_name(raw_name):
    cleaned_name = raw_name.strip()

    if " (" in cleaned_name:
        cleaned_name = cleaned_name.split(" (")[0].strip()

    return cleaned_name

#session state for user building around an item, prepare pop up result
def generate_build_outfit(selected_item_name):
    st.session_state.selected_build_item = selected_item_name
    st.session_state.build_outfit_result = st.session_state.generator.generate_outfit_from_item(
        selected_item_name,
        st.session_state.closet
    )
    st.session_state.show_outfit_dialog = True

#close pop up 
def close_outfit_dialog():
    st.session_state.selected_build_item = None
    st.session_state.build_outfit_result = None
    st.session_state.show_outfit_dialog = False

#displays the clothes 
def display_outfit_cards(outfit):
    cols = st.columns(len(outfit))

    for col, (category, item) in zip(cols, outfit.items()):
        with col:
            st.markdown(f"### {category}")

            if item.get_image_data() is not None:
                st.image(item.get_image_data(), use_container_width=True)
            else:
                st.write("No image uploaded")

            st.write(f"**{item.get_name()}**")
            st.write(f"Occasions: {', '.join(item.get_occasions())}")
            st.write(f"Weather: {', '.join(item.get_weather_categories())}")

#create pop up window 
@st.dialog("Outfit Suggestion", dismissible=False)
def show_outfit_dialog():
    selected_item_name = st.session_state.selected_build_item
    outfit = st.session_state.build_outfit_result

    st.write(f"Built around: **{selected_item_name}**")

    if not outfit:
        st.write("No matching outfit could be generated from that item.")
        st.write("Make sure your closet has other items with overlapping occasion and weather tags.")
    else:
        st.write("Suggested outfit:")
        display_outfit_cards(outfit)

    button_col1, button_col2 = st.columns(2)

    with button_col1:
        if st.button("Generate New One", key="dialog_generate_new"):
            st.session_state.build_outfit_result = st.session_state.generator.generate_outfit_from_item(
                selected_item_name,
                st.session_state.closet
            )
            st.rerun()

    with button_col2:
        if st.button("Close", key="dialog_close"):
            close_outfit_dialog()
            st.rerun()


def display_item_card(item, show_remove_button=False, remove_key_prefix="remove", build_key_prefix="build"):
    st.markdown(
        """
        <div style="
            background-color: white;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        ">
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"### {item.get_name()}")

    if item.get_image_data() is not None:
        st.image(item.get_image_data(), use_container_width=True)
    else:
        st.write("No image uploaded")

    st.write(f"**Category:** {item.get_category()}")
    st.write(f"**Occasions:** {', '.join(item.get_occasions())}")
    st.write(f"**Weather:** {', '.join(item.get_weather_categories())}")

    if show_remove_button:
        if st.button("Remove", key=f"{remove_key_prefix}_{item.get_name()}"):
            removed_item = st.session_state.closet.remove_item_by_name(item.get_name())
            if removed_item is not None:
                st.session_state.closet.save_to_file()
                if st.session_state.selected_build_item == removed_item.get_name():
                    close_outfit_dialog()
                st.success(f"Removed: {removed_item.get_name()}")
                st.rerun()
    else:
        if st.button("Build around this item", key=f"{build_key_prefix}_{item.get_name()}"):
            generate_build_outfit(item.get_name())
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

#displays the sidebar options
option = st.sidebar.selectbox(
    "Menu",
    ["Add Item", "View Closet", "Generate Outfit"]
)

# Add item to closet 
if option == "Add Item":
    if st.session_state.show_outfit_dialog:
        close_outfit_dialog()

    st.subheader("Add New Item")

    if st.session_state.save_message != "":
        st.success(st.session_state.save_message)
        st.session_state.save_message = ""

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
                st.session_state.closet.save_to_file()
                st.session_state.save_message = f"Saved: {item.display()}"
                st.session_state.save_counter += 1
                st.rerun()


#View Closet 
elif option == "View Closet":
    if st.session_state.show_outfit_dialog:
        close_outfit_dialog()

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
        for row_start in range(0, len(filtered_items), 3):
            cols = st.columns(3)
            row_items = filtered_items[row_start:row_start + 3]

            for col, item in zip(cols, row_items):
                with col:
                    display_item_card(
                        item,
                        show_remove_button=True,
                        remove_key_prefix="remove_closet"
                    )

#Generate an outfit 
else:
    st.subheader("Generate Outfit")

    generation_mode = st.radio(
        "Choose outfit generation mode",
        ["Generate from occasion + weather", "Build around one item"]
    )
    #generate from occasion and weather 
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
                st.session_state.build_outfit_result = None
                st.session_state.selected_build_item = None
                st.session_state.show_outfit_dialog = False
                st.write("No matching outfit could be generated.")
                st.write("You need at least a top, bottom, and shoes that all fit the selected occasion and weather.")
            else:
                st.write("Suggested outfit:")
                display_outfit_cards(outfit)
                
    #build around item 
    else:
        item_names = st.session_state.closet.get_item_names()

        if not item_names:
            st.info("Your closet is empty. Add some items first.")
        else:
            filter_category = st.selectbox(
                "Filter items by category",
                ["All"] + CATEGORY_OPTIONS,
                key="build_filter_category"
            )

            selectable_items = st.session_state.closet.get_filtered_items(
                category=filter_category,
                occasion="All",
                weather="All"
            )

            selectable_items = sorted(
                selectable_items,
                key=lambda item: item.get_name().lower()
            )

            if not selectable_items:
                st.info("No items found in this category.")
            else:
                st.write("Choose the item you want to wear:")

                for row_start in range(0, len(selectable_items), 3):
                    cols = st.columns(3)
                    row_items = selectable_items[row_start:row_start + 3]

                    for col, item in zip(cols, row_items):
                        with col:
                            display_item_card(
                                item,
                                show_remove_button=False,
                                build_key_prefix="build_outfit"
                            )

if st.session_state.show_outfit_dialog:
    show_outfit_dialog()