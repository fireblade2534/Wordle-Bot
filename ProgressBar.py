import math



    
class ProgressBar:
    def __init__(self,Length:int,Start,End,ShowPrecent=True,SmoothBar=True,Name=""):
        self.Length=Length
        self.Start=Start
        self.End=End
        self.ShowPrecent=ShowPrecent

        self.Name=Name
        if self.Name != "":
            self.Name+=" "
        #print(self.Name)
        self.SmoothBar=SmoothBar
        self.SME=self.End - self.Start
        if self.Start > self.End:
            
            self.SME=self.Start - self.End 
            

    def Update(self,Current,Name="%NoChange%"):
        if Name == "%NoChange%":
            Name=self.Name
        #print(Name)
        MinFrom=0
        if self.Start > self.End:
            MinFrom=1
        Precent=max(min(abs(MinFrom - (Current / self.SME))* 100,100),0)

        PrecentStep=100 / self.Length
        PrecentSmoother=(Precent / PrecentStep) % 1
        
        Bar="█" * (math.floor(Precent / PrecentStep))
        if self.SmoothBar:
            if PrecentSmoother > 0.5:
                Bar+="▋"
            elif PrecentSmoother > 0.25:
                Bar+="▎"
        PrecentShow=""
        if self.ShowPrecent:
            PrecentShow=f" - {math.floor(Precent * 10) / 10}%"
        print(f"{Name}[{Bar.ljust(self.Length,' ')}]{PrecentShow}       ", end=' \r',flush=True)

    def EndProgressBar(self,Name="%NoChange%"):
        if Name == "%NoChange%":
            Name=self.Name
        PrecentShow=""
        if self.ShowPrecent:
            PrecentShow=f" - 100%"
        print(f"{Name}[{'█' * self.Length}]{PrecentShow} ...Done!", end=' \n',flush=True)