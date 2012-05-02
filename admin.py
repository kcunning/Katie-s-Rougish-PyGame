import sys
import os
import xml.etree.ElementTree as etree
from xml.dom.minidom import parseString

sys.path.append(os.path.join("roguey", "classes"))

from items import Treasure
from constants import *

def prettify(element):
	# Helper function to make XML look more prettier
    txt = etree.tostring(element)
    return parseString(txt).toprettyxml()

class Admin(object):
	def __init__(self):
		# Load the existing treasures
		f = open(
			os.path.join(
				"roguey",
				"resources",
				"items.xml",
				)
			)
		self.treasures = etree.fromstring(f.read())
		f.close()
		# trim the annoying whitespace...
		self.treasures.text = ""
		for element in self.treasures.iter():
			element.text = element.text.strip()
			element.tail = ""
		# Load the list of treasure type templates
		f = open(
			os.path.join(
				"roguey",
				"resources",
				"item_templates.xml",
				)
			)
		self.treasure_templates = etree.fromstring(f.read())
		f.close()
		# Enter main loop
		self.running = True
		self.main()		

	def new_treasure(self):
		item_attributes = {}  # This will hold optional stats only.

		template_options = [
			template.find("item_type").text for template in self.treasure_templates
		]

		# Gather the mandatory attributes
		selection = self.prompt_for_selection(
			prompt="Choose an item type",
			options=template_options
		)
		item_type = template_options[selection]
		template = self.treasure_templates[selection]

		title = raw_input("Give it a title: ")
		description = raw_input("Give it a description: ")

		# Check if this template requires any additional attributes
		for attr in template:
			if attr.tag == "item_type":
				continue
			prompt = attr.attrib["prompt"]
			value_type = attr.attrib.get("type", "string")  # type defaults to "string" if not specified
			item_attributes[attr.tag] = (raw_input("%s (%s): " % (prompt, value_type)), value_type)

		# finally we can add this new item to the list
		new_item = etree.SubElement(self.treasures, "item")
		etree.SubElement(new_item, "item_type").text = item_type
		etree.SubElement(new_item, "title").text = title
		etree.SubElement(new_item, "description").text = description
		for attrib, value in item_attributes.iteritems():
			optional_stat = etree.SubElement(new_item, attrib)
			optional_stat.text, optional_stat.attrib["type"] = value

	def list_treasures(self):
		for treasure in self.treasures:
			print treasure.find('title').text.strip()

	def save_and_quit(self):
		f = open("roguey/resources/items.xml", "w")
		f.write(prettify(self.treasures))
		f.close()
		self.running = False

	def quit_without_save(self):
		is_sure_about_quitting = self.yes_no_prompt(
			"Are you super sure you want to quit without saving?"
		)
		if is_sure_about_quitting:
			self.running = False

	def delete_treasure(self):
		options = [element.find('title').text for element in self.treasures]
		prompt = "Select a treasure to delete: "
		selection = self.prompt_for_selection(prompt, options)
		confirmation_prompt = (
			'Do you really want to delete "%s"?'
			% options[selection]
			)
		sure_about_deleting = self.yes_no_prompt(confirmation_prompt)
		if sure_about_deleting:
			self.treasures.remove(self.treasures[selection])

	def main(self):
		menu_options_with_actions = [
			("Make a new treasure", self.new_treasure),
			("List current treasures", self.list_treasures),
			("Delete a treasure", self.delete_treasure),
			("Save and quit", self.save_and_quit),
			("Quit without saving", self.quit_without_save)
		]
		menu_options = [x[0] for x in menu_options_with_actions]
		menu_prompt = "Make a choice"

		while self.running:
			selection = self.prompt_for_selection(menu_prompt, menu_options)
			# Call the appropriate action based on the user selection
			menu_options_with_actions[selection][1]()

	def prompt_for_selection(self, prompt, options):
		"""Given a list of options and a prompt,
		get the users selection and return the index of the selected option
		"""
		retval = None
		# Print out the numbered options
		for i, option in enumerate(options):
			print "%3s. %s" % (i+1, option)
		# Continue to prompt user until valid input is recieved.
		while retval == None:
			# Get the users selection
			selection = raw_input("%s: " % prompt)
			# Check that the input is valid integer
			try:
				retval = int(selection) - 1
			except ValueError:
				print "Invalid input. Please enter a number."
				continue
			# Ensure input is within the valid range
			if retval < 0 or retval >= len(options):
				print ("Please enter a number between 1 and %d inclusive." 
					% len(options))
				retval = None  # reset the illegal value
				continue
		return retval

	def yes_no_prompt(self, prompt):
		'''Prompt for a yes/no answer. 
		Will accept any response beginning with Y, N, y or n.
		Returns a bool.'''
		retval = None
		selection = raw_input("%s (Y/N): " % prompt)
		# Continue to prompt user until valid input starts with "Y" or "N".
		while retval == None:
			first_letter = selection.strip()[0].upper()
			try:
				retval = {
					"Y": True,
					"N": False
				}[first_letter]
			except KeyError:
				pass
		return retval


if __name__ == "__main__":
	a = Admin()
