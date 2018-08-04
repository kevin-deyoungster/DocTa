import os
import sys
import string


def createDir(seed_chain):
    path = "/".join(seed_chain)
    if not os.path.exists(path):
        print(f"Creating Node: {path}")
        os.makedirs(path)
    else:
        print(f"Node Already Exists: {path}")


def getTabLevel(line):
    return line.count("\t")


# Obtained from http://www.andrew-seaford.co.uk/generate-safe-filenames-using-python/
def makeSafeFilename(inputFilename):
    try:
        safechars = string.ascii_letters + string.digits + " -_."
        return "".join(filter(lambda c: c in safechars, inputFilename))
    except:
        print(f"Could not create safefilename for {inputFilename}")


def updateSeedChain(node, tabDifference, seed_chain):
    if tabDifference == 0:
        # On the Same Level, replace last node with current node
        seed_chain[len(seed_chain) - 1] = node
    elif tabDifference == 1:
        # On higher level, Current node is a subfolder, add to chain
        seed_chain.append(node)
    elif tabDifference < 0:
        # On lower level, current node is a parent folder, remove aahn till proper level and replace
        for i in range(abs(tabDifference)):
            seed_chain.pop()
        seed_chain[len(seed_chain) - 1] = node
    else:
        print(f"Integrity of Seed has been compromised at {node}")
        return False
    return True

# Create a folder tree


def germinate(seed, seed_chain):
    prevTabLevel = None
    for i in range(len(seed)):
        node = seed[i]
        currTabLevel = getTabLevel(node)
        if i == 0:
            folderToCreate = makeSafeFilename(node).strip()
            seed_chain.append(folderToCreate)
            # print(f"Main Dir: {folderToCreate}")
            createDir(seed_chain)
        else:
            folderToCreate = makeSafeFilename(node).strip()
            tabDiff = currTabLevel - prevTabLevel
            updated = updateSeedChain(folderToCreate, tabDiff, seed_chain)
            if updated:
                createDir(seed_chain)

        prevTabLevel = currTabLevel


def main():
    # Germinate all seed files in current directory
    seed_files = [
        f for f in os.listdir('.')
        if os.path.isfile(f) and os.path.splitext(f)[1] == ".seed"
    ]
    for seed_file in seed_files:
        seed = open(seed_file, encoding='utf-8-sig').readlines()
        seed_chain = []
        germinate(seed, seed_chain)


main()
