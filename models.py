class ClothingItem:
    def __init__(self, name, category, occasions, weather_categories, image_data=None):
        self.__name = name
        self.__category = category
        self.__occasions = occasions
        self.__weather_categories = weather_categories
        self.__image_data = image_data

    # Getters
    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_occasions(self):
        return self.__occasions

    def get_weather_categories(self):
        return self.__weather_categories

    def get_image_data(self):
        return self.__image_data

    # Setters
    def set_occasions(self, new_occasions):
        if len(new_occasions) > 0:
            self.__occasions = new_occasions

    def set_weather_categories(self, new_weather_categories):
        if len(new_weather_categories) > 0:
            self.__weather_categories = new_weather_categories

    def display(self):
        occasions_text = ", ".join(self.__occasions)
        weather_text = ", ".join(self.__weather_categories)
        return f"{self.__name} ({self.__category}) | Occasions: {occasions_text} | Weather: {weather_text}"


class Top(ClothingItem):
    def __init__(self, name, occasions, weather_categories, image_data=None):
        super().__init__(name, "Top", occasions, weather_categories, image_data)


class Bottom(ClothingItem):
    def __init__(self, name, occasions, weather_categories, image_data=None):
        super().__init__(name, "Bottom", occasions, weather_categories, image_data)


class Shoes(ClothingItem):
    def __init__(self, name, occasions, weather_categories, image_data=None):
        super().__init__(name, "Shoes", occasions, weather_categories, image_data)


class Jacket(ClothingItem):
    def __init__(self, name, occasions, weather_categories, image_data=None):
        super().__init__(name, "Jacket", occasions, weather_categories, image_data)