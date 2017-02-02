#Get die roll from user
usr_in = str (raw_input  ("Enter a die roll (ex: d20adv+2d4-1): "))

#Format die roll. Put a delimiting space between every die or bonus and separate into a list.
usr_in = usr_in.replace ("+"," +")
usr_in = usr_in.replace ("-"," -")
usr_in = "+" + usr_in
usr_in = usr_in.replace ("+d","+1d")
usr_in = usr_in.replace ("-d","-1d")
usr_in = usr_in.split (" ")

#Look through list of dice and bonuses to remove all bonuses and total them.
bonus = 0
n = 0
for i in usr_in:
    if not "d" in i:
        if i[0] == "+":
            bonus += int (i[1:])
            del (usr_in[n])
        else:
            bonus -= int (i[1:])
            del (usr_in[n])
    n += 1

#Now the list contains only dice. Create a formula for the roll; record a list of the dice to be used and their current values.
formula = "0" #starts formula at "0+x" instead of "+x" to give me one less case to care about
dice = [] #current value of each die
dieMax = [] #type of dice/max value of each die
iterations = 1 #number of iterations (used later)
n = 0 #number of dice to be rolled
for dieForm in usr_in:
	#if only one die of desired type (ex: d20), insert a 1 (ie: 1d20).
	if dieForm[1] == "d":
		dieForm = dieForm[0] + "1" + dieForm[1:]
	#split the die formula into the number of rolls (formSplit[0]) and max value of the die (formSplit[1])
	formSplit = dieForm.split("d")
	#iterate over each individual die
	for numOfRolls in range(0,int(formSplit[0])):
		#handles die formulas that have advantage
		if dieForm[-3:] == "adv":
			n += 1
			formula += str(dieForm[0]) + "max(dice[" + str(n-1) + "],dice[" + str(n) + "])"
			dieMax.append(int(formSplit[1][:-1]))
			dieMax.append(int(formSplit[1][:-1]))
			dice.append(1)
			dice.append(1)
			iterations = iterations * int(formSplit[1][:-1]) * int(formSplit[1][:-1])
		#handles die formulas that have disadvantage
		elif dieForm[-3:] == "dis":
			n += 1
			formula += str(dieForm[0]) + "min(dice[" + str(n-1) + "],dice[" + str(n) + "])"
			dieMax.append(int(formSplit[1]))
			dieMax.append(int(formSplit[1]))
			dice.append(1)
			dice.append(1)
			iterations = iterations * int(formSplit[1]) * int(formSplit[1])
		#handles die formulas that have neither advantage nor disadvantage
		else:
			formula += str(dieForm[0]) + "dice[" + str(n) + "]"
			dieMax.append(int(formSplit[1]))
			dice.append(1)
			iterations = iterations * int(formSplit[1])
		n += 1
#add bonus to formula
if bonus < 0:
	formula += str(bonus)
elif bonus > 0:
	formula += "+" + str(bonus)

#Evaluate formula for each possible combination of dice and record each answer.
dice.append(0) #Acts as a counter. When != 0, loop stops
dieMax.append(2) #Keeps dice and dieMax lists the same length. 2 is an arbitraty value that iteration will never reach.
answers = {}
avgSum = 0
while dice[-1] == 0:
	#Evaluate and record answer
	ans = eval(formula)
	avgSum += ans
	if ans in answers:
		answers[ans] += 1
	else:
		answers[ans] = 1
	#Increment dice
	dice[0] += 1
	for i in range(0,len(dice)):
		if dice[i] > dieMax[i]:
			dice[i] = 1
			dice[i+1] += 1

#Convert answers to percents; Divide the number of each answer in dictionary by the product of dieMax's elements (ignoring the last entry)
for i in answers:
	answers[i] = float(answers[i]) / iterations #"answers" dictionary is now the Probability Density Function (PDF)

#Convert answers dictionary into two lists. Nums contains all possible rolls and pdf is their corresponding values in the PDF
nums = answers.keys()
nums.sort()
pdf = []
for key in nums:
	pdf.append(answers[key])

#Calculate Cumulative Distribution Function (CDF)
cdf = []
runSum = 0
for i in range(0,len(nums)):
	runSum += pdf[i]
	cdf.append(round(runSum,4))

#Find average
avg = float(avgSum) / iterations

#Display results
print("\nAverage: " + str(avg) + "\n")
print("# \tPDF\t\tCDF\t\t1/CDF\n")
for i in range(0,len(nums)):
	line = str(nums[i]) + "\t" + str(round(pdf[i]*100,2)) + "%\t\t" + str(round(cdf[i]*100,4)) + "%\t\t" + str(100-round(cdf[i]*100,4)) + "%"
	print(line)
