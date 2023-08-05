from typing import List as _List, Callable as _Callable, Tuple as _Tuple, Union as _Union
from threading import Lock as _Lock
from datetime import datetime as _datetime
from time import time as _now
import sys as _sys
import traceback as _traceback


def int_2_bool_list(integer, bit_count) -> _List[bool]:
	result = [False] * bit_count
	for i in range(bit_count):
		if (integer & (1 << i)) != 0:
			result[i] = True
	return result


def bool_list_2_int(bools: _List[bool]) -> int:
	result = 0
	for b, idx in enumerate(bools):
		if b:
			result |= (1 << idx)

	return result


class Callback:
	def __init__(self):
		self._callback_list = list()
		self._callback_list_guard = _Lock()

	def subscribe(self, callback: _Callable):
		with self._callback_list_guard:
			if callback not in self._callback_list:
				self._callback_list.append(callback)

	def unsubscribe(self, callback: _Callable):
		with self._callback_list_guard:
			if callback in self._callback_list:
				self._callback_list.remove(callback)

	def unsubscribe_all(self):
		with self._callback_list_guard:
			self._callback_list.clear()

	def __call__(self, *args, **kwargs):
		with self._callback_list_guard:
			for callback in self._callback_list:
				callback(*args, **kwargs)


def timestamp(stamp: float = None) -> str:
	if stamp is None:
		stamp = _now()
	dt = _datetime.fromtimestamp(stamp)
	return dt.isoformat(' ')[:19]


def timestamp_as_filename(stamp: float = None, sep: str = '-') -> str:
	return timestamp(stamp).replace(':', sep)


def format_exception(skip_level: int = 0):
	exc_type, exc_value, exc_tb = _sys.exc_info()
	for i in range(skip_level):
		if exc_tb.tb_next is not None:
			exc_tb = exc_tb.tb_next

	return _traceback.format_exception(exc_type, exc_value, exc_tb)


def print_exception(skip_level: int = 0):
	lines = format_exception(skip_level)
	print(''.join(lines), end='')


class StrState:
	__states__: _Tuple[str] = ()

	@classmethod
	def all(cls) -> _Tuple[str]:
		return tuple(cls.__states__)

	def __init__(self, value: _Union[str]):
		if isinstance(value, str):
			assert value in self.__states__
			self.__value = value
		else:
			assert isinstance(value, StrState)
			self.__value = value.__value

	def set(self, value: _Union[str]):
		if isinstance(value, str):
			assert value in self.__states__
			self.__value = value
		else:
			assert isinstance(value, StrState)
			self.__value = value.__value

	def __contains__(self, item):
		if isinstance(item, str):
			return item in self.__states__
		else:
			assert isinstance(item, StrState)
			return item.__value in self.__states__

	def __str__(self):
		return self.__value

	def __eq__(self, other):
		if isinstance(other, str):
			assert other in self.__states__
			return self.__value == other
		assert isinstance(other, StrState)
		return self.__value == other.__value

	def __int__(self):
		return self.__states__.index(self.__value)

	def __lt__(self, other):
		if isinstance(other, StrState):
			return int(self) < int(other)
		else:
			assert isinstance(other, str)
			return int(self) < self.__states__.index(other)
