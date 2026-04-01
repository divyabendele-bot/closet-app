class Closet:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_all_items(self):
        return self.items

    def get_items_by_category(self, category):
        return [item for item in self.items if item.get_category() == category]

    def get_items_by_style(self, style):
        return [item for item in self.items if item.get_style() == style]

    def get_items_by_season(self, season):
        return [item for item in self.items if item.get_season() == season]

    def count_items(self):
        return len(self.items)

    def remove_item_by_name(self, name):
        index = 0

        while index < len(self.items):
            if self.items[index].get_name().lower() == name.lower():
                removed_item = self.items.pop(index)
                return removed_item
            index += 1

        return None