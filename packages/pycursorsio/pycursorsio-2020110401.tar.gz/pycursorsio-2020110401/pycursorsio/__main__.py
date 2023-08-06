#!/usr/bin/env python3
#**************************************************************************
# Copyright (C) 2020 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
#**************************************************************************

import os.path as _path
import asyncio as _asyncio
import aiostream.stream as _aiostream
import websockets as _websockets
import pygame as _pygame

from enum import Enum as _Enum
from pygame.locals import *

# ---
# Game state utilities.
# ---

class Object:
	def __init__(self, id):
		self._id = id

	@property
	def id(self):
		return self._id

class TextObject(Object):
	def __init__(self, id, x, y, size, centered, text):
		super().__init__(id)

		self._x = x
		self._y = y
		self._size = size
		self._centered = centered
		self._text = text

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def size(self):
		return self._size

	@property
	def centered(self):
		return self._centered

	@property
	def text(self):
		return self._text

class WallObject(Object):
	def __init__(self, id, x, y, w, h, color):
		super().__init__(id)

		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._color = color

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def width(self):
		return self._w

	@property
	def height(self):
		return self._h

	@property
	def color(self):
		return self._color

class WarpObject(Object):
	def __init__(self, id, x, y, w, h, bad):
		super().__init__(id)

		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._bad = bad

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def width(self):
		return self._w

	@property
	def height(self):
		return self._h

	@property
	def bad(self):
		return self._bad

class ActivatorObject(Object):
	def __init__(self, id, x, y, w, h, count, color):
		super().__init__(id)

		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._count = count
		self._color = color

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def width(self):
		return self._w

	@property
	def height(self):
		return self._h

	@property
	def count(self):
		return self._count

	@property
	def color(self):
		return self._color

class Cursor:
	def __init__(self, id, x, y):
		self._id = id
		self._x = x
		self._y = y

	@property
	def id(self):
		return self._id

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

class DrawnLine:
	def __init__(self, start_x, start_y, end_x, end_y):
		self._sx = start_x
		self._sy = start_y
		self._ex = end_x
		self._ey = end_y

	@property
	def start_x(self):
		return self._sx

	@property
	def start_y(self):
		return self._sy

	@property
	def end_x(self):
		return self._ex

	@property
	def end_y(self):
		return self._ey

# ---
# Utilities.
# ---

class Assets:
	""" Class for loading assets. """

	def __init__(self):
		assets_folder = _path.join(_path.dirname(__file__), 'assets')

		self._fontpath = _path.join(assets_folder, 'NovaSquare.ttf')
		self._fontsizes = {}

		self._icon = _pygame.image.load(_path.join(assets_folder,
			'favicon.ico'))
		self._cursor = _pygame.image.load(_path.join(assets_folder,
			'cursor.png'))

	@property
	def icon(self):
		return self._icon

	@property
	def cursor(self):
		return self._cursor

	def font(self, size):
		if not size in self._fontsizes:
			self._fontsizes[size] = _pygame.font.Font(self._fontpath, size)
		return self._fontsizes[size]

class ReceivedMessageType(_Enum):
	""" The message type received from the server. """

	NONE = 0
	UNKNOWN = -1

	LEVEL = 1

