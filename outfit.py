import random

class OutfitGenerator:
    def generate_outfit(self, style, closet):
        tops = []
        bottoms = []
        shoes = []
        jackets = []

        for item in closet.get_all_items():
            if item.style == style:
                if item.category == "Top":
                    tops.append(item)
                elif item.category == "Bottom":
                    bottoms.append(item)
                elif item.category == "Shoes":
                    shoes.append(item)
                elif item.category == "Jacket":
                    jackets.append(item)

        outfit = {}

        if tops:
            outfit["Top"] = random.choice(tops)
        if bottoms:
            outfit["Bottom"] = random.choice(bottoms)
        if shoes:
            outfit["Shoes"] = random.choice(shoes)
        if jackets:
            outfit["Jacket"] = random.choice(jackets)

        return outfit