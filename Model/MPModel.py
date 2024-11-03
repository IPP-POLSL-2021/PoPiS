class Mp:
    def __init__(self, club, districtName, educationLevel, numberOfVotes, profession, voivodeship) -> None:
        self.club = club
        self.districtName = districtName
        self.educationLevel = educationLevel
        self.numberOfVotes = numberOfVotes
        self.profession = profession
        self.voivodeship = voivodeship
        pass

    def __str__(self) -> str:
        base = f" był w klubie {self.club}, został wybrany z okręgu {self.districtName} znajdującym się w woj. {self.voivodeship}, miał wykształcenie {self.educationLevel} "
        if self.numberOfVotes != 0:
            base += f" , otrzymał {self.numberOfVotes} głosów "
        if self.profession is None:
            base += " poczas tej kadecji poseł nie pełnił żadenej profesji "
        else:
            base += f" podczas tej kadencji poseł miał preofesje {self.profession}"
        return base
