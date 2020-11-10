class DecisionTable():
    def __init__(self, attributes):
        self.currObjId = 0
        self.attributes = {}
        self.attributesInv = {}
        for attribute in attributes:
            self.attributes[attribute] = {}
            self.attributesInv[attribute] = {}

    def getAllObjects(self):
        for attributeName, dictionary in self.attributes.items():
            return frozenset(dictionary.keys())  
        
    def insertObject(self, valuesDict):
        objId = self.currObjId
        self.currObjId += 1
        for attribute, value in valuesDict.items():
            self.attributes[attribute][objId] = value
            if not value in self.attributesInv[attribute]:
                self.attributesInv[attribute][value] = frozenset()
            self.attributesInv[attribute][value] = self.attributesInv[attribute][value].union([objId])

    def tBlock(self, condition):
        return self.attributesInv[condition[0]][condition[1]]
    
    def TSquare(self, conditions):
        # if len(conditions) == 0:
        #     return frozenset()
        objs = self.getAllObjects()
        for condition in conditions:
            objs = objs.intersection(self.tBlock(condition))
        return objs

    def getAllConditions(self):
        return [(attr, val) for attr in self.attributes.keys() for val in self.attributesInv[attr].keys() if attr != "decision"]


    def show(self):
        print(self.currObjId)
        print(self.attributes)
        print(self.attributesInv)


def lem2(objs, decisionTable):
    XObjs = frozenset(objs) #decisionTable.getAllObjects()
    G = frozenset(objs)
    Tau = frozenset()
    while G:
        T = frozenset()
        TG = {t for t in decisionTable.getAllConditions() if decisionTable.tBlock(t) & G}
        while (len (T) == 0) or (not (decisionTable.TSquare(T) <= XObjs)):
            helper = [(t, len(decisionTable.tBlock(t)), len(decisionTable.tBlock(t).intersection(G))) for t in TG]
            maxIntersectionVal = max(helper, key = lambda x: x[2])[2]
            helper = list(filter(lambda x : x[2] == maxIntersectionVal, helper))
            t = min(helper, key=lambda x : x[1])[0] if len(helper) > 1 else helper[0][0]
            T = T.union({t})
            G = G & decisionTable.tBlock(t)
            TG = {t for t in decisionTable.getAllConditions() if decisionTable.tBlock(t) & G} - T
        TCopy = frozenset(T)
        for t in TCopy:
            if decisionTable.TSquare(T - {t}) <= XObjs:
                T = T - {t}
        Tau = Tau | {T}
        TSquaresUnion = frozenset()
        TSquares = [decisionTable.TSquare(T) for T in Tau]
        for elem in TSquares:
            TSquaresUnion = TSquaresUnion | elem 
        G = XObjs - TSquaresUnion
    TauCopy = frozenset(Tau)
    for T in TauCopy:
        if frozenset([decisionTable.TSquare(Tprim) for Tprim in Tau - {T}]) == XObjs:
            Tau = Tau - {T}
    return Tau
        








exampleDecisionTable = DecisionTable(["fever", "headache", "decision"])
exampleDecisionTable.insertObject({"fever":"high", "headache": True, "decision": True})
exampleDecisionTable.insertObject({"fever":"low", "headache": True, "decision": False})
exampleDecisionTable.insertObject({"fever":"low", "headache": False, "decision":False})
exampleDecisionTable.insertObject({"fever":"medium", "headache": True, "decision":True})
exampleDecisionTable.insertObject({"fever":"medium", "headache": False, "decision":False})
exampleDecisionTable.insertObject({"fever":"high", "headache": False, "decision":True})

exampleDecisionTable.show()

print("Lem2 output:")
print(lem2([0,3,5], exampleDecisionTable))


