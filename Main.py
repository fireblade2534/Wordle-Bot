import json
from functools import wraps
import hashlib

def memoize(obj):
    cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

def GetHash(Input):
    return hashlib.sha256(str(Input).encode('utf-8')).hexdigest()

def GetPreCompute(Hash):
    try:
        File=open(f"PreComputed/{Hash}.txt","r")
        FC=json.load(File)
        File.close()
        return FC
    except:
        return False

def SavePreCompute(Hash,Word,Groups):
    File=open(f"PreComputed/{Hash}.txt","w")
    json.dump({"Word":Word,"Groups":Groups},File)
    File.close()



@memoize
def ComputeCode(Input,Correct,AsList=True):
    Output = [0 for _ in range(len(Input))]
    Check=list(Correct)
    for X,Y in enumerate(Input):
        if Y == Correct[X]:
            Check.remove(Y)
            Output[X]={"Letter":Y,"Code":2}

    for X,Y in enumerate(Input):
        if Y in Check and Y != Correct[X]:
            Check.remove(Y)
            Output[X]={"Letter":Y,"Code":1}
        elif Output[X] == 0:
            Output[X]={"Letter":Y,"Code":0}

    if not AsList:
        Output = "".join([str(X["Code"]) for X in Output])

    return Output




class BotClass:
    def __init__(self,AllWords,Words) -> None:
        self.AllWords = AllWords
        self.Trimmed = Words
    
    def GenerateGroups(self):

        BestWord=""
        BestGroups={}

        TrimmedHash=GetHash(Bot.Trimmed)
        PreComputed=GetPreCompute(TrimmedHash)
        if PreComputed == False:
            
            
            BestGroupScore=0

            for X in self.AllWords:
                Groups={}
                for Y in self.Trimmed:
                    Code=ComputeCode(X,Y,False)
                    if Groups.get(Code) == None:
                        Groups[Code]=[]
                    Groups[Code].append(Y)
                    
                    

                
                Trimed=set(Groups.keys()) 
                Total=(len(Trimed) * 4) + (sum([243 - len(Groups[X]) for X in Trimed]) * 3) + (len([X for X in Groups if len(Groups[X]) == 1]) / len(Groups)) * 500
                #Total=abs((len(self.Trimmed) / len(Trimed)) - (sum([list(Groups.keys()).count(X) for X in Trimed]) / len(Trimed)))

                if Total > BestGroupScore:
                    BestGroupScore=Total
                    BestWord=X
                    BestGroups=Groups
            SavePreCompute(TrimmedHash,BestWord,BestGroups)

        else:
            BestWord=PreComputed["Word"]
            BestGroups=PreComputed["Groups"]
        return BestWord,BestGroups
    
    


        




            


if __name__ == "__main__":
    while True:
        AllWords = json.load(open("AllWords.txt", "r"))
        Words = json.load(open("Words.txt", "r"))


        Bot=BotClass(AllWords,Words)

        BestGuess,BestGroups=Bot.GenerateGroups()
        
        while True:
            CurrentHash=GetHash(Bot.Trimmed)
            Chance=(len([X for X in BestGroups if len(BestGroups[X]) == 1]) / len(BestGroups)) * 100
            print("\n==================================================")
            print("Best Guess:",BestGuess)
            print("Remaining Words:",len(Bot.Trimmed))
            print("Number of groups:",len(BestGroups))
            print("Current Hash:",CurrentHash)
            print("Chance of geting answer:","{:.3f}%".format(Chance))
            print("==================================================")
            Input=""
            while 1:

                Input=input("Enter Code: ").strip()
                if len(Input) == 5 and all(T.isdigit() for T in Input) and Input in list(BestGroups.keys()):
                    break


            
            Bot.Trimmed=BestGroups[Input]
            if len(Bot.Trimmed) == 1:
                print("The word is:",Bot.Trimmed[0])
                input("\nPress Enter to continue")
                break
                
            #Bot.Trimmed=Bot.Trimmed.remove(BestGuess)
            BestGuess,BestGroups=Bot.GenerateGroups()


            
            


            



        

