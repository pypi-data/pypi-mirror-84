import datetime
from os import listdir, mkdir
from os.path import isfile, join
import requests
import argparse


class NoteSaver():

	def save_note_local(self, title, description):
		try:
			mkdir("notes")
		except Exception as e:
			print(e)
			pass
		with open(f"notes/{title}", "w") as f:
			f.write(description)

	def save_note_online(self, title, description):
		r = requests.post("https://pastebin.com/api/api_post.php", data={
			"api_dev_key": "2b2a1470268e3045f87ee376ef7918f8",
			"api_option": "paste",
			"api_paste_code": description
		})
		return r.text

	def fetch_all_notes(self):
		try:
			onlyfiles = [f for f in listdir("notes") if isfile(join("notes", f))]
			return onlyfiles
		except:
			return []

	def open_note(self, title):
		with open(f"notes/{title}") as f:
			return f.read()

	def get_multiline_input(self):
		lines = []
		while True:
			line = input()
			if line:
				lines.append(line)
			else:
				break
		text = '\n'.join(lines)
		return text

	def current_date(self):
		now = datetime.datetime.now()
		return now.strftime("%Y-%m-%d-%H:%M:%S")


	def gen_id_notes(self, notes):
		self.ns = {}
		count = 1
		for i in notes:
			self.ns[count] = i
			count+=1


	def cli(self):
		parser = argparse.ArgumentParser(description='A Note Saver')
		parser.add_argument('command', help='View all the notes')

		args = parser.parse_args()

		if args.command == "l":
			notes = self.fetch_all_notes()
			if len(notes) == 0:
				print("No note available, why don't create one?")
			else:
				print("Here's all of your notes:")
				self.gen_id_notes(notes)

		elif args.command == "r":
			self.gen_id_notes(self.fetch_all_notes())
			id = input("Type ID of the notes. If you don't know, in command, type l")

			try:
				print("\nContent:\n")
				print(self.open_note(self.ns[int(id)]))
			except:
				print("Notes unavailable")


		elif args.command == "c":
			title = input("Please go ahead and type a title for your note: ")
			print("Type your contents of your note: ")
			note = self.get_multiline_input()
			self.save_note_local(f"{self.current_date()}--{title}", note)
			link = self.save_note_online(f"{self.current_date()}--{title}", note)
			print(f"Done! You can also access your note online at {link}")


if __name__ == "__main__":
    n = NoteSaver()
    n.cli()