# encoding: utf-8
import sys
import yaml

""" Parent class of Serenaded / Serenader """
class __Parent_Serenade:
    def __init__(self, name : str):
        self.__name: str = name
        self.__rank: list = [] # rank of the preferred member of the other group, less is better

    def get_name(self):
        return self.__name

    def get_rank(self):
        return self.__rank

    def set_rank(self, rank : list):
        self.__rank = rank

""" Represents a Serenader """
class Serenader(__Parent_Serenade):
    def get_name_of_first(self):
        return next(iter(self.get_rank())).get_name()

    def serenade(self):
        next(iter(self.get_rank())).rank_serenader(self)

    def refused(self):
        self.get_rank().pop(0)

""" Represents a Serenaded """
class Serenaded(__Parent_Serenade):
    def __init__(self, name: str, nmax : int):
        super().__init__(name)
        self.__nmax : int = nmax
        self.__serenades : dict = {} # contains {serenader_rank : serenader}

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
        for rank in sorted(self.__serenades):
            if accepted_serenaders < self.get_nmax():
                accepted_serenaders += 1
            else:
                self.__serenades[rank].refused()

""" Check integrity of the YAML source file """
def check_yaml(sources):
    print("********************************")
    print("Checking YAML file integrity...")
    if "group1_serenading" not in sources.keys():
        print("missing group1_serenading boolean")
        sys.exit(-1)
    if "group1" not in sources.keys():
        print("missing group1 list")
        sys.exit(-1)
    if "group2" not in sources.keys():
        print("missing group2 list")
        sys.exit(-1)
    group1_serenading : bool = sources["group1_serenading"]
    group1 : list = sources["group1"]
    group2 : list = sources["group2"]
    for i in range(len(group1)):
        for key in ["name", "rank", "nmax"] if not group1_serenading else ["name", "rank"]:
            if key not in group1[i]:
                print(f"{key} key missing in group1, element {i}")
                sys.exit(-1)
    for i in range(len(group2)):
        for key in ["name", "rank", "nmax"] if group1_serenading else ["name", "rank"]:
            if key not in group2[i]:
                print(f"{key} key missing in group2, element {i}")
                sys.exit(-1)

    if len( list(element["name"] for element in group1) ) != len( set(element["name"] for element in group1) ):
        print("group1 has duplicate")
        sys.exit(-1)

    if len( list(element["name"] for element in group2) ) != len( set(element["name"] for element in group2) ):
        print("group2 has duplicate")
        sys.exit(-1)

    group1_names : set = set(element["name"] for element in group1)
    group2_names : set = set(element["name"] for element in group2)
    for element in group1:
        for rank_element in element["rank"]:
            if rank_element not in group2_names:
                print(f"{rank_element} not in group2 names")
                sys.exit(-1)
    for element in group2:
        for rank_element in element["rank"]:
            if rank_element not in group1_names:
                print(f"{rank_element} not in group1 names")
                sys.exit(-1)

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

""" Our implementation of stable marriage algorithm :) """
def stable_marriage_algorithm(sources):
    serenaders: dict = {} # contains {serenader_name : serenader_object}
    serenadeds: dict = {} # contains {serenaded_name : serenaded_object}
    """ Decode sources """
    group1_serenading : bool = sources["group1_serenading"]
    group1_elements : list = sources["group1"]
    group2_elements : list = sources["group2"]
    """ Fill serenaders/serenadeds dictionaries 
    Then, fill serenaders/serenadeds rank dictionaries """
    if group1_serenading:
        for element1, element2 in zip(group1_elements, group2_elements):
            serenaders[element1["name"]] = Serenader(element1["name"])
            serenadeds[element2["name"]] = Serenaded(element2["name"], element2["nmax"])
        for element1, element2 in zip(group1_elements, group2_elements):
            serenaders[element1["name"]].set_rank([serenadeds[element1["rank"][rank_key]] for rank_key in sorted(element1["rank"])])
            serenadeds[element2["name"]].set_rank([serenaders[element2["rank"][rank_key]] for rank_key in sorted(element2["rank"])])
    else:
        for element1, element2 in zip(group1_elements, group2_elements):
            serenadeds[element1["name"]] = Serenaded(element1["name"], element1["nmax"])
            serenaders[element2["name"]] = Serenader(element2["name"])
        for element1, element2 in zip(group1_elements, group2_elements):
            serenadeds[element1["name"]].set_rank([serenaders[element1["rank"][rank_key]] for rank_key in sorted(element1["rank"])])
            serenaders[element2["name"]].set_rank([serenadeds[element2["rank"][rank_key]] for rank_key in sorted(element2["rank"])])

    """ Loop the algorithm till its end """
    serenade_end : bool = False
    while not serenade_end:
        serenade_end = True
        """ First, each serenader has to serenade """
        for serenader in serenaders.values():
            serenader.serenade()
        """ Next, each serenaded replies to his serenaders """
        for serenaded in serenadeds.values():
            serenaded.reply_to_serenaders()
        """ Finally, if a serenaded has less serenades than his nmax, we do another loop """
        for serenaded in serenadeds.values():
            if serenaded.get_nmax() > serenaded.get_nb_serenades():
                serenade_end = False
            serenaded.reset_serenades()

    """ Print results """
    for serenader in serenaders.values():
        print(f"{serenader.get_name()} : {serenader.get_name_of_first()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You have to specify a YAML source file!")
        sys.exit(-1)

    try:
        sources = yaml.load(open(sys.argv[1]), Loader=yaml.Loader)
    except FileNotFoundError:
        print("The specified file is incorrect.")
        sys.exit(-1)

    #check_yaml(sources)
    stable_marriage_algorithm(sources)