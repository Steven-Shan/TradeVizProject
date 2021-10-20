import tkinter as tkr
from win32con import BN_CLICKED

master = tkr.Tk()
master.geometry("200x100")
master.title("Dropdown List")

    
tkr.Label(master, text = "Countries").grid(row = 0)
clicked = tkr.StringVar()
clicked.set("Canada")
set1 = tkr.OptionMenu(master, clicked, "Canada", "Mexico", "Japan", "Germany", "China")

# Country Codes
# Canada:  1220
# Mexico:  2010
# Japan:   5880
# Germany: 4280
# China:   5700
set1.configure(font=("Arial", 25))
set1.grid(row = 1, column = 0)


tkr.mainloop()
country_import = clicked.get()
print(country_import)

country_code_values = 0
if(country_import == "Canada"):
    country_code_values = 1220
    
elif(country_import == "Mexico"):
    country_code_values = 2010
    
elif(country_import == "Japan"):
    country_code_values = 5880
    
elif(country_import == "Germany"):
    country_code_values = 4280
    
elif(country_import == "China"):
    country_code_values = 5700
    