class GameState:
	""" Manages the local game state. """

	def __init__(self):
		self._playerid = 0
		self._playercount = 0
		self._position = (0, 0)
		self._objects = []
		self._cursors = []
		self._lines = []
		self._lastmsg = ReceivedMessageType.NONE

	@property
	def player_id(self):
		return self._playerid

	@property
	def player_count(self):
		return self._playercount

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, value):
		# TODO: check with collisions

		self._position = value

	@property
	def objects(self):
		return iter(self._objects)

	@property
	def drawn_lines(self):
		return iter(self._lines)

	@property
	def cursors(self):
		return iter(self._cursors)

	@property
	def last_message_type(self):
		return self._lastmsg

	def process_message(self, data):
		""" Process a given frame. """

		_int = lambda x: int.from_bytes(x, 'little')
		_col = lambda x: ((x >> 16) & 255, (x >> 8) & 255, x & 255)
		packet_type = int(data[0])

		self._lastmsg = ReceivedMessageType.UNKNOWN

		if packet_type == 0:
			# Only contains four bytes.
			# Potentially client id?

			self._playerid = _int(data[1:5])
		elif packet_type == 1:
			# get game status?
			# [nbr, {i_32, i_16, i_16}, nbr_16, {i_32}, nbr_16, {i_32}[, opt_32]]

			print('packet 1:')

			self._cursors = []
			self._lines = []

			nbr = _int(data[1:3])
			data = data[3:]

			for i in range(nbr):
				o = i * 8 # offset

				id = _int(data[o:o+4])
				x = _int(data[o+4:o+6]) * 2
				y = _int(data[o+6:o+8]) * 2

				if id != self._playerid:
					self._cursors.append(Cursor(id, x, y))

				#print(f'  a[{i}] = [{_int(data[o:o+4])}, {_int(data[o+4:o+6])}, {_int(data[o+6:o+8])}]')

			data = data[nbr * 8:]
			nbr = _int(data[:2])
			data = data[2:]

			for i in range(nbr):
				i = i * 4 # offset
				print(f'  b[{i}] = [{_int(data[o:o+2])}, {_int(data[o+2:o+4])}]')

			data = data[nbr * 4:]
			nbr = _int(data[:2])
			data = data[2:]

			for i in range(nbr):
				o = i * 4 # offset
				print(f'  c[{i}] = [{_int(data[o:o+4])}]')

			data = data[nbr * 4:]
			nbr = _int(data[:2])
			data = data[2:]

			for i in range(nbr):
				o = i * 4 # offset
				print(f'  d[{i}] = [{_int(data[o:o+4])}]')

			data = data[nbr * 4:]
			nbr = _int(data[:2])
			data = data[2:]

			for i in range(nbr):
				o = i * 8 # offset

				sx = _int(data[o:o+2]) * 2
				sy = _int(data[o+2:o+4]) * 2
				ex = _int(data[o+4:o+6]) * 2
				ey = _int(data[o+6:o+8]) * 2

				self._lines.append(DrawnLine(sx, sy, ex, ey))

				#print(f'  e[{i}] = [{_int(data[o:o+2])}, {_int(data[o+2:o+4])}, {_int(data[o+4:o+6])}, {_int(data[o+6:o+8])}]')

			data = data[nbr * 8:]

			# Possiblement après, le nombre de joueurs connectés.
			self._playercount = 0
			if len(data) >= 4:
				self._playercount = _int(data[:4])
		elif packet_type == 4:
			# load the level!
			# [nbr, i_16, i_16, nbr_16, {variable}[, opt_16_32]]

			self._lastmsg = ReceivedMessageType.LEVEL
			self._position = (_int(data[1:3]) * 2, _int(data[3:5]) * 2)
			self._objects = []

			nobjects = _int(data[5:7])

			o = 7
			for i in range(nobjects):
				object_id = _int(data[o:o+4])
				object_type = _int(data[o+4:o+5])
				o += 5

				if object_type == 255:
					# This object is ignored in the original script.

					pass
				elif object_type == 0:
					# is a text object!

					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					size = _int(data[o+4:o+5])
					centered = bool(_int(data[o+5:o+6]) != 0)
					o += 6

					# read a NUL-terminated string

					find_result = data.find(b'\0', o)
					if find_result < 0: text_length = len(data) - o - 1
					text_length = find_result - o
					text_content = data[o:o + text_length].decode('ASCII')
					o += text_length + 1

					self._objects.append(TextObject(object_id,
						x, y, size, centered, text_content))
				elif object_type == 1:
					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					w = _int(data[o+4:o+6]) * 2
					h = _int(data[o+6:o+8]) * 2
					col = _int(data[o+8:o+12])
					o += 12

					self._objects.append(WallObject(object_id,
						x, y, w, h, _col(col)))
				elif object_type == 2:
					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					w = _int(data[o+4:o+6]) * 2
					h = _int(data[o+6:o+8]) * 2
					bad = bool(_int(data[o+8:o+9]) != 0)
					o += 9

					self._objects.append(WarpObject(object_id,
						x, y, w, h, bad))
				elif object_type == 3:
					# unknown object (probably activator while standing?)

					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					w = _int(data[o+4:o+6]) * 2
					h = _int(data[o+6:o+8]) * 2
					count = _int(data[o+8:o+10])
					color = _int(data[o+10:o+14])
					o += 14

					self._objects.append(ActivatorObject(object_id,
						x, y, w, h, count, _col(color)))
				elif object_type == 4:
					# unknown object (probably button on which to click on?)

					x = _int(data[o:o+2])
					y = _int(data[o+2:o+4])
					w = _int(data[o+4:o+6])
					h = _int(data[o+6:o+8])
					clicks = _int(data[o+8:o+10])
					count = _int(data[o+10:o+12])
					col = _int(data[o+12:o+16])
					o += 16

					print(f'  obj[{i}] is button (2)')
					print(f'    x = {x}')
					print(f'    y = {y}')
					print(f'    w = {w}')
					print(f'    h = {h}')
					print(f'    clicks = {clicks}')
					print(f'    count = {count}')
					print(f'    color = #{hex(col).zfill(6)}')
				else:
					print(f'  obj[{i}] has type {object_type}')

			#o = 7
			#for i in range(nbr):
			#	print(f'  a[{i}] = [{_int(data[o:o+4])}]')
			#	o += 4

			data = data[o:]
			print(f'  end = {data}')
		elif packet_type == 5:
			# [i_16, i_16, i_16_or_32]

			pass
		else:
			print(f"Unknown packet: {data}")
			return

