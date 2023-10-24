import json
from functools import wraps
import hashlib
import multiprocessing
from multiprocessing import Pool
from ProgressBar import ProgressBar
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
def ComputeCode(Input,Correct):
    Output = ["0","0","0","0","0"]
    Check=list(Correct)
    for X,Y in enumerate(Input):
        if Y == Correct[X]:
            Check.remove(Y)
            Output[X]="2"

    for X,Y in enumerate(Input):
        if Y in Check and Y != Correct[X]:
            Check.remove(Y)
            Output[X]="1"

    return ["".join(Output),Correct]




class BotClass:
    def __init__(self,AllWords,Words) -> None:
        self.AllWords = AllWords
        self.Trimmed = Words
    
    def GenerateGroups(self,Word=None):

        BestWord=""
        BestGroups={}

        TrimmedHash=GetHash(Bot.Trimmed)
        PreComputed=GetPreCompute(TrimmedHash)
        if PreComputed == False or Word != None:
            
            
            BestGroupScore=0
            Bar=ProgressBar(28,0,len(self.AllWords),Name="Computing Best Guess")
            for Count,X in enumerate(self.AllWords):
                if Word == None or X == Word.lower():
                    #print(X)
                    Groups={}
                    with Pool(processes=4) as pool:
                        for Code in pool.starmap(ComputeCode,[(X,Y) for Y in self.Trimmed],chunksize=600):
                            #print(Code)
                            if Groups.get(Code[0]) == None:
                                Groups[Code[0]]=[]
                            Groups[Code[0]].append(Code[1])
                            
                    Bar.Update(Count)

                    
                    Trimed=set(Groups.keys()) 
                    #print(Trimed)
                    Total=(len(Trimed) * 4)# + (sum([243 - len(Groups[X]) for X in Trimed]) * 3) + (len([X for X in Groups if len(Groups[X]) == 1]) / len(Groups)) * 500
                    #Total=abs((len(self.Trimmed) / len(Trimed)) - (sum([list(Groups.keys()).count(X) for X in Trimed]) / len(Trimed)))

                    if Total > BestGroupScore:
                        BestGroupScore=Total
                        BestWord=X
                        BestGroups=Groups
            if Word == None:
                SavePreCompute(TrimmedHash,BestWord,BestGroups)
            Bar.EndProgressBar()
        else:
            BestWord=PreComputed["Word"]
            BestGroups=PreComputed["Groups"]
        return BestWord,BestGroups
    
    


        




            


if __name__ == "__main__":
    while True:
        AllWords = json.load(open("AllWords.txt", "r"))
        Words = json.load(open("Words.txt", "r"))


        Bot=BotClass(AllWords,Words)
        StartWord=None
        while True:
            Input=input("Inital Guess(Leave blank for it to compute one): ").lower()
            if Input == "":
                break
            if Input.lower().strip() in Bot.AllWords:
                StartWord=Input
                break
        BestGuess,BestGroups=Bot.GenerateGroups(StartWord)
        
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


            
            


            



        

