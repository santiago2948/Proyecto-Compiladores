def firsRuele(rule):
        P={"B":["aSb", "BC", "e"], "B":["bC", "e"], "C":["d", "e"]}
        firstn={"S":["a", "b", "e", "d"], "B":["b", "e"], "C":["d", "e"]}
        first=[]
        for i in rule:
            if i in P:
                first.extend(firstn[i])
                if "e" in first: first.remove("e")
                if "e" not in firstn[i]: return first
            else:
                first.append(i)
                return first
        first.append("e")
        return first

print(firsRuele("BCf"))

for i in range(0, 1):
     inter= {"1"} & {"8"}
     print(len(inter))