from .h import *

def help():
  return f"Use {Green}PythonColouring.[any of options below]{Reset} to find out the options\n\nE.g. print(PythonColouring.settings())\n\n* settings\n* regular\n* bold\n* underline\n* background\n* high_intensity\n* bold_high_intensity\n* high_intensity_background"

def info():
  return f"Use {Green}PythonColouring.[any of options below]{Reset} to find out the options\n\nE.g. print(PythonColouring.settings())\n\n* settings\n* regular\n* bold\n* underline\n* background\n* high_intensity\n* bold_high_intensity\n* high_intensity_background"

def settings():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. reset = (PythonColouring.Reset)\n\n* Reset\n* {Underline}Underline{Reset}\n* {Italic}Italic{Reset}"

def regular():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. red = (PythonColouring.Red)\n\n* {Black}Black{Reset}\n* {Red}Red{Reset}\n* {Green}Green{Reset}\n* {Yellow}Yellow{Reset}\n* {Blue}Blue{Reset}\n* {Purple}Purple{Reset}\n* {Cyan}Cyan{Reset}\n* {White}White{Reset}"

def bold():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. darkBlue = (PythonColouring.BBlue)\n\n* {BBlack}BBlack{Reset}\n* {BRed}BRed{Reset}\n* {BGreen}BGReen{Reset}\n* {BYellow}BYellow{Reset}\n* {BBlue}BBlue{Reset}\n* {BPurple}BPurple{Reset}\n* {BCyan}BCyan{Reset}\n* {BWhite}BWhite{Reset}"

def underline():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. underlinePurple = (PythonColouring.UPurple)\n\n* {UBlack}UBlack{Reset}\n* {URed}URed{Reset}\n* {UGreen}UGreen{Reset}\n* {UYellow}UYellow{Reset}\n* {UBlue}UBlue{Reset}\n* {UPurple}UPurple{Reset}\n* {UCyan}UCyan{Reset}\n* {UWhite}UWhite{Reset}"

def background():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. yellow_background = (PythonColouring.On_Yellow)\n\n* {On_Black}On_Black{Reset}\n* {On_Red}On_Red{Reset}\n* {On_Green}On_Green{Reset}\n* {On_Yellow}On_Yellow{Reset}\n* {On_Blue}On_Blue{Reset}\n* {On_Purple}On_Purple{Reset}\n* {On_Cyan}On_Cyan{Reset}\n* {On_White}On_White{Reset}"

def high_intensity():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. HICyan = (PythonColouring.ICyan)\n\n* {IBlack}IBlack{Reset}\n* {IRed}IRed{Reset}\n* {IGreen}IGreen{Reset}\n* {IYellow}IYellow{Reset}\n* {IBlue}IBlue{Reset}\n* {IPurple}IPurple{Reset}\n* {ICyan}ICyan{Reset}\n* {IWhite}IWhite{Reset}"

def bold_high_intensity():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. BHIGreen = (PythonColouring.BIGreen)\n\n* {BIBlack}BIBlack{Reset}\n* {BIRed}BIRed{Reset}\n* {BIGreen}BIGreen{Reset}\n* {BIYellow}BIYellow{Reset}\n* {BIBlue}BIBlue{Reset}\n* {BIPurple}BIPurple{Reset}\n* {BICyan}BICyan{Reset}\n* {BIWhite}BIWhite{Reset}"

def high_intensity_background():
  return f"Use {Green}[Variable_name] = PythonColouring.[any of options below]{Reset} to set [Variable_name] to that colour\n\nE.g. HighWhiteBack = (PythonColouring.On_IWhite)\n\n* {On_IBlack}On_IBlack{Reset}\n* {On_IRed}On_IRed{Reset}\n* {On_IGreen}On_IGreen{Reset}\n* {On_IYellow}On_IYellow{Reset}\n* {On_IBlue}On_IBlue{Reset}\n* {On_IPurple}On_IPurple{Reset}\n* {On_ICyan}On_ICyan{Reset}\n* {On_IWhite}On_IWhite{Reset}"