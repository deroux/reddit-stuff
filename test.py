i = 0
filename = "info_{i}.txt".format(i=i)
with open(filename, "w") as file:
    file.write("Test asdf title\n")
    file.write("Test asdf description")
