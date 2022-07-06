from time import sleep

class Input:
    userInputSleep = None
    helpGlossary = ''

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

    def __init__(self, sleepTime, helpGlossary):
        self.userInputSleep = sleepTime
        self.helpGlossary = helpGlossary

    def write(self, text):
        print(text)


    def introDirections(self):

        self.write("Welcome to this tool! We're so glad to have you join us.")
        sleep(self.userInputSleep)
        self.write(
            "I hope this program will help you gain a clearer view of your company and help improve your business.")
        sleep(self.userInputSleep)
        self.write("All you have to do is put in some of your business accounts and the program will do the rest!")
        sleep(self.userInputSleep)

        # Basic info
        self.write("Don't worry - this won't take long. You only need 11 numbers at hand.")
        sleep(self.userInputSleep)
        self.write(
            "If you ever want to quit the program, just write and enter the word: 'quit'. If you want to restart, enter the word: 'restart'.")
        sleep(self.userInputSleep)
        self.write(
            "Lastly, an Input Help Guide is available for your reference. If you ever want to access this guide, enter the word 'help'!")
        sleep(self.userInputSleep)

    def userInputandCheck(self, directions):
        userInput = input(directions)
        while userInput == 'help':
            self.write(self.helpGlossary)
            userInput = input(directions)

        if userInput == 'quit':
            quit()
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
                "\nGreat! Now let's fill in the bulk of the data. Please make sure these numbers are only from the last full month (not year).")
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