
def selectvalidawaitime(waitime):

    if waitime <= 20 :
        waitime = 20
    else: 
        waitime = waitime
    
    return waitime



print(selectvalidawaitime(24))