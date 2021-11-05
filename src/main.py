# import copycat
from flight import *
from gui import *
# import spellcaster


# Create and start the client that will connect to the drone
client = SimpleClient(uri, use_controller=False, use_observer=False, channel=34)

app = Applet(client)
app.mainloop()