import os
from future.utils import iteritems
import readline

def main():
	while True:
		print("What do you need?")
		print("1 - Get Hashes from NTDS Dump")
		print("2 - Recombine Cracked Hashes with Usernames")
		print("3 - Quit")

		mainChoice = int(input("Please make a choice: "))

		if mainChoice == 3:
			print("Byee!")
			quit()
		elif mainChoice == 2:
			recombinator()
		elif mainChoice == 1:
			secretsDumpMenu()
		else:
			print("Inconceivable!")
			main()

def recombinator():
    # Thank you to ShawnDEvans for hashmash, which is the basis for this portion of the script.
    readline.get_completer()
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims('\t\n=\\')
    print('$ python %s <Hash File> <OCL Hashcat Decrypted File>')
    print('\n')
    print('User Hash File format is username:hash (or JTR NTLM)')
    print('OCL Decrypted Pasword File format is, hash:password')
    print('\n')
    try:
        hash_file = raw_input("user:hash file? ")
        pass_file = raw_input("hash:pass file? ")
	combOutFile = raw_input("Name of Output File? ")
    except IOError:
        print('[ERROR]\tInvalid input files, please review..')
        recombinator()

    passDict = dict(line.split(':') for line in open(pass_file))
    hashes = open(hash_file, 'r')
    f = hashes.readlines()

    for cracked_hash, passwd in iteritems(passDict):
        for hashItem in f:
            if len(hashItem) > 0:
                hashList = hashItem.split(':')
                if len(hashList) == 7 or len(hashList) == 4:
                    user_name, user_hash = (hashList[0], hashList[3])
                else:
                    user_name, user_hash = (hashList[0], hashList[1])
                    if cracked_hash.upper().strip() == user_hash.upper().strip():
			out = open(combOutFile, 'a')
    	                out.write('%s:%s\n' % (user_name.strip(), passwd.strip()))
    print("\n")
    print("Done!")
    quit()

def secretsDumpMenu():
    readline.get_completer()
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims('\t\n=\\')
    ntds = raw_input("Where is the NTDS.dit File? ")
    systemFile = raw_input("Where is the SYSTEM File? ")
    outFile = raw_input("Output File Name (name only, no extension)? ")
    while True:
        history = raw_input("Do you want historical passwords? (Y/N): ")
        F1 = history[0].lower()
        if history == '' or not F1 in ['y','n']:
            print("Invalid Choice! Please answer Y or N.")
        else:
            break
    if F1 == "n":
        sedHashesOnly = "sed -e '/des-cbc/d' -e '/aes256/d' -e '/aes128/d' -e '/rc4_hmac/d' -e '/$:/d' -e '/$_/d' -e '/\\\/!d' " + str(outFile) + ".raw | cut -d'\\' -f2 | cut -d':' -f4 > " + str(outFile) + ".hash"
        noHist = "impacket-secretsdump -ntds " + str(ntds) + " -system " + str(systemFile) + " LOCAL > " + str(outFile) + ".raw"
        print("Running Secretsdump....")
        os.system(noHist)
        print("Done!")

        print("Preparing your file for Hashcat...")
        rawFile = str(outFile) + ".raw"
        open(rawFile)
        os.system(sedHashesOnly)
        print("Done!")

        print("Preparing the User:Hash file...")
        sedUserHashes = "sed -e '/des-cbc/d' -e '/aes256/d' -e '/aes128/d' -e '/rc4_hmac/d' -e '/$:/d' -e '/$_/d' -e '/\\\/!d' " + str(outFile) + ".raw | cut -d'\\' -f2 | cut -d':' -f1,4 > " + str(outFile) + ".userHash"
        os.system(sedUserHashes)
        print("Done!")
        print("Three files generated: " + str(outFile) + ".raw, " + str(outFile) + ".hash, and " + str(outFile) + ".userHash")
	quit()
    elif F1 =="y":
        sedHashesOnly = "sed -e '/des-cbc/d' -e '/aes256/d' -e '/aes128/d' -e '/rc4_hmac/d' -e '/$:/d' -e '/$_/d' -e '/\\\/!d' " + str(outFile) + ".raw | cut -d'\\' -f2 | cut -d':' -f4 > " + str(outFile) + ".hash"
        yesHist = "impacket-secretsdump -history -ntds " + str(ntds) + " -system " + str(systemFile) + " LOCAL > " + str(outFile) + ".raw"
        print("Running Secretsdump....")
        #print(yesHist)
        os.system(yesHist)
        print("Done!")

        print("Preparing your file for Hashcat...")
        rawFile = str(outFile) + ".raw"
        open(rawFile)
        os.system(sedHashesOnly)
        print("Done!")

	print("Preparing the User:Hash file...")
        sedUserHashes = "sed -e '/des-cbc/d' -e '/aes256/d' -e '/aes128/d' -e '/rc4_hmac/d' -e '/$:/d' -e '/$_/d' -e '/\\\/!d' " + str(outFile) + ".raw | cut -d'\\' -f2 | cut -d':' -f1,4 > " + str(outFile) + ".userHash"
        os.system(sedUserHashes)
	print("Done!")
        print("Three files generated: " + str(outFile) + ".raw, " + str(outFile) + ".hash, and " + str(outFile) + ".userHash")
        quit()
#    impacket-secretsdump -history -ntds -system


main()
