from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase


class Robot(object):
	def __init__(self):
		self.core = EV3Brick()
		self.right_motor = Motor(Port.C)
		self.stick_motor = Motor(Port.B)
		self.left_motor = Motor(Port.A)

		self.robot = DriveBase(self.left_motor, self.right_motor, 55.5, 104)

	def forward(self, milimeters: int) -> None:
		self.robot.straight(milimeters)
		return "done"

	def backward(self, milimeters: int) -> None:
		self.robot.straight(-milimeters)
		return "done"

	def turn_right(self, angle: int) -> None:
		self.robot.turn(angle)
		return "done"

	def turn_left(self, angle: int) -> None:
		self.robot.turn(-angle)
		return "done"

	def stick_up(self, angle: int, speed=100) -> None:
		self.stick_motor.run_angle(speed, angle)
		return "done"

	def stick_down(self, angle: int, speed=100) -> None:
		self.stick_motor.run_angle(speed, -angle)
		return "done"
		
	def get_nsium(self) -> str:
		print("Analise du sol")
		return str(random.randint(0, 100))

	def get_wall_distance(self) -> str:
		print("Analise de l'environnement")
		return str(random.randint(0, 2500))



ROBOT_ACTIONS = { "motor", "rotate", "stick", "capteur" }
ROBOT_DIRECTION = { "up", "down", "left", "right", "nsium%", "walldistance" }


class Request(object):
	"""
	A Request object have 5 attributes:
		-raw_content: The list of all the headers 
		-action: The action submitted (should be either "GET" or "POST")
		-path: The path requested
		-protocol: The protocol and the version of transmission
		-headers: A dict listing all the headers
	"""
	def __init__(self, raw_request: str):
		self.raw_content = [line for line in raw_request.split('\n')]

		if not self.is_valid_request(raw_request):
			raise RequestError()

		self.action = self.raw_content[0].split(' ')[0]

		if not self._check_command(self.raw_content[2]):
			raise ActionError()

	def _check_command(self, command: str) -> bool:
		"""
		Vérifie qu'une requête contient bien une commande valide
		:param command: le texte brut
		:type command: str
		:return: si la commande est valide ou non
		:rtype: bool
		"""
		content = command.split(":")
		print(content)
		if len(content) != 2:
			return False

		"""if self.action == "GET":
									if content[0] in ROBOT_ACTIONS:
										return True"""

		action = content[0].split("_")
		if len(action) != 2:
			return False
		if action[0] not in ROBOT_ACTIONS:
			return False
		if action[1] not in ROBOT_DIRECTION:
			return False

		return True

	def extract_action(self) -> tuple:
		"""
		Extrait ce que l'on a besoin pour effectuer l'action requise

		:return: (action, direction, value)
		"""
		data = self.raw_content[2].split("_")  # if self.action == "DO" else (None, self.raw_content[2])
		action = data[0]
		option = data[1].split(":")[0]
		value = data[1].split(":")[1]

		return (action, option, value)

	@classmethod
	def is_valid_request(self, content: str) -> bool:
		"""
		Détermine si une requête est une requête NSITTP ou non
		:param content: la requête
		:type content: str
		:return: si la requête est valide ou non
		:rtype: bool
		"""
		request = [line for line in content.split('\n')]
		if len(request) != 3:
			return False

		first_line = request[0].split(' ')
		if len(first_line) != 3:
			return False
		if first_line[0] not in { "GET", "DO" }:
			return False
		if first_line[2] != "NSITTP":
			return False

		second_line = request[1]
		if second_line != '.':
			return False

		return True



class ActionError(Exception):
	def __str__(self):
		return "L'action donnée n'est pas une action valide"

class RequestError(Exception):
	def __str__(self):
		return "La requête donnée n'est pas une requête NSITTP."
