from functools import reduce


class DecisionTable():
    @staticmethod
    def printRules(rules):
        print("Rules:")
        for i, rule in enumerate(rules):
            for condition in rule:
                print(f"({condition[0]}={condition[1]})", end="")
            if(i != len(rules)-1):
                print(" OR")
            else:
                print()

    @staticmethod
    def extractUsedAttributes(rules, verbose=False):
        usedAttributes = set()
        for rule in rules:
            for condition in rule:
                usedAttributes.add(condition[0])
        if verbose:
            print("Used attributes:")
            print(usedAttributes)
        return usedAttributes

    def __init__(self, attributes):
        self.currObjId = 0
        self.attributes = {}
        self.attributesInv = {}
        for attribute in attributes:
            self.attributes[attribute] = {}
            self.attributesInv[attribute] = {}

    def getAllObjects(self):
        for _, dictionary in self.attributes.items():
            return frozenset(dictionary.keys())

    def insertObject(self, valuesDict):
        objId = self.currObjId
        self.currObjId += 1
        for attribute, value in valuesDict.items():
            self.attributes[attribute][objId] = value
            if not value in self.attributesInv[attribute]:
                self.attributesInv[attribute][value] = frozenset()
            self.attributesInv[attribute][value] = self.attributesInv[attribute][value].union([
                                                                                              objId])

    def tBlock(self, condition):
        return self.attributesInv[condition[0]][condition[1]]

    def TSquare(self, conditions):
        objs = self.getAllObjects()
        for condition in conditions:
            objs = objs & self.tBlock(condition)
        return objs

    def getAllConditions(self):
        return [(attr, val) for attr in self.attributes.keys() for val in self.attributesInv[attr].keys()]

    def show(self):
        print(self.currObjId)
        print(self.attributes)
        print(self.attributesInv)

    def getObjectsSatisfyingConditions(self, conditions):
        return reduce(lambda A, B: A | B, [self.attributesInv[condition[0]][condition[1]]for condition in conditions], frozenset())

    def getRulesForObjects(self, objs, verbose=False):
        XObjs = frozenset(objs)
        G = frozenset(objs)
        Tau = frozenset()
        while G:
            T = frozenset()
            TG = {t for t in self.getAllConditions() if self.tBlock(t) & G}
            while not T or not (self.TSquare(T) <= XObjs):
                helper = [(t, len(self.tBlock(t)), len(self.tBlock(t) & G))
                          for t in TG]
                maxIntersectionVal = max(helper, key=lambda x: x[2])[2]
                helper = [elem for elem in helper if elem[2]
                          == maxIntersectionVal]
                t = min(helper, key=lambda x: x[1])[
                    0] if len(helper) > 1 else helper[0][0]
                T = T | {t}
                G = G & self.tBlock(t)
                TG = {t for t in self.getAllConditions() if self.tBlock(t)
                      & G} - T
            for t in T:
                if(self.TSquare(T-{t}) <= XObjs):
                    T = T - {t}
            Tau = Tau | {T}
            G = XObjs - reduce(lambda A, B: A | B,
                               [self.TSquare(T) for T in Tau], frozenset())
        TauCopy = frozenset(Tau)
        for T in Tau:
            if reduce(lambda A, B: A | B, [self.TSquare(
            Tprim) for Tprim in Tau - {T}], frozenset()) == XObjs:
                Tau = Tau - {T}
        if verbose:
            DecisionTable.printRules(Tau)
        return Tau


if __name__ == "__main__":
    exampleDecisionTable = DecisionTable(["fever", "headache"])
    exampleDecisionTable.insertObject({"fever": "high", "headache": True})
    exampleDecisionTable.insertObject({"fever": "low", "headache": True})
    exampleDecisionTable.insertObject({"fever": "low", "headache": False})
    exampleDecisionTable.insertObject({"fever": "medium", "headache": True})
    exampleDecisionTable.insertObject({"fever": "medium", "headache": False})
    exampleDecisionTable.insertObject({"fever": "high", "headache": False})

    print("Lem2 output:")
    rules = exampleDecisionTable.getRulesForObjects([0, 3, 5], verbose=True)

    DecisionTable.extractUsedAttributes(rules, verbose=True)

    print(exampleDecisionTable.getObjectsSatisfyingConditions(
        [("fever", "low"), ("fever", "high")]))
