with open("./readme.md", 'a') as f:
    for chapter in range(0, 10):
        print("0{}------>{}".format(chapter, chapter+20), file=f)
