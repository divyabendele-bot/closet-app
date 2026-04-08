import json
import os
import pickle
from models import Top, Bottom, Shoes, Jacket


class Closet:
    def __init__(self):
        self.__items = []

    def add_item(self, item):
        self.__items.append(item)

    def get_all_items(self):
        return self.__items

    def count_items(self):
        return len(self.__items)

    def get_item_names(self):
        names = []
        for item in self.__items:
            names.append(item.get_name())
        return names

    def get_item_by_name(self, name):
        index = 0

        while index < len(self.__items):
            if self.__items[index].get_name() == name:
                return self.__items[index]
            index += 1

        return None

    def remove_item_by_name(self, name):
        index = 0

        while index < len(self.__items):
            if self.__items[index].get_name() == name:
                removed_item = self.__items.pop(index)
                return removed_item
            index += 1

        return None

    def get_items_sorted_by_name(self):
        return sorted(self.__items, key=lambda item: item.get_name().lower())

    def get_filtered_items(self, category="All", occasion="All", weather="All"):
        filtered_items = []

        for item in self.__items:
            category_match = False
            occasion_match = False
            weather_match = False

            if category == "All" or item.get_category() == category:
                category_match = True

            if occasion == "All" or occasion in item.get_occasions():
                occasion_match = True

            if weather == "All" or weather in item.get_weather_categories():
                weather_match = True

            if category_match and occasion_match and weather_match:
                filtered_items.append(item)

        return filtered_items

    def generate_unique_name(self, name):
        existing_names = self.get_item_names()

        if name not in existing_names:
            return name

        counter = 2
        new_name = f"{name} {counter}"

        while new_name in existing_names:
            counter += 1
            new_name = f"{name} {counter}"

        return new_name

    def save_to_file(self, filename="closet_data.json"):
        data = []

        for item in self.__items:
            image_data = item.get_image_data()
            image_hex = image_data.hex() if image_data is not None else None

            item_dict = {
                "name": item.get_name(),
                "category": item.get_category(),
                "occasions": item.get_occasions(),
                "weather_categories": item.get_weather_categories(),
                "image_data": image_hex
            }

            data.append(item_dict)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def load_from_file(self, json_filename="closet_data.json", pickle_filename="closet_data.pkl"):
        if os.path.exists(json_filename):
            self.load_from_json(json_filename)
            return

        if os.path.exists(pickle_filename):
            loaded = self.load_from_pickle(pickle_filename)

            if loaded:
                self.save_to_file(json_filename)

    def load_from_json(self, filename="closet_data.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            loaded_items = []

            for item_data in data:
                name = item_data["name"]
                category = item_data["category"]
                occasions = item_data["occasions"]
                weather_categories = item_data["weather_categories"]

                image_data = None
                if item_data["image_data"] is not None:
                    image_data = bytes.fromhex(item_data["image_data"])

                if category == "Top":
                    item = Top(name, occasions, weather_categories, image_data)
                elif category == "Bottom":
                    item = Bottom(name, occasions, weather_categories, image_data)
                elif category == "Shoes":
                    item = Shoes(name, occasions, weather_categories, image_data)
                else:
                    item = Jacket(name, occasions, weather_categories, image_data)

                loaded_items.append(item)

            self.__items = loaded_items

        except:
            self.__items = []

    def load_from_pickle(self, filename="closet_data.pkl"):
        try:
            with open(filename, "rb") as file:
                loaded_items = pickle.load(file)

            self.__items = loaded_items
            return True

        except:
            self.__items = []
            return False