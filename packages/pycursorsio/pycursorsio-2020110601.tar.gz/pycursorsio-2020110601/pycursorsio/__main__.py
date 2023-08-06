#!/usr/bin/env python3
#**************************************************************************
# Copyright (C) 2020 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
#**************************************************************************

from os import environ as _environ

_environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import os.path as _path
import math as _math
import asyncio as _asyncio
import aiostream.stream as _aiostream
import websockets as _websockets
import pygame as _pygame

from enum import Enum as _Enum
from time import monotonic as _monotonic
from pygame.locals import *

# ---
# Game state utilities.
# ---

class Text:
	def __init__(self, x, y, size, centered, text):
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

class Wall:
	def __init__(self, x, y, w, h, color = (0, 0, 0, 0)):
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._color = color

	def __repr__(self):
		attrs = ('x', 'y', 'width', 'height', 'color')
		attrs = ', '.join(f"{n} = {repr(getattr(self, n))}" for n in attrs)
		return f"{self.__class__.__name__}({attrs})"

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
	def w(self):
		return self._w

	@property
	def height(self):
		return self._h

	@property
	def h(self):
		return self._h

	@property
	def color(self):
		return self._color

class Warp:
	def __init__(self, x, y, w, h, bad):
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._bad = bad

	def __repr__(self):
		attrs = ('x', 'y', 'width', 'height', 'bad')
		attrs = ', '.join(f"{n} = {repr(getattr(self, n))}" for n in attrs)
		return f"{self.__class__.__name__}({attrs})"

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
	def w(self):
		return self._w

	@property
	def height(self):
		return self._h

	@property
	def h(self):
		return self._h

	@property
	def bad(self):
		return self._bad

class Detector:
	def __init__(self, x, y, w, h, count, color):
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._count = count
		self._color = color

	def __repr__(self):
		attrs = ('x', 'y', 'width', 'height', 'count', 'color')
		attrs = ', '.join(f"{n} = {repr(getattr(self, n))}" for n in attrs)
		return f"{self.__class__.__name__}({attrs})"

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
	def w(self):
		return self._w

	@property
	def height(self):
		return self._h

	@property
	def h(self):
		return self._h

	@property
	def count(self):
		return self._count

	@property
	def color(self):
		return self._color

class Button:
	def __init__(self, x, y, w, h, count, color, last_click):
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._count = count
		self._color = color
		self._lastclick = last_click

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
	def w(self):
		return self._w

	@property
	def height(self):
		return self._h

	@property
	def h(self):
		return self._h

	@property
	def count(self):
		return self._count

	@property
	def color(self):
		return self._color

	@property
	def last_click(self):
		return self._lastclick

	@property
	def pressed(self):
		return (self._lastclick is not None
			and (_monotonic() - self._lastclick) < .150)

class Cursor:
	def __init__(self, x, y):
		self._x = x
		self._y = y

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

class DrawnLine:
	def __init__(self, start_time, start_x, start_y, end_x, end_y):
		self._start = start_time
		self._current = start_time
		self._sx = start_x
		self._sy = start_y
		self._ex = end_x
		self._ey = end_y

	@property
	def alpha(self):
		elapsed = self._current - self._start
		fading_start = 0.0
		fading_end = 5.0

		value = (fading_end - elapsed) / (fading_end - fading_start)
		return min(max(value, 0.0), 1.0)

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

	def set_current_time(self, value):
		self._current = value

	def has_faded(self):
		return self.alpha == 0.0

class Click:
	def __init__(self, start_time, x, y):
		self._start = start_time
		self._current = start_time
		self._x = x
		self._y = y

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def advancement(self):
		elapsed = self._current - self._start
		fading_start = 0.0
		fading_end = 0.5

		value = (fading_end - elapsed) / (fading_end - fading_start)
		return 1 - min(max(value, 0.0), 1.0)

	@property
	def radius(self):
		return int(25 * self.advancement)

	@property
	def alpha(self):
		return 1.0 - self.advancement

	def set_current_time(self, value):
		self._current = value

	def has_faded(self):
		return self.advancement == 1.0

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
	POSITION = 2