# ---
# Main game function.
# ---

async def main():
	_pygame.init()

	assets = Assets()
	state = GameState()

	async with _websockets.connect("ws://128.199.12.58:2828") as ws:
		window = _pygame.display.set_mode((820, 620))
		window.fill((0, 0, 0))
		screen = window.subsurface((10, 10, 800, 600))

		_pygame.display.set_caption("cursors.io python client")
		_pygame.display.set_icon(assets.icon)
		_pygame.mouse.set_visible(False)

		def infotext(text, xy):
			x, y = xy
			surface = assets.font(12).render(text, True, (0, 0, 0))
			screen.blit(surface, (x, y - surface.get_height()))

		async def send_mouse_movement(x, y):
			msg = b'\1' + (x // 2).to_bytes(2, 'little')
			msg += (y // 2).to_bytes(2, 'little')
			msg += (1).to_bytes(2, 'little')
			msg += (1).to_bytes(2, 'little')
			await ws.send(msg)

		async def pygevts():
			""" async generator for pygame events. """

			yield _pygame.event.Event(NOEVENT)

			while True:
				event = _pygame.event.poll()
				if event.type == NOEVENT:
					await _asyncio.sleep(0.005)
					continue

				yield event

		async def wsevts():
			""" async generator for websocket events. """

			while True:
				message = await ws.recv()
				yield _pygame.event.Event(USEREVENT, message = message)

		# Main event loop.

		async with _aiostream.merge(wsevts(), pygevts()).stream() as streamer:
			async for event in streamer:
				if event.type == QUIT:
					break
				elif event.type == MOUSEMOTION:
					x, y = _pygame.mouse.get_pos()
					state.position = (x, y)
					await send_mouse_movement(*state.position)
				elif event.type == USEREVENT:
					state.process_message(event.message)
					if state.last_message_type == ReceivedMessageType.LEVEL:
						_pygame.mouse.set_pos(state.position)
				elif event.type == NOEVENT:
					pass
				else:
					continue

				# Display code.

				window.fill((0, 0, 0))
				screen.fill((255, 255, 255))

				for object in state.objects:
					if isinstance(object, TextObject):
						font = assets.font(object.size)
						rndr = font.render(object.text, True, (0, 0, 0))
						x, y = object.x, object.y
						if object.centered:
							x -= rndr.get_width() // 2
						y -= rndr.get_height()
						screen.blit(rndr, (x, y))
					elif isinstance(object, WallObject):
						x, y = object.x, object.y
						w, h = object.width, object.height
						color = object.color
						_pygame.draw.rect(screen, color, (x, y, w, h))
					elif isinstance(object, WarpObject):
						rect = _pygame.Surface((object.width, object.height))
						rect.fill((255, 0, 0) if object.bad else (0, 255, 0))
						rect.set_alpha(int(.2 * 255))
						screen.blit(rect, (object.x, object.y))
					elif isinstance(object, ActivatorObject):
						x, y = object.x, object.y
						w, h = object.width, object.height

						rect = _pygame.Surface((w, h))
						rect.fill(object.color)
						rect.set_alpha(int(.2 * 255))
						screen.blit(rect, (x, y))

						if w < 80 or h < 80:
							font = assets.font(30)
						else:
							font = assets.font(60)

						rndr = font.render(f"{object.count}", True,
							(0, 0, 0))
						rndr.set_alpha(int(.5 * 255))
						tx = x + w // 2 - rndr.get_width() // 2
						ty = y + h // 2 - rndr.get_height() // 2

						screen.blit(rndr, (tx, ty))

				infotext(f"{state.player_count} "
					"players online", (10, 590))

				for line in state.drawn_lines:
					_pygame.draw.line(screen, (121, 121, 121),
					   (line.start_x, line.start_y),
					   (line.end_x, line.end_y))

				for cursor in state.cursors:
					window.blit(assets.cursor, (10 + cursor.x, 10 + cursor.y))

				x, y = state.position
				window.blit(assets.cursor, (10 + x, 10 + y))

				_pygame.display.flip()

	_pygame.quit()

# Run the program.

_asyncio.run(main())

# End of file.
