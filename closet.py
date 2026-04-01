class Closet:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_all_items(self):
        return self.items

    def count_items(self):
        return len(self.items)

    def get_item_names(self):
        names = []
        for item in self.items:
            names.append(item.get_name())
        return names

    def get_item_by_name(self, name):
        index = 0

        while index < len(self.items):
            if self.items[index].get_name() == name:
                return self.items[index]
            index += 1

        return None

    def remove_item_by_name(self, name):
        index = 0

        while index < len(self.items):
            if self.items[index].get_name() == name:
                removed_item = self.items.pop(index)
                return removed_item
            index += 1

        return None

    def get_items_sorted_by_name(self):
        return sorted(self.items, key=lambda item: item.get_name().lower())

    def get_filtered_items(self, category="All", occasion="All", weather="All"):
        filtered_items = []

        for item in self.items:
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