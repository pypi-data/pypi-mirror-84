from .measurement import Measurement

def read(filename, headerline = False, col = 0, totalcol = 1):
    #Reads the data from the file.
    #The file MUST have only the raw data
    with open(filename, 'r') as f:
        s = f.read()
        if headerline:
            s = s.split('\n', 1)[1]
        #For European/Brazilian number notation
        s = s.replace(",", ".")
        data = [float(val) for i, val in enumerate(s.split()) if i%totalcol == col]
    return data

#The standard deviation of the mean
def sigma_m(data):
    l = len(data)
    av = sum(data)/l
    return ( sum([(x-av)**2 for x in data])/((l-1)*l) ) ** 0.5

def create(filename):
    data = read(filename)
    return Measurement( sum(data)/len(data), sigma_m(data) )