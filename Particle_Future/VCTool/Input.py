from time import sleep
from timeit import default_timer as timer

class Input:
    userInputSleep = None
    helpGlossary = ''
    file = ''
    writeList = []

    #Inputs
    totalYears = None
    netARR = None
    netBurn = None
    growthRate = None
    MRRperCustomer = None
    totalMRR = None
    upsellRevenue = None
    grossMargin = None
    numberofCustomersAcquired = None
    salesMarketingCosts = None
    churnContractionCosts = None


    def __init__(self, sleepTime, helpGlossary, file, writeList):
        self.userInputSleep = sleepTime
        self.helpGlossary = helpGlossary
        self.file = file
        self.writeList = writeList

    def addtowriteList(self, text):
        self.writeList.append(text + '\n')

    def write(self, text):
        print(text)
        self.addtowriteList(text)



    def writeLines(self):
        return self.writeList

    def promptUser(self):
        self.write(input(""))

    def introDirections(self):

        text = "Welcome to the StartUp Health Diagnostic Tool!"
        self.write(text)

        sleep(self.userInputSleep)

        text = "Press Enter to Continue"
        input(text)
        self.addtowriteList(text)

        text = "This tool's purpose is to help you gain a clearer view of your company and help improve your startup."
        self.write(text)

        self.promptUser()

        text = "It will do this by measuring your company's overall efficiency, sales efficiency, product retention, growth, and profitability."
        self.write(text)

        self.promptUser()

        text = "Based on these measurements, the tool will attempt to pinpoint why a metric may be underperforming and " \
               "further suggest some actions steps to improve your startup."
        self.write(text)

        self.promptUser()

        text = "All you have to do is put in some of your business accounts and the tool will do the rest!"
        self.write(text)

        self.promptUser()

        text = "Don't worry - this won't take long. You only need 11 numbers at hand."
        self.write(text)

        self.promptUser()

        text = "If you ever want to quit the program, just write and enter the word: 'quit'."
        self.write(text)

        self.promptUser()

        text =  "Lastly, an Input Help Guide is available for your reference. If you ever want to access this guide, enter the word 'help'."
        self.write(text)

        self.promptUser()
    def userInputandCheck(self, directions):
        done = False

        while True:
            try:
                userInput = input(directions)
                self.addtowriteList(directions+userInput)
                while userInput == 'help':
                    self.write(self.helpGlossary)
                    userInput = input(directions)
                    self.addtowriteList(directions + userInput)
                if userInput == 'quit':
                    quit()
                userInput = float(userInput)
            except ValueError:
                self.write("Please try again and enter a number")
            else:
                return float(userInput)

    def runUserInput(self):
        # basic info
            self.totalYears = self.userInputandCheck("\nTo begin, enter how many years your company has been in operation: ")

            # yearly info
            self.write("\nGreat! Now let's fill in some data from the last full 12 months")
            sleep(self.userInputSleep / 2)
            self.netARR = self.userInputandCheck("Enter your Net ARR from the last full 12 months: ")
            self.netBurn = self.userInputandCheck("Enter your Net Burn from the last full 12 months: ")

            # monthly info
            self.write(
                "\nGreat! Now let's fill in the bulk of the data. Please ensure these numbers are from the last full month.")
            sleep(self.userInputSleep)
            self.growthRate = self.userInputandCheck("Enter your MRR Growth Rate (%): ")
            self.MRRperCustomer = self.userInputandCheck("Enter your Average MRR per customer ($): ")
            self.totalMRR = self.userInputandCheck("Enter your total MRR at the start of the last month ($): ")
            self.upsellRevenue = self.userInputandCheck("Enter your revenue in expansions and upsells ($): ")
            self.grossMargin = self.userInputandCheck("Enter your Gross Margin (%): ")
            self.numberofCustomersAcquired = self.userInputandCheck(
                "Enter the number of new customers or subscribers acquired (#): ")
            self.salesMarketingCosts = self.userInputandCheck("Enter your sales and marketing costs ($): ")
            self.churnContractionCosts = self.userInputandCheck("Enter your revenue lost in churns and contractions ($): ")
            self.write("\nGreat thank you! The report should be ready in a few seconds...\n")
            sleep(self.userInputSleep / 2)

            return self.totalYears, self.netARR, self.netBurn, self.growthRate, self.MRRperCustomer, self.totalMRR, self.upsellRevenue, \
                   self.grossMargin, self.numberofCustomersAcquired, self.salesMarketingCosts, self.churnContractionCosts