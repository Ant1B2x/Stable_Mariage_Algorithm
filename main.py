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
        self.__nmax : int = nmax
        self.__serenades : dict = {} # serenaders_rank / serenaders

    def get_nmax(self):
        return self.__nmax

    def get_nb_serenades(self):
        return len(self.__serenades)

    def get_serenaders(self):
        return self.__serenades.values()

    def reset_serenades(self):
        self.__serenades = {}

    def __get_serenader_rank(self, serenader : Serenader):
        i = 0
        while i < len(self.get_rank()) and self.get_rank()[i] != serenader:
            i += 1
        return i

    def rank_serenader (self, serenader : Serenader):
        self.__serenades[self.__get_serenader_rank(serenader) - 1] = serenader

    def reply_to_serenaders(self):
        accepted_serenaders : int = 0
        for rank in sorted(self.__serenades.keys()):
            if accepted_serenaders < self.get_nmax():
                accepted_serenaders += 1
            else:
                self.__serenades[rank].refused()

class YAMLIntegrityError(Exception):
    pass

def stable_mariage_algorithm():
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

    serenade_end : bool = False
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

def check_yaml(sources):
    print("********************************")
    print("Checking YAML file integrity...")
    if "group1_serenading" not in sources.keys():
        print("missing group1_serenading boolean")
        raise YAMLIntegrityError
    if "group1" not in sources.keys():
        print("missing group1 list")
        raise YAMLIntegrityError
    if "group2" not in sources.keys():
        print("missing group2 list")
        raise YAMLIntegrityError
    group1_serenading : bool = sources["group1_serenading"]
    group1 : list = sources["group1"]
    group2 : list = sources["group2"]
    for i in range(len(group1)):
        for key in ["name", "rank", "nmax"] if not group1_serenading else ["name", "rank"]:
            if key not in group1[i]:
                print(f"{key} key missing in group1, element {i}")
                raise YAMLIntegrityError
    for i in range(len(group2)):
        for key in ["name", "rank", "nmax"] if group1_serenading else ["name", "rank"]:
            if key not in group2[i]:
                print(f"{key} key missing in group2, element {i}")
                raise YAMLIntegrityError

    if len( list(element["name"] for element in group1) ) != len( set(element["name"] for element in group1) ):
        print("group1 has duplicate")
        raise YAMLIntegrityError

    if len( list(element["name"] for element in group2) ) != len( set(element["name"] for element in group2) ):
        print("group2 has duplicate")
        raise YAMLIntegrityError

    group1_names : set = set(element["name"] for element in group1)
    group2_names : set = set(element["name"] for element in group2)
    for element in group1:
        for rank_element in element["rank"]:
            if rank_element not in group2_names:
                print(f"{rank_element} not in group2 names")
                raise YAMLIntegrityError
    for element in group2:
        for rank_element in element["rank"]:
            if rank_element not in group1_names:
                print(f"{rank_element} not in group1 names")
                raise YAMLIntegrityError

    for element in group1:
        if len(element["rank"]) < len(group2_names):
            print(f"not enough ranked values in group1, element {element['name']} ")
        elif len(element["rank"]) > len(group2_names):
            print(f"too many ranked values in group1, element {element['name']}")

    for element in group2:
        if len(element["rank"]) < len(group1_names):
            print(f"not enough ranked values in group2, element {element['name']} ")
        elif len(element["rank"]) > len(group1_names):
            print(f"too many ranked values in group2, element {element['name']}")

    if group1_serenading:
        for element in group1:
            if element["nmax"] < 1:
                print(f"nmax < 1 at group1, element {element['name']}")
            elif element["nmax"] > len(group2):
                print(f"nmax > group2 length at group1, element {element['name']}")
    else:
        for element in group2:
            if element["nmax"] < 1:
                print(f"nmax < 1 at group2, element {element['name']}")
            elif element["nmax"] > len(group1):
                print(f"nmax > group1 length at group2, element {element['name']}")
    print("********************************")

if __name__ == "__main__":
    sources = yaml.load(open("sources.yml"), Loader=yaml.Loader)
    check_yaml(sources)
    stable_mariage_algorithm()