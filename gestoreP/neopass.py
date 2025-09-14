try:
	import cry
except ModuleNotFoundError:
	from gestoreP import cry
import os
from load_dotenv import load_dotenv

load_dotenv()
PATH = os.getenv("PASS_PATH")

MANUAL = """\n======\nMANUAL\n======\n
>>>> lookup <website_name>: search for a password for this website
>>>> set <password> <website_name>: set a password for this website
>>>> remove <website_name>: removes the password for this website\n"""

def do(func, website_name: str, password: str = None):
	thisfile = f"{PATH}/{format(website_name)}.txt"
	try:
		cry.decryptfile(thisfile)
	except:
		pass

	f = func(website_name, password)

	if os.path.exists(thisfile):
		cry.encryptfile(thisfile)

	return f

def format(website_name: str):
	return website_name.replace("/", "").replace("?", "").replace(":", "")

def unformat(website_name: str):
	return website_name.replace(".txt", "")

def set_password(website_name: str, password: str):
	thisfile = f"{PATH}/{format(website_name)}.txt"
	if os.path.exists(thisfile):
		with open(thisfile, "r") as f:
			oldpass = f.read()
		with open(thisfile, "w") as f:
			f.write(password)
			print(f"Password {oldpass} replaced with {password}")
	else:
		with open(thisfile, "a") as f:
			f.write(password)
			print(f"Password set to {password}")

def remove_password(website_name: str, password: str = None):
	thisfile = f"{PATH}/{format(website_name)}.txt"
	if os.path.exists(thisfile):
		os.remove(thisfile)
		print(f"Password for {website_name} removed")
	else:
		print(f"Password for {website_name} was not set")

def read(website_name: str, password: str = None):
	with open(f"{PATH}/{website_name}.txt", "r") as f:
		return f"{unformat(website_name)} --> {f.read()}"

def lookup(website_name: str, password: str = None):
	results = []
	for file in os.listdir(PATH):
		if file.startswith(format(website_name)):
			results.append(do(read, file.replace(".txt", "")))
	return results

def main():
	print("==============\nType q to quit; man to read the manual\n==============")
	running = True
	while running:
		action = input()
		args = action.split(" ")
		match args[0].lower():
			case "q":
				print("Quitting program...")
				running = False
			case "lookup":
				result = lookup(" ".join(args[1:]))
				print(f"{len(result)} result{('s' if len(result) != 1 else '')}:")
				print("\n".join(sorted(result)))
			case "set":
				do(set_password, " ".join(args[2:]), args[1])
			case "remove":
				do(remove_password, " ".join(args[1:]))
			case "man":
				print(MANUAL)
			case _:
				print("Command not found. Use 'man' to read the manual")

def migrate(l: list):
	count = 0
	for i in l:
		i = i.split(" --> ")
		do(set_password, i[0], i[1])
		count += 1
	print(f"{count} passwords imported")

if __name__ == "__main__":
	main()
