class Estado():

	"""

		Clase definitoria de un estado para un AFN o un AFD

			nombre: 		Nombre del estado
			transiciones:	Diccionario que define las transiciones del estado con otros estados, la llave es un síbolo del alfabeto y los elementos descritos por la llave los estados a los que transiciona
			aceptacion:		Valor Booleano lo denota como estado de aceptación

	"""

	def __init__(self, nombre, transiciones = {} , aceptacion = False, inicial = False):
		self._nombre = nombre
		self._transiciones = transiciones
		self._aceptacion = aceptacion
		self._inicial = inicial

	# Getters

	def getNombre(self):
		return self._nombre

	def getTransiciones(self):
		return self._transiciones

	def isAceptacion(self):
		return self._aceptacion

	def isInicial(self):
		return self._inicial

	# Setters

	def setNombre(self, nombre):
		self._nombre = nombre

	def setTransiciones(self, transiciones):
		self._transiciones = transiciones

	def setAceptacion(self, aceptacion = True):
		self._aceptacion = aceptacion

	def setInicial(self, inicial = True):
		self._inicial = inicial

	def agregarTransicion(self, simbolo, estados = []):
		if simbolo in self._transiciones:
			for estado in estados:
				if estado not in self._transiciones[simbolo]:
					self._transiciones[simbolo].append(estado)
		else:
			self._transiciones[simbolo] = estados

	# Operaciones

	def mover(self, simbolo):
		""" Operación que retorna un conjunto de estados al que transiciona un estado con el símbolo dado

			@param simbolo: string
			@returns transiciones[simbolo] : list(Estado)"""

		return self._transiciones[simbolo]


class Automata():
	"""

		Clase definitoria de un Automata y los elementos que lo componen:

			nombre: 	Nombre para identificación del autómata
			estados: 	Lista del conjunto de objetos tipo Estado
			alfabeto: 	Conjunto de símbolos que conforman al alfabeto del Automata

	"""

	def __init__(self, nombre, estados = [], alfabeto = []):
		self._nombre = nombre
		self._estados = []
		self._alfabeto = []

	# Getters

	def getNombre(self):
		return self._nombre

	def getEstados(self):
		return self._estados

	def getAlfabeto(self):
		return self._alfabeto

	def getEstado(self, nombre):
		for estado in self._estados:
			if estado.getNombre() == nombre:
				return estado
			else:
				return None

	def getEstadosAceptacion(self):
		estadosAceptacion = []

		for estado in self._estados:
			if estado.isAceptacion():
				estadosAceptacion.append(estado)

		return estadosAceptacion

	def getEstadoInicial(self):
		for estado in self._estados:
			if estado.isInicial():
				return estado

	def inAlfabeto(self, simbolo):
		return simbolo in self._alfabeto

	# Setters

	def setEstados(self, estados):
		self._estados = estados

	def setAlfabeto(self, alfabeto):
		self._alfabeto = alfabeto

	def agregarEstado(self, estado):
		""" Método que permite agregar un estado al conjunto perteneciente al Autómata

			@param estado: Estado
			@returns 0 : en caso correcto // -1 : estado no es una instancia de la clase Estado """

		if type(estado) == Estado and estado not in self._estados:
			self._estados.append(estado)
			return 0

		return -1

	def agregarEstados(self, estados):

		for estado in estados:
			if estado not in self._estados:
				self._estados.append(estado)

	def agregarSimboloAlfabeto(self, simbolo):
		""" Método que permite agregar un símbolo al Alfabeto perteneciente al Autómata

			@param simbolo: string
			@returns 0 : en caso correcto // -1 : el símbolo ya es parte del Alfabeto """

		if simbolo not in self._alfabeto:
			self._alfabeto.append(simbolo)
			return 0

		return -1

	def setEstadoInicial(self, estado):
		estado.setInicial()

		for estados in self._estados:
			if estados.isInicial():
				estados.setInicial(False)

		self._estados.append(estado)

	# Operaciones

	def imprimirAutomataConsola(self):

		print('Automata: ' + self._nombre + '\n')
		#Se imprime el estado inicial y sus transiciones

		estadosAceptacion = []

		#Se imprimen los demás estados
		for estado in self._estados:
			if estado.isAceptacion():
				estadosAceptacion.append(estado)

			else:
				print(estado.getNombre() + ': ', end='')

				for simbolo,es in estado.getTransiciones().items():
					print('{' + simbolo + '=>',end='')

					for n in es:
						print(',' + n.getNombre(),end='')

					print('}')

			#Finalmente los estados de aceptación
			for aceptacion in estadosAceptacion:
				print(aceptacion.getNombre() + '(f): ',end='')
				print(aceptacion.getTransiciones())

			estadosAceptacion.clear()

			print('>>>>>>>>>>>>>>>>>>>>>>\n')


	def eliminarEstado(self,estado):
		self._estados.remove(estado)

	def renombreAutomaticoEstados(self,letra):

		numero = 0
		pilaRevisados = []
		pilaPendientes = []
		estadoInicial = self.getEstadoInicial()

		estadoInicial.setNombre(letra + str(numero))

		pilaRevisados.append(estadoInicial)

		for simbolo,estados in estadoInicial.getTransiciones().items():
			for estado in estados:
				if estado not in pilaRevisados:
					pilaPendientes.append(estado)

		while pilaPendientes:
			estadoAux = pilaPendientes.pop()

			pilaRevisados.append(estadoAux)

			if not estadoAux.isAceptacion():
				numero += 1
				estadoAux.setNombre(letra + str(numero))
			else:
				estadoAux.setNombre(letra + 'f')

			for simbolo,estados in estadoAux.getTransiciones().items():
				for estado in estados:
					if estado not in pilaRevisados:
						pilaPendientes.append(estado)

		if not pilaPendientes and len(pilaPendientes) == len(self._estados):
			return 0,'Renombre Correcto'
		else:
			return -1,'Error en el Renombre'



class AFN(Automata):

	"""

		Clase definitoria de un AFN

	"""

	def __init__(self, nombre, estados =[], alfabeto = []):
		Automata.__init__(self, nombre, estados, alfabeto)

	def cerraduraEpsilon(self, estados = []):
		""" Caso especial de la operación mover donde se obtienen el número máximo de estados que transicionan desde el primer estado con 'ɛ' como símbolo

			@param estados : lista de estados que transicionan con ɛ
			@returns 0: en caso correcto // -1 : en un error en el proceso de la operación
			El resultado de los estados que transicionan con 'ɛ' se agregarán a la lista 'estados' pasada como parámetro
		"""
		pass


class AFD(Automata):

	"""

		Clase definitori de una AFD

	"""
	def __init__(self, nombre, estados = [], alfabeto = []):
		Automata.__init__(self, nombre, estados, alfabeto)