class GameState:
	""" Manages the local game state. """

	def __init__(self):
		self._playerid = 0
		self._playercount = 0
		self._position = (0, 0)
		self._objects = {}
		self._cursors = {}
		self._lines = []
		self._clicks = []
		self._lastmsg = ReceivedMessageType.NONE

	@property
	def width(self):
		return 800

	@property
	def height(self):
		return 600

	@property
	def player_id(self):
		return self._playerid

	@property
	def player_count(self):
		return self._playercount

	@property
	def position(self):
		return self._position

	@property
	def objects(self):
		for obj in self._objects.values():
			yield obj

	@property
	def drawn_lines(self):
		curtime = _monotonic()
		for line in list(self._lines):
			line.set_current_time(curtime)
			if line.has_faded():
				self._lines.remove(line)
				continue

			yield line

	@property
	def clicks(self):
		curtime = _monotonic()
		for click in list(self._clicks):
			click.set_current_time(curtime)
			if click.has_faded():
				self._clicks.remove(click)
				continue

			yield click

	@property
	def cursors(self):
		return iter(self._cursors.values())

	@property
	def last_message_type(self):
		return self._lastmsg

	def process_message(self, data):
		""" Process a given frame. """

		_int = lambda x: int.from_bytes(x, 'little')
		_col = lambda x: ((x >> 16) & 255, (x >> 8) & 255, x & 255)

		curtime = _monotonic()
		packet_type = int(data[0])

		self._lastmsg = ReceivedMessageType.UNKNOWN

		o = 1

		def _updateobjects():
			""" Internal function to define objects states, either for
				existing ones or for non-existing ones (creations). """

			nonlocal o, data

			nobjects = _int(data[o:o+2])
			o += 2

			for i in range(nobjects):
				object_id = _int(data[o:o+4])
				object_type = _int(data[o+4:o+5])
				o += 5

				previous = self._objects.get(object_id, None)

				if object_type == 255:
					# This object is ignored in the original script.

					if object_id in self._objects:
						del self._objects[object_id]
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

					self._objects[object_id] = Text(x, y, size,
						centered, text_content)
				elif object_type == 1:
					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					w = _int(data[o+4:o+6]) * 2
					h = _int(data[o+6:o+8]) * 2
					col = _int(data[o+8:o+12])
					o += 12

					self._objects[object_id] = Wall(x, y, w, h,
						_col(col))
				elif object_type == 2:
					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					w = _int(data[o+4:o+6]) * 2
					h = _int(data[o+6:o+8]) * 2
					bad = bool(_int(data[o+8:o+9]) != 0)
					o += 9

					self._objects[object_id] = Warp(x, y, w, h, bad)
				elif object_type == 3:
					# unknown object (probably activator while standing?)

					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					w = _int(data[o+4:o+6]) * 2
					h = _int(data[o+6:o+8]) * 2
					count = _int(data[o+8:o+10])
					color = _int(data[o+10:o+14])
					o += 14

					self._objects[object_id] = Detector(x, y, w, h,
						count, _col(color))
				elif object_type == 4:
					# unknown object (probably button on which to click on?)

					x = _int(data[o:o+2]) * 2
					y = _int(data[o+2:o+4]) * 2
					w = _int(data[o+4:o+6]) * 2
					h = _int(data[o+6:o+8]) * 2
					count = _int(data[o+8:o+10])
					col = _int(data[o+10:o+14])
					o += 14

					last_click = None
					if previous is not None:
						last_click = previous.last_click
						if previous.count > count:
							last_click = _monotonic()

					self._objects[object_id] = Button(x, y, w, h,
						count, _col(col), last_click)
				else:
					return False

			return True

		if packet_type == 0:
			# Only contains four bytes.
			# Potentially client id?

			self._playerid = _int(data[o:o+4])
		elif packet_type == 1:
			# get game status?
			# [nbr, {i_32, i_16, i_16}, nbr_16, {i_32}, nbr_16, {i_32}[, opt_32]]

			nbr_cursors = _int(data[o:o+2])
			o += 2

			self._cursors = {}
			for i in range(nbr_cursors):
				id = _int(data[o:o+4])
				x = _int(data[o+4:o+6]) * 2
				y = _int(data[o+6:o+8]) * 2
				o += 8

				if id != self._playerid:
					self._cursors[id] = Cursor(x, y)

			nbr_clicks = _int(data[o:o+2])
			o += 2

			for i in range(nbr_clicks):
				x = _int(data[o:o+2]) * 2
				y = _int(data[o+2:o+4]) * 2
				o += 4

				self._clicks.append(Click(curtime, x, y))

			nbr_dlt = _int(data[o:o+2])
			o += 2

			for i in range(nbr_dlt):
				object_id = _int(data[o:o+4])
				o += 4

				if object_id in self._objects:
					del self._objects[object_id]

			_updateobjects()

			nbr_lines = _int(data[o:o+2])
			o += 2

			for i in range(nbr_lines):
				sx = _int(data[o:o+2]) * 2
				sy = _int(data[o+2:o+4]) * 2
				ex = _int(data[o+4:o+6]) * 2
				ey = _int(data[o+6:o+8]) * 2
				o += 8

				self._lines.append(DrawnLine(curtime, sx, sy, ex, ey))

			# Possiblement après, le nombre de joueurs connectés.
			self._playercount = 0
			if len(data) >= o + 4:
				self._playercount = _int(data[o:o+4])
		elif packet_type == 4:
			# load the level!
			# [nbr, i_16, i_16, nbr_16, {variable}[, opt_16_32]]

			self._lastmsg = ReceivedMessageType.LEVEL
			self._position = (_int(data[o:o+2]) * 2, _int(data[o+2:o+4]) * 2)
			self._cursors = {}
			self._objects = {}
			self._lines = []
			self._clicks = []

			o += 4

			_updateobjects()
		elif packet_type == 5:
			# [i_16, i_16, i_16_or_32]

			self._lastmsg = ReceivedMessageType.POSITION

			x = _int(data[o:o+2]) * 2
			y = _int(data[o+2:o+4]) * 2
			o += 4

			death_count = 0
			if len(data) >= 9:
				death_count = _int(data[o:o+4])
			elif len(data) >= 7:
				death_count = _int(data[o:o+2])

			self._position = (x, y)

	def set_position(self, x, y):
		""" Set the position. This function returns the updated
			position that have been calculated locally using collisions. """

		def dst(ax, ay, bx, by):
			return _math.sqrt(abs(ax - bx) ** 2 + abs(ay - by) ** 2)

		ox, oy = self._position
		px, py = x, y

		# Initialize the final position and calculate the initial
		# distance of the path to the current final position.

		fx, fy = x, y
		fdst = dst(ox, oy, fx, fy)

		# Check with all of the walls.

		sw, sh = self.width, self.height
		walls = [Wall(-1, 0, 1, sh), Wall(0, -1, sw, 1),
			Wall(sw, 0, 1, sh), Wall(0, sh, sw, 1)]
		walls.extend(filter(lambda x: isinstance(x, Wall), self.objects))

		for wall in walls:
			# First, let's check horizontally.

			new_x = None
			if ox < px and ox < wall.x:
				new_x = wall.x - 1
			elif ox > px and ox > wall.x + wall.w - 1:
				new_x = wall.x + wall.w

			if new_x is not None:
				# Calculate the projected y coordinates using Thales' theorem,
				# and check if it's within the shape.

				new_y = int(oy + (oy - py) * (new_x - ox) / (px - ox))
				if new_y in range(wall.y, wall.y + wall.h):
					new_dst = dst(ox, oy, new_x, new_y)
					if new_dst < fdst:
						fx, fy, fdst = new_x, new_y, new_dst

			# Then, even if the horizontal checks did pass, let's
			# check vertically.

			new_y = None
			if oy < py and oy < wall.y:
				new_y = wall.y - 1
			elif oy > py and oy > wall.y + wall.h - 1:
				new_y = wall.y + wall.h

			if new_y is not None:
				# Calculate the projected x coordinate using Thales' theorem,
				# the same way we have done it with x.

				new_x = int(ox + (ox - px) * (new_y - oy) / (py - oy))
				if new_x in range(wall.x, wall.x + wall.w):
					new_dst = dst(ox, oy, new_x, new_y)
					if new_dst < fdst:
						fx, fy, fdst = new_x, new_y, new_dst

		# This shouldn't happen, but let's restrict our values within the
		# game limits.

		if fx < 0: fx = 0
		elif fx >= self.width: fx = self.width - 1
		if fy < 0: fy = 0
		elif fy >= self.height: fy = self.height - 1

		# Okay, set the new position.

		self._position = (fx, fy)
		return (fx, fy)

