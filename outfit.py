import random

#logic for outfit creation
class OutfitGenerator:
    #method for generating outfit when user picks an occasion and weather
    def generate_new_outfit(self, occasion, weather, closet):
        matching_items = closet.get_filtered_items(
            category="All",
            occasion=occasion,
            weather=weather
        )

        tops = []
        bottoms = []
        shoes = []
        jackets = []

        #creates list from each item   
        for item in matching_items:
            if item.get_category() == "Top":
                tops.append(item)
            elif item.get_category() == "Bottom":
                bottoms.append(item)
            elif item.get_category() == "Shoes":
                shoes.append(item)
            elif item.get_category() == "Jacket":
                jackets.append(item)

        if not tops or not bottoms or not shoes:
            return None

        #randomly selects an outfit from the options 
        outfit = {
            "Top": random.choice(tops),
            "Bottom": random.choice(bottoms),
            "Shoes": random.choice(shoes)
        }

        if jackets:
            outfit["Jacket"] = random.choice(jackets)

        return outfit

    #feature to check if items match one occasion and oe weather as the selected item
    def item_matches_selected_vibe(self, candidate_item, selected_item):
        occasion_match = False
        weather_match = False

        for occasion in candidate_item.get_occasions():
            if occasion in selected_item.get_occasions():
                occasion_match = True

        for weather in candidate_item.get_weather_categories():
            if weather in selected_item.get_weather_categories():
                weather_match = True

        if occasion_match and weather_match:
            return True
        else:
            return False
    
    #user picks an item and outfit is built around it 
    def generate_outfit_from_item(self, item_name, closet):
        selected_item = closet.get_item_by_name(item_name)

        if selected_item is None:
            return None

        tops = []
        bottoms = []
        shoes = []
        jackets = []

        #lists with all available items that have same occasion and weather 
        for item in closet.get_all_items():
            if item.get_name() != selected_item.get_name():
                if self.item_matches_selected_vibe(item, selected_item):
                    if item.get_category() == "Top":
                        tops.append(item)
                    elif item.get_category() == "Bottom":
                        bottoms.append(item)
                    elif item.get_category() == "Shoes":
                        shoes.append(item)
                    elif item.get_category() == "Jacket":
                        jackets.append(item)

        outfit = {}

        #selecteed item will be included in the final version
        if selected_item.get_category() == "Top":
            outfit["Top"] = selected_item
        elif selected_item.get_category() == "Bottom":
            outfit["Bottom"] = selected_item
        elif selected_item.get_category() == "Shoes":
            outfit["Shoes"] = selected_item
        elif selected_item.get_category() == "Jacket":
            outfit["Jacket"] = selected_item

        #chooses matching clothing items 
        if "Top" not in outfit:
            if tops:
                outfit["Top"] = random.choice(tops)
            else:
                return None

        if "Bottom" not in outfit:
            if bottoms:
                outfit["Bottom"] = random.choice(bottoms)
            else:
                return None

        if "Shoes" not in outfit:
            if shoes:
                outfit["Shoes"] = random.choice(shoes)
            else:
                return None

        if "Jacket" not in outfit and jackets:
            outfit["Jacket"] = random.choice(jackets)

        return outfit