class Game_Master(object):

    def __init__(self, colonies=None, colonists=None, member_lists=None):

        if not colonies:
            colonies = []

        if not colonists:
            colonists = []

        if not member_lists:
            member_lists = []

        self.colonies = colonies
        self.colonists = colonists
        self.colony_member_list = member_lists

    def add_colonist_to_colony(self, colonist, colony):
        if self.get_colonist_colony(colonist):
            return False
        else:
            self.colony_member_list[colony].append(colonist)
            return True

    def remove_colonist_from_colony(self, colonist):
        colony = self.get_colonist_colony(colonist)
        self.colonies[colony].remove(colonist)

    def get_colonist_colony(self, colonist):
        for colony in self.colony_member_list:
            if colonist in colony:
                return colony