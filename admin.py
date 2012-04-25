import sys
import xml.etree.ElementTree as etree
from xml.dom.minidom import parseString

sys.path.append("roguey/classes")

from items import Treasure
from constants import *

def prettify(element):
	# Helper function to make XML look more prettier
    txt = etree.tostring(element)
    return parseString(txt).toprettyxml()

class Admin(object):
	def __init__(self):
		# Load the existing treasures
		f = open("roguey/resources/items.xml")
		self.treasures = etree.fromstring(f.read())
		f.close()
		# Load the list of treasure type templates
		f = open("roguey/resources/item_templates.xml")
		self.treasure_templates = etree.fromstring(f.read())
		f.close()
		# Enter main loop
		self.running = True
		self.main()		

	def new_treasure(self):
		item_attributes = {}

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
			try:
				value_type = attr.attrib["type"]
				item_attributes[attr.tag] = raw_input("%s (%s): " % (prompt, value_type))
			except KeyError:
				item_attributes[attr.tag] = raw_input("%s: " % prompt)

		# finally we can add this new item to the list
		new_item = etree.SubElement(self.treasures, "item")
		etree.SubElement(new_item, "item_type").text = item_type
		etree.SubElement(new_item, "title").text = title
		etree.SubElement(new_item, "description").text = description
		for attrib, value in item_attributes.iteritems():
			etree.SubElement(new_item, attrib).text = value

	def list_treasures(self):
		for treasure in self.treasures:
			print treasure.find('title').text.strip()

	def save_and_quit(self):
		f = open("roguey/resources/items.xml", "w")
		f.write(prettify(self.treasures))
		f.close()
		self.running = False

	def delete_treasure(self):
		pass

	def main(self):
		menu_options_with_actions = [
			("Make a new treasure", self.new_treasure),
			("List current treasures", self.list_treasures),
			("Delete a treasure", self.delete_treasure),
			("Quit", self.save_and_quit),
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
		# Print out the numbered options
		for i, option in enumerate(options):
			print "%3s. %s" % (i+1, option)
		# Get the users selection
		selection = raw_input("%s: " % prompt)
		return int(selection)-1

if __name__ == "__main__":
	a = Admin()
