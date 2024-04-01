


#Prevent user from deleting or writing from output
def on_key(event):
    if event.keysym in ["BackSpace", "Delete"]:
        return 'break'
    elif event.char:
        return 'break'


#Prevent user from write non-float or int
def validate_num(value):
    try:
        if value == "" :
            return True #Allow empty string
        float(value) # Try convert to float
        return True
    except ValueError:
        return False