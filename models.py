class ClothingItem:
    def __init__(self, name, category, style, color, season, image_path=None):
        self.__name = name              # encapsulated
        self.__category = category
        self.__style = style
        self.__color = color
        self.__season = season
        self.__image_path = image_path

    # Getters
    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_style(self):
        return self.__style

    def get_color(self):
        return self.__color

    def get_season(self):
        return self.__season

    def get_image_path(self):
        return self.__image_path

    # Setters
    def set_style(self, new_style):
        allowed_styles = ["Casual", "Chic", "Elegant", "Sporty"]
        if new_style in allowed_styles:
            self.__style = new_style
        else:
            print("Invalid style")

    def display(self):
        return f"{self.__name} ({self.__category}, {self.__style}, {self.__color}, {self.__season})"


class Top(ClothingItem):
    def __init__(self, name, style, color, season, image_path=None):
        super().__init__(name, "Top", style, color, season, image_path)


class Bottom(ClothingItem):
    def __init__(self, name, style, color, season, image_path=None):
        super().__init__(name, "Bottom", style, color, season, image_path)


class Shoes(ClothingItem):
    def __init__(self, name, style, color, season, image_path=None):
        super().__init__(name, "Shoes", style, color, season, image_path)


class Jacket(ClothingItem):
    def __init__(self, name, style, color, season, image_path=None):
        super().__init__(name, "Jacket", style, color, season, image_path)