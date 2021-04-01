"""
Ce fichier est le fichier exéctuté par le robot, il 
représente le serveur et attends des instructions
de la part d'un seul et unique client.
"""
import socket
import utils_robot


HOST = ("0.0.0.0", int(input("port: ")))

server = socket.socket()
server.bind(HOST)
server.listen(1)

robot = utils_robot.Robot()

ACTIONS = {
		'DO': {
			'motor': {
					'up': robot.forward,
					'down': robot.backward
					},
			'rotate': {
					'left': robot.turn_left,
					'right': robot.turn_right
					},
			'stick': {
					'up': robot.stick_up,
					'down': robot.stick_down
					}
			},

		'GET': {
			'none': None
			}
		}


while True:
	client, _ = server.accept()
	message = client.recv(1024).decode("utf-8")

	try:
		request = utils_robot.Request(message)
	except utils_robot.ActionError:
		client.send("action incorrect".encode("utf-8"))
		continue
	except utils_robot.RequestError:
		client.send("not NSITTP request".encode("utf-8"))
		continue

	command = request.extract_action()
	action = ACTIONS[request.action][command[0]][command[1]](int(command[2]))

	client.send(("ok " + action).encode("utf-8"))

server.close()
