class GeneralUser:
    def __init__(self, username:str, email:str, password:str) -> None:
        self.username:str = username
        self.email:str = email
        self.password:str = password

    def __str__(self):
        return f"name: {self.username} contact: {self.email}" #str conversion
    
class TradieUser:
    def __init__(self, username:str, email:str, password:str, trade:str, hourlyRate:float, calloutFee:float, certified:bool=False) -> None:
        self.username:str = username
        self.email:str = email
        self.password:str = password
        self.trade:str = trade
        self.hourlyRate:float = hourlyRate
        self.calloutFee:float = calloutFee
        self.certified:bool = certified #functionality which allows the user to be considered certified through external process if they provide their valid trade license

    def __str__(self):
        return f"name: {self.username} trade: {self.trade} contact: {self.email}, Rate = {self.calloutFee} + {self.hourlyRate} per hour." #str conversion

class Location:
    def __init__(self, streetNumber:str, street:str, suburb:str, postcode:str, state:str) -> None:
        self.streetNumber:str = streetNumber
        self.street:str = street
        self.suburb:str = suburb
        self.postcode:str = postcode
        self.state:str = state

    def __str__(self):
        return f"{self.streetNumber} {self.street}, {self.suburb}, {self.state}, {self.postcode}" #str conversion
    

class JobRequest:
    def __init__(self, requestor:GeneralUser, job:str, description:str, location:Location, dateCreated:str, timeCreated:str) -> None:
        self.userName:str = requestor.username
        self.userEmail:str = requestor.email
        self.job:str = job
        self.description:str = description
        self.location:Location = location
        self.dateCreated:str = dateCreated #date format: dd/mm/yyyy
        self.timeCreated:str = timeCreated #time format: hh:mm

class JobOffer:
    def __init__(self, tradie:TradieUser, jobRequest:JobRequest, dateOffered:str, timeOffered:str, timeEstimate:float) -> None:
        self.tradieName:str = tradie.username
        self.tradieEmail:str = tradie.email
        self.jobRequest:str = jobRequest
        self.timeEstimate:float = timeEstimate
        self.costEstimate:float = tradie.calloutFee + tradie.hourlyRate * timeEstimate
        self.dateOffered:str = dateOffered #date format: dd/mm/yyyy
        self.timeOffered:str = timeOffered #time format: hh:mm