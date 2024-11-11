class Alarm:
    def __init__(self):
        self.state = "alarm_off"
        self.input_password = ""
    
    def setState(self, state):
        self.state = state

    def setPassword(self, password):
        self.password = password
        self.setState("password_set")
    
    def getPassword(self):
        return self.password
    
    def getMessage(self):
        if self.state == "get_password":
            return "Enter Password"
        if self.state == "password_set":
            return "Password Set"
        if self.state == "alarm_on":
            return "Alarm is on"
        if self.state == "alarm_off":
            return "Alarm is off"
        return "No state found"