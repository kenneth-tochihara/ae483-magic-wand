# import copycat
from flight import *
from gui import *
# import spellcaster


# Create and start the client that will connect to the drone
client = SimpleClient(uri, use_controller=False, use_observer=False, channel=34)

# # Leave time at the start to initialize
# client.stop(1.0)

# # Take off and hover (with zero yaw)
# client.move(0.0, 0.0, 0.15, 0.0, 1.0)
# client.move(0.0, 0.0, 0.50, 0.0, 1.0)

# # Fly in a square five times (with a pause at each corner)
# num_squares = 5
# for i in range(num_squares):
#     client.move_smooth([0.0, 0.0, 0.5], [0.5, 0.0, 0.5], 0.0, 2.0)
#     client.move(0.5, 0.0, 0.5, 0.0, 1.0)
#     client.move_smooth([0.5, 0.0, 0.5], [0.5, 0.5, 0.5], 0.0, 2.0)
#     client.move(0.5, 0.5, 0.5, 0.0, 1.0)
#     client.move_smooth([0.5, 0.5, 0.5], [0.0, 0.5, 0.5], 0.0, 2.0)
#     client.move(0.0, 0.5, 0.5, 0.0, 1.0)
#     client.move_smooth([0.0, 0.5, 0.5], [0.0, 0.0, 0.5], 0.0, 2.0)
#     client.move(0.0, 0.0, 0.5, 0.0, 1.0)

# # Go back to hover (with zero yaw) and prepare to land
# client.move(0.0, 0.0, 0.50, 0.0, 1.0)
# client.move(0.0, 0.0, 0.15, 0.0, 1.0)

# # Land
# client.stop(1.0)

# # Disconnect from drone
# client.disconnect()

app = Applet(client)
app.mainloop()