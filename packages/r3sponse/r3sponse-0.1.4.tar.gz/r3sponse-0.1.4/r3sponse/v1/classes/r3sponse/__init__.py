#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3sponse.v1.classes.config import *
from django.http import JsonResponse

# the manager class.
class R3sponse(object):
	def __init__(self):	
		self.log_file = None
		#
	def default_response(self):
		return {
			"success":False,
			"error":None,
			"message":None,
		}
	def success_response(self,
		# the message (must be param #1).
		message, 
		# additional returnable functions (must be param #2).
		variables={}, 
		# log the message to the console.
		log=False, 
		# save the error to the logs file.
		save=False,
		# return as a django JsonResponse.
		django=False,
	):
		response = self.default_response()
		response["success"] = True
		response["message"] = message
		for key, value in variables.items():
			response[key] = value
		if log: print(response["message"])
		if save: self.__log_to_file__(response["message"])
		if django: response = JsonResponse(response)
		return response
	def error_response(self,
		# the error message.
		error, 
		# log the error to the console.
		log=False, 
		# save the error to the erros file.
		save=False,
		# return as a django JsonResponse.
		django=False,
	):
		response = self.default_response()
		response["error"] = error
		if log: print(response["error"])
		if save: self.__log_to_file__(response["error"])
		if django: response = JsonResponse(response)
		return response
		#
	def load_logs(self, format="webserver", options=["webserver", "cli", "array", "string"]):
		try:
			logs = Formats.File(self.log_file, load=True, blank="").data
		except:
			return self.error_response("Failed to load the logs.")
		if format == "webserver":
			logs = logs.replace("\n", "<br>")
		elif format == "cli":
			a=1
		elif format == "array" or format == list:
			logs = logs.split("\n")
		elif format == "string" or format == str:
			logs = str(logs)
		else: 
			return self.error_response(f"Invalid format parameter [{format}], valid options: {options}.")

		return self.success_response("Succesfully loaded the logs.", {"logs":logs})
	def reset_logs(self):
		Formats.File(self.log_file).save(f"Resetted log file.\n")
		#
	# system functions.
	def __log_to_file__(self, message):

		# init.
		response = self.default_response()
		try:
			with open(self.log_file, "a") as file:
				file.write(f'{Formats.Date().seconds_timestamp} - {message}\n')
			response["success"] = True
			response["message"] = "Succesfully logged the message."
		except:
			response["error"] = "Failed to log the message."
			return response
		
		# check file size.
		size = Formats.FilePath(self.log_file).size(mode="mb", type="integer")
		if size >= 100: self.reset_logs()

		# return response.
		return response

		#

# initialized objects.
r3sponse = R3sponse()

