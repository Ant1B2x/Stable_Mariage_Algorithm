import yaml

class Generic_Serenade:
    def __init__(self, name : str):
        self.__name: str = name
        self.__rank: list = []

    def get_name(self):
        return self.__name

    def get_rank(self):
        return self.__rank

    def set_rank(self, rank : list):
        self.__rank = rank

class Serenader(Generic_Serenade):
    def get_name_of_first(self):
        return self.get_rank()[1].get_name()

    def serenade(self):
        self.get_rank()[1].rank_serenader(self)

    def refused(self):
        self.get_rank().pop(1)

class Serenaded(Generic_Serenade):
    def __init__(self, name: str, nmax : int):
        super().__init__(name)
        self.__nmax = nmax
        self.__nb_serenades: int = 0
        self.__serenaded_by : list = []

    def get_nmax(self):
        return self.__nmax

    def get_nb_serenades(self):
        return self.__nb_serenades

    def set_rank(self, rank : list):
        super().set_rank(rank)
        self.__serenaded_by = [False] * len(self.get_rank())

    def __get_serenader_rank(self, serenader : Serenader):
        i = 0
        while i < len(self.get_rank()) and self.get_rank()[i] != serenader:
            i += 1
        return i

    def rank_serenader (self, serenader : Serenader):
        self.__serenaded_by[self.__get_serenader_rank(serenader) - 1] = True
        self.__nb_serenades += 1

    def reply_to_serenaders(self):
        accepted_serenaders : int = 0
        for i in range(len(self.__serenaded_by)):
            if accepted_serenaders < self.__nmax and self.__serenaded_by[i]:
                accepted_serenaders += 1
            elif self.__serenaded_by[i]:
                self.get_rank()[i].refused()

    def reset_serenades(self):
        self.__nb_serenades = 0
        self.__serenaded_by = [False] * len(self.__serenaded_by)

    def get_serenaders(self):
        serenaders = []
        for i in range(len(self.__serenaded_by)):
            if self.__serenaded_by[i]:
                serenaders.append(self.get_rank()[i])
        return serenaders

serenader1 = Serenader("Esteban")
serenader2 = Serenader("Antoine")
serenader3 = Serenader("Yvan")

serenaded1 = Serenaded("N7", 1)
serenaded2 = Serenaded("X", 1)
serenaded3 = Serenaded("A7", 1)

serenader1.set_rank([serenaded2, serenaded1, serenaded3])
serenader2.set_rank([serenaded1, serenaded2, serenaded3])
serenader3.set_rank([serenaded1, serenaded2, serenaded3])

serenaded1.set_rank([serenader1, serenader3, serenader2])
serenaded2.set_rank([serenader2, serenader1, serenader3])
serenaded3.set_rank([serenader3, serenader1, serenader2])

serenade_end = False
while not serenade_end:
    serenade_end = True
    for serenader in [serenader1, serenader2, serenader3]:
        serenader.serenade()
    for serenaded in [serenaded1, serenaded2, serenaded3]:
        serenaded.reply_to_serenaders()
    for serenaded in [serenaded1, serenaded2, serenaded3]:
        if serenaded.get_nmax() > serenaded.get_nb_serenades():
            serenade_end = False
        serenaded.reset_serenades()

for serenader in [serenader1, serenader2, serenader3]:
    print(f"{serenader.get_name()} : {serenader.get_name_of_first()}")

sources = yaml.load(open("sources.yml"), Loader=yaml.Loader)
#check_yaml(sources)