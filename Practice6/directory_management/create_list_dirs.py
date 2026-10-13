import os

folder_name = "my_folder"

"""#create a directory
os.makedirs(folder_name, exist_ok = True)
print(f"Directory '{folder_name}' was created.")

#create a sample file inside it
file_path = os.path.join(folder_name, "sample.txt")

with open(file_path, "w") as f:
    f.write("This is a sample file. ")"""

#list files and folders
print("\nContents of the current directory: ")

for item in os.listdir(): 
    print(item)

print(f"\nContents of '{folder_name}':")

for item in os.listdir(folder_name):
    print(item)