# ---
# Main game function.
# ---

async def amain():
	_pygame.display.init()
	_pygame.font.init()

	assets = Assets()
	state = GameState()

	async with _websockets.connect("ws://128.199.12.58:2828") as ws:
		screen_w, screen_h = state.width, state.height

		window = _pygame.display.set_mode((screen_w + 20, screen_h + 20))
		window.fill((0, 0, 0))
		screen = window.subsurface((10, 10, screen_w, screen_h))

		screen_x, screen_y = screen.get_offset()
		_should_grab = False # TODO: True

		_pygame.display.set_caption("cursors.io python client")
		_pygame.display.set_icon(assets.icon)
		_pygame.mouse.set_visible(False)
		_pygame.event.set_grab(_should_grab)

		def set_cursor_pos(x, y):
			off_x, off_y = screen_x, screen_y
			_pygame.mouse.set_pos((x + off_x, y + off_y))

		def infotext(text, xy):
			x, y = xy
			surface = assets.font(12).render(text, True, (0, 0, 0))
			screen.blit(surface, (x, y - surface.get_height()))
			del surface

		async def send_mouse_movement(x, y):
			msg = b'\1' + (x // 2).to_bytes(2, 'little')
			msg += (y // 2).to_bytes(2, 'little')
			msg += (1).to_bytes(2, 'little')
			msg += (1).to_bytes(2, 'little')
			await ws.send(msg)

		async def send_mouse_click(x, y):
			msg = b'\2' + (x // 2).to_bytes(2, 'little')
			msg += (y // 2).to_bytes(2, 'little')
			msg += (1).to_bytes(2, 'little')
			msg += (1).to_bytes(2, 'little')
			await ws.send(msg)

		async def pygame_events():
			""" async generator for pygame events. """

			while True:
				event = _pygame.event.poll()
				if event.type == NOEVENT:
					await _asyncio.sleep(0.005)
					continue

				yield event

		async def websocket_events():
			""" async generator for websocket events. """

			while True:
				message = await ws.recv()
				yield _pygame.event.Event(USEREVENT, message = message)

		async def regular_events():
			""" async generator for regular events. """

			tm = 1.0 / 30 # number of fps

			while True:
				yield _pygame.event.Event(NOEVENT)
				await _asyncio.sleep(tm)

		# Main event loop.

		event_streams = (regular_events(),
			websocket_events(), pygame_events())
		async with _aiostream.merge(*event_streams).stream() as streamer:
			blocked_x, blocked_y = None, None
			paused = False

			async for event in streamer:
				if event.type == QUIT:
					break
				elif event.type == NOEVENT:
					# is a display event, so let's show'em what we do best!
					pass
				elif event.type == USEREVENT:
					state.process_message(event.message)
					if state.last_message_type in (ReceivedMessageType.LEVEL,
						ReceivedMessageType.POSITION):
						if not paused:
							set_cursor_pos(*state.position)

					continue
				elif paused:
					if event.type == MOUSEBUTTONDOWN:
						paused = False
						_pygame.event.set_grab(_should_grab)
						_pygame.mouse.set_visible(False)
						set_cursor_pos(*state.position)

					continue
				else:
					if event.type == MOUSEMOTION:
						x, y = event.pos
						x, y = x - screen_x, y - screen_y

						ox, oy = x, y

						if blocked_x is not None:
							x = blocked_x
						if blocked_y is not None:
							y = blocked_y

						x, y = state.set_position(x, y)
						if (x, y) != (ox, oy):
							set_cursor_pos(x, y)

						await send_mouse_movement(x, y)
					elif event.type == MOUSEBUTTONDOWN:
						if event.button == 1:
							await send_mouse_click(*state.position)
					elif event.type == KEYDOWN:
						if event.key == K_LCTRL:
							blocked_x = state.position[0]
						elif event.key == K_LALT:
							blocked_y = state.position[1]
						elif event.key == K_ESCAPE:
							paused = True
							_pygame.event.set_grab(False)
							_pygame.mouse.set_visible(True)
					elif event.type == KEYUP:
						if event.key == K_LCTRL:
							blocked_x = None
						elif event.key == K_LALT:
							blocked_y = None
					elif event.type == ACTIVEEVENT:
						if event.state == 1 and not event.gain:
							# Window has been unfocused.
							paused = True
							_pygame.event.set_grab(False)
							_pygame.mouse.set_visible(True)
						elif event.state == 1 and event.gain:
							# Window has been focused.
							# Let's redraw.

							pass

					continue

				# Display code.

				window.fill((0, 0, 0))
				screen.fill((255, 255, 255))

				for object in state.objects:
					if isinstance(object, Text):
						font = assets.font(object.size)
						rndr = font.render(object.text, True, (0, 0, 0))
						x, y = object.x, object.y
						if object.centered:
							x -= rndr.get_width() // 2
						y -= rndr.get_height()
						screen.blit(rndr, (x, y))
					elif isinstance(object, Wall):
						x, y = object.x, object.y
						w, h = object.width, object.height
						color = object.color
						_pygame.draw.rect(screen, color, (x, y, w, h))
					elif isinstance(object, Warp):
						rect = _pygame.Surface((object.width, object.height))
						rect.fill((255, 0, 0) if object.bad else (0, 255, 0))
						rect.set_alpha(int(.2 * 255))
						screen.blit(rect, (object.x, object.y))
					elif isinstance(object, Detector):
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
					elif isinstance(object, Button):
						x, y = object.x, object.y
						w, h = object.width, object.height
						pressed = object.pressed
						b = 8 if pressed else 12

						# We draw the button's base.

						button = _pygame.Surface((w, h))
						button.fill(object.color)

						work = _pygame.Surface((w, h), _pygame.SRCALPHA)
						work.fill((0, 0, 0))
						work.set_alpha(int(.2 * 255))
						button.blit(work, (0, 0))
						del work

						# We draw the button's top.

						work = _pygame.Surface((w - 2 * b, h - 2 * b))
						work.fill(object.color)
						button.blit(work, (b, b))
						del work

						# We draw the grid.

						work = _pygame.Surface((w, h), _pygame.SRCALPHA)
						_pygame.draw.line(work, (0, 0, 0),
							(0, 0), (b, b), width = 2)
						_pygame.draw.line(work, (0, 0, 0),
							(w - 1, 0), (w - b - 1, b), width = 2)
						_pygame.draw.line(work, (0, 0, 0),
							(0, h - 1), (b, h - b - 1), width = 2)
						_pygame.draw.line(work, (0, 0, 0),
							(w - 1, h - 1), (w - b - 1, h - b - 1),
							width = 2)
						_pygame.draw.polygon(work, (0, 0, 0),
							((0, 0), (w - 1, 0), (w - 1, h - 1), (0, h - 1)),
							width = 2)
						_pygame.draw.polygon(work, (0, 0, 0),
							((b, b), (w - b - 1, b), (w - b - 1, h - b - 1),
							(b, h - b - 1)), width = 2)
						work.set_alpha(int(.1 * 255))
						button.blit(work, (0, 0))
						del work

						# We write the text.

						if w <= 100 or h <= 100:
							font = assets.font(35)
							fontpad = 13
						else:
							font = assets.font(45)
							fontpad = 16

						rndr = font.render(f"{object.count}", True,
							(0, 0, 0))
						rndr.set_alpha(int(.5 * 255))

						button.blit(rndr, (w // 2 - rndr.get_width() // 2,
							h // 2 - fontpad))
						del rndr

						# Let us make it darker if the button is pressed.

						if pressed:
							work = _pygame.Surface((w - 2 * b, h - 2 * b),
								_pygame.SRCALPHA)
							work.fill((0, 0, 0))
							work.set_alpha(int(.15 * 255))
							button.blit(work, (b, b))
							del work

						# Let's blit the final button to the screen!

						screen.blit(button, (x, y))

				infotext(f"{state.player_count} "
					"players online", (10, 590))

				for line in state.drawn_lines:
					w = abs(line.start_x - line.end_x + 1)
					h = abs(line.start_y - line.end_y + 1)
					x = min(line.start_x, line.end_x)
					y = min(line.start_y, line.end_y)

					rect = _pygame.Surface((w, h), _pygame.SRCALPHA)
					_pygame.draw.line(rect, (121, 121, 121),
					   (line.start_x - x, line.start_y - y),
					   (line.end_x - x, line.end_y - y))
					rect.set_alpha(int(line.alpha * 255))
					screen.blit(rect, (x, y))

				for click in state.clicks:
					x, y = click.x, click.y
					radius = click.radius
					alpha = click.alpha

					rect = _pygame.Surface((radius * 2, radius * 2),
						_pygame.SRCALPHA)
					_pygame.draw.circle(rect, (0, 0, 0),
						(radius, radius), radius, width = 3)
					rect.set_alpha(int(.3 * alpha * 255))
					screen.blit(rect, ((x - rect.get_width() // 2,
						y - rect.get_height() // 2)))
					del rect

				for cursor in state.cursors:
					window.blit(assets.cursor, (10 + cursor.x - 5,
						10 + cursor.y - 5))

				x, y = state.position
				# Approximations due to:
				# - the size of the window border (10px).
				# - the number of transparent pixels on top left of the
				#   cursor image (5px hor. and ver.).
				x, y = 10 + x - 5, 10 + y - 5

				rect = _pygame.Surface((40, 40), _pygame.SRCALPHA)
				_pygame.draw.circle(rect, (255, 255, 0),
					(20, 20), 20)
				rect.set_alpha(int(.2 * 255))

				cx = x + assets.cursor.get_width() // 2 - 23
				cy = y + assets.cursor.get_height() // 2 - 23

				window.blit(rect, (cx, cy))
				window.blit(assets.cursor, (x, y))

				if paused:
					grey = _pygame.Surface((window.get_width(),
						window.get_height()), _pygame.SRCALPHA)
					grey.fill((128, 128, 128))
					grey.set_alpha(int(.5 * 255))
					window.blit(grey, (0, 0))
					del grey

				_pygame.display.flip()

	_pygame.quit()

def main():
	_asyncio.run(amain())

# Run the program.

main()

# End of file.
