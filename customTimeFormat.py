from datetime import datetime,timedelta

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))
def generateCustomTimeFormat():
	return datetime.now().strftime("%I:%M %p") + ' on ' + custom_strftime("%B the {S}", datetime.now())