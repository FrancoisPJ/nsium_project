"""
Interface assurant la liaison avec le robot
"""
import socket


class RobotConnexion(object):
	"""
	Objet symbolisant la connexion avec le robot
	via wifi
	"""
	def __init__(self, robot_ip: str, robot_port=6677):
		"""
		constructeur de la classe, on demande
		de spécifier l'ip du robot pour établir
		la connexion.

		:param robot_ip: une addresse ip valable
		:type robot_ip: str
		:syntax robot_ip: "x.x.x.x"
		:param port: le port sur lequel on va écouter
		:type port: int
		"""
		self.network_info = (robot_ip, robot_port)
		self.connexion = None


	def _start(self) -> bool:
		"""
		Méthode non-bloquante démarrant la connexion

		:return: si la connexion est prête ou non
		:rtype: bool
		"""
		self.connexion = socket.socket()
		self.connexion.settimeout(10)

		try:
			self.connexion.connect(self.network_info)
			return True

		except socket.error as error:
			return False


	def _stop(self) -> None:
		"""
		Arrêt de la connexion avec le robot
		"""
		self.connexion.close()


	def send(self, command: str) -> bool:
		"""
		Commande non-bloquante qui envoit une commande
		au robot, aucune réponse n'est attendue de la 
		part du robot.

		:param command: la commande à envoyer devant respecter
							les règles établies (cf discord)
		:type command: str
		:syntax command: "[MOVE]_[ACTION]:[DATA]"
		:return: True si la commande le robot à envoyé une confirmation de
					la récéption, False sinon
		:rtype: bool
		"""
		if not self._start():
			print("Une erreur lors de la connexion est survenue, et le message n'a pas pu être transmit.\nMerci de vérifier que le couple adresse, port est correct.")
			return None

		self.connexion.send(command.encode("utf-8"))

		try:
			output = self.connexion.recv(1024).decode("utf-8")

		except socket.error as error:
			return None

		self._stop()
		return output


def NSITTP_request(data: str, action: str) -> str:
	"""
	Créée une requête NSITTP valide suivant la 
	RFC 9999 (cf discord)

	:param data: les données à transformer en requête
	:type data: str
	:param action: l'action à effectuer ("DO" ou "GET")
	:type action: str
	:return: une requête NSITTP valide
	:rtype: str
	"""
	secret_key = "chocolatine"
	
	if action not in ("DO", "GET"):
		raise ValueError()


	return f"{action} {secret_key} NSITTP\n.\n{data}"
