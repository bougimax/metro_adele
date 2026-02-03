# Pour une pile on va vouloir créer plusieurs opérations:
# - faire_file_vide (init)
# - est_vide
# - enfiler
# - defiler


class File:
    def __init__(self):
        self.entrant = []
        self.sortant = []

    def est_vide(self):
        return len(self.entrant) == 0 and len(self.sortant) == 0

    def enfiler(self, element):
        self.entrant.append(element)

    def defiler(self):
        if len(self.sortant) == 0:
            for i in range(len(self.entrant)):
                self.sortant.append(self.entrant.pop())
        return self.sortant.pop()


# Demonstration
#
# file = File()
#
# for i in range(0, 10, 2):
#     file.enfiler(i)
#     print(f"J'ai enfilé {i}")
#
# print(f"La file ressemble à {file}")
#
# print(f"J'ai défilé {file.defiler()}")
#
# print(f"La file ressemble à {file}")
#
# for i in range(10, 20, 2):
#     file.enfiler(i)
#     print(f"J'ai enfilé {i}")
#
# print(f"La file ressemble à {file}")
#
# print(f"La pile {"est" if file.est_vide() else "n'est pas"} vide")
#
# while not file.est_vide():
#     print(f"J'ai défilé {file.defiler()}")
#
# print(f"La pile {"est" if file.est_vide() else "n'est pas"} vide")
