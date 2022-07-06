from math import *
from time import sleep
import sys



T2D3Dict = {0: 2, 1: 6, 2: 18, 3: 36, 4: 72, 5: 144}
numMetric = 5
userInputSleep = 2.5
metricCalculateSleep = 0.5
restart = True

# path
path = '/'

helpGlossary = """
    MRR = Monthly Recurring Revenue
    ARR = Annual Recurring Revenue
    CAC = Customer Acquisition Cost
    Upsells/Expansions = The amount of revenue gained either due to customers upgrading to a more expensive subscription or purchasing expanded features
    Churn/Contractions = The amount of revenue lost either due to customers cancelling their subscriptions or downgrading to a less expensive version
    % Gross Margin = ((Revenue - the cost of goods sold) / revenue) * 100 
    % Growth Rate = ((Ending ARR last month- Ending ARR two months ago)  / Ending ARR two months ago) * 100
"""

def write(text):
    print(text)

def calculate_diff(Input, Benchmark):
    metricDiff = ((abs(Input - Benchmark)) / ((Input + Benchmark) / 2)) * 100
    if Benchmark > Input:
        return -round(metricDiff, 2)
    else:
        return round(metricDiff, 2)

# Inputs:

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

# Results
totalYears = None
burnMultiple = None
CACPayback = None
NRRPercent = None
growthDiffPercent = None
rule40 = None

# Metric Numbers
burnMultiple = None
CACPayback = None
NRRPercent = None
growthDiffPercent = None
rule40 = None

# metric benchmarks
burnMultipleBench = 1
CACPaybackBench = 1
NRRBench = 100
growthBench = None
rule40Bench = 40

def calculateMetrics():
    global burnMultiple, CACPayback, NRRPercent, growthBench, growthDiffPercent, rule40

    burnMultiple = netBurn / netARR
    CACPayback = (salesMarketingCosts / numberofCustomersAcquired) * (1 / (MRRperCustomer * grossMargin))
    NRRPercent = ((totalMRR + upsellRevenue - churnContractionCosts) / totalMRR) * 100
    growthBench = T2D3Dict[totalYears]
    growthDiffPercent = calculate_diff(netARR, growthBench)
    rule40 = growthRate + grossMargin

def checkRestart(input):
    global restart
    if input == 'restart':
        write("\nThe program has restarted!")
        userInput()

def userInputandCheck(directions):
    userInput = input(directions)
    while userInput == 'help':
        write(helpGlossary)
        userInput = input(directions)

    if userInput == 'quit':
        quit()
    elif userInput == 'restart':
        checkRestart(userInput)
    else:
        return float(userInput)

def introDirections():

    write("Welcome to this tool! We're so glad to have you join us.")
    sleep(userInputSleep)
    write("I hope this program will help you gain a clearer view of your company and help improve your business.")
    sleep(userInputSleep)
    write("All you have to do is put in some of your business accounts and the program will do the rest!")
    sleep(userInputSleep)

    # Basic info
    write("Don't worry - this won't take long. You only need 11 numbers at hand.")
    sleep(userInputSleep)
    write(
        "If you ever want to quit the program, just write and enter the word: 'quit'. If you want to restart, enter the word: 'restart'.")
    sleep(userInputSleep)
    write(
        "Lastly, an Input Help Guide is available for your reference. If you ever want to access this guide, enter the word 'help'!")
    sleep(userInputSleep)

def userInput():
    global restart, totalYears, netARR, netBurn, growthRate, MRRperCustomer, totalMRR, upsellRevenue, grossMargin, numberofCustomersAcquired, salesMarketingCosts, churnContractionCosts

    # basic info
    while restart == True:
        totalYears = userInputandCheck("\nTo begin, enter how many years your company has been in operation: ")
        if totalYears == 'restart' and restart:
            userInput()
        elif not restart:
            return
        # yearly info
        write("\nGreat! Now let's fill in some data from the last full 12 months")
        sleep(userInputSleep / 2)
        netARR = userInputandCheck("Enter your Net ARR from the last full 12 months: ")
        netBurn = userInputandCheck("Enter your Net Burn from the last full 12 months: ")

        # monthly info
        write(
            "\nGreat! Now let's fill in the bulk of the data. Please make sure these numbers are only from the last full month (not year).")
        sleep(userInputSleep)
        growthRate = userInputandCheck("Enter your MRR Growth Rate (%): ")
        MRRperCustomer = userInputandCheck("Enter your Average MRR per customer ($): ")
        totalMRR = userInputandCheck("Enter your total MRR at the start of the last month ($): ")
        upsellRevenue = userInputandCheck("Enter your revenue in expansions and upsells ($): ")
        grossMargin = userInputandCheck("Enter your Gross Margin (%): ")
        numberofCustomersAcquired = userInputandCheck(
            "Enter the number of new customers or subscribers acquired (#): ")
        salesMarketingCosts = userInputandCheck("Enter your sales and marketing costs ($): ")
        churnContractionCosts = userInputandCheck("Enter your revenue lost in churns and contractions ($): ")
        restart = False
        write("\nGreat thank you! The report should be ready in a few seconds...\n")
        sleep(userInputSleep / 2)

## Output

# basic info

def calculate_diff(Input, Benchmark):
    metricDiff = ((abs(Input - Benchmark)) / ((Input + Benchmark) / 2)) * 100
    if Benchmark > Input:
        return -round(metricDiff, 2)
    else:
        return round(metricDiff, 2)

# comparable is 1 when input >= benchmark counts as a pass and 0 when input <= benchmark counts as pass
def check_metric(input, benchmark, comparable, metricName):
    if comparable == 0:
        if input <= benchmark:
            write("Passed " + metricName)
            return 1
        else:
            write("Failed " + metricName)
            return 0

    if comparable == 1:
        if input >= benchmark:
            write("Passed " + metricName)
            return 1
        else:
            write("Failed " + metricName)
            return 0

# Metric Names
burnMultipleName = 'Burn Multiple'
CACPaybackName = 'CAC Payback Period'
NRRName = 'Net Retention Rate'
growthName = 'T2D3'
rule40Name = 'Rule of 40'

# Metric Categories

burnMultipleCategory = 'Overall Company Efficiency'
CACPaybackCategory = 'Overall Sales Efficiency'
NRRCategory = 'Overall Product Retention'
growthCategory = 'Growth Rate'
rule40Category = 'Profitability'

# metric results (1 for pass, 0 for fail)
burnMultipleResult = None
CACPaybackResult = None
NRRResult = None
growthDiffResult = None
rule40Result = None

# Metric Success Desc

burnSuccessDesc = 'This means that the amount of revenue that you are earning is greater than the amount of cash you are spending to achieve this growth. ' \
                  'However, check the growth rate of your company. A company with a great burn multiple but low growth means it is not spending enough to achieve its highest potential growth rate. \n'

CACSuccessDesc = "This means that either the costs to acquire your customer is low and/or the amount of revenue you are gaining for each customer acquired is enough to cover your customer acquisition costs in a short time.' \
                 'However, mcheck the retention rates of your product since this metric does not account for churn rates after you have recovered the each customer's acquisition costs. \n"

NRRSuccessDesc = 'This means that your revenue in expansions and upsells are greater than your revenue lost in churns and contractions. ' \
                 'However, check the overall efficiency and profitability of your company since this metric does not account for your gross margins or overall net burn.\n'

growthSuccessDesc = 'This means that the you are on the way to becoming a high exit company at IPO. However, check the overall efficiency of your spending and the retention' \
                    'of your product to ensure that your burn or churn rates are not negating each sale that you make. \n'

rule40SuccessDesc = "This means that you are either at least somewhat profitable or growing at an extremely high pace to compensate for low or negative gross margins.\n" \
                    "However, if you're at early stages, check the growth rate of your company. If you're near a 20 / 20 split, you have passed the Rule of 40 but still be stuck in sub-scale growth mode.\n" \
                    "Avoid focusing too much on profitability too early on, which can sacrifice growth, hurt your valuations, and hinder opportunities to lower your Customer Acquisition Costs. \n"

# Metric Action Steps

burnActionStepsDesc = "Burn Action Steps Desc\n"

CACActionStepsDesc = "1. Check if the company can narrow its target market to reduce burn\n" \
                     "2. See if there are more effective marketing techniques for each target segment to lower the CAC\n" \
                     "3. Check whether the company is targeting the wrong audience\n" \
                     "4. Check to see if company is focusing on least-cost customer acquisition channels\n" \
                     "5. Loss of business champion / executive sponsor\n"

NRRActionStepsDesc = "1. Check if there is easy onboarding for customers.\n" \
                     "2. Check if there are enough new features.\n" \
                     "3. Check whether consumers know how to use the product.\n" \
                     "4. Check your Net Promoter Score.\n"

growthActionStepsDesc = "1. Check if there is a high enough willingness to pay for the product.\n" \
                        "2. Check whether the problem is actually tackling a necessary problem in the market.\n" \
                        "3. Check whether the product is useful. \n" \
                        "4. Check whether there is low barrier to entry into the product -> can introduce usage-based pricing or free trials.\n"

rule40ActionStepsDesc = "1. Check whether there are ways to increase R&D efficiency and cut waste\n" \
                        "2. Check is there are ways to make the most of your premises\n" \
                        "3. Check whether you can negotiate better terms with your suppliers or change your use model\n" \
                        "4. Check whether there are any overheads that can be cut\n"

# Hash Tables and lists
metricNameList = []
diagMetricDict = {}

metricNameInputDict = {}
metricNameBenchDict = {}
metricNameComparableDict = {}
metricNameCategoryDict = {}
metricNameResultDict = {}
metricNameBaseDescDict = {}
metricNameSuccessDescDict = {}
metricNameActionStepsDict = {}

def incrementIndex(index, list):
    if index + 1 == len(list):
        metricIndex = 0
        # print(metricIndex)
        return metricIndex
    else:
        metricIndex = index + 1
        # print(metricIndex)
        return metricIndex

def updateHelperDicts():
    global metricNameResultDict, metricNameList, metricNameActionStepsDict, metricNameSuccessDescDict, metricNameInputDict, metricNameBenchDict, metricNameComparableDict, metricNameCategoryDict

    metricNameList = [burnMultipleName, CACPaybackName, NRRName, growthName, rule40Name]
    metricBenchList = [burnMultipleBench, CACPaybackBench, NRRBench, growthBench, rule40Bench]
    metricComparableList = [0, 0, 1, 1, 1]
    metricResultList = [burnMultipleResult, CACPaybackResult, NRRResult, growthDiffResult, rule40Result]
    metricNameActionStepsList = [burnActionStepsDesc, CACActionStepsDesc, NRRActionStepsDesc, growthActionStepsDesc,
                                 rule40ActionStepsDesc]
    metricNameSuccessDescList = [burnSuccessDesc, CACSuccessDesc, NRRSuccessDesc, growthSuccessDesc,
                                 rule40SuccessDesc]
    metricInputList = [burnMultiple, CACPayback, NRRPercent, growthDiffPercent, rule40]
    metricCategoryList = [burnMultipleCategory, CACPaybackCategory, NRRCategory, growthCategory, rule40Category]

    metricNameInputDict = dict(zip(metricNameList, metricInputList))
    metricNameBenchDict = dict(zip(metricNameList, metricBenchList))
    metricNameCategoryDict = dict(zip(metricNameList, metricCategoryList))
    metricNameComparableDict = dict(zip(metricNameList, metricComparableList))
    metricNameActionStepsDict = dict(zip(metricNameList, metricNameActionStepsList))
    metricNameResultDict = dict(zip(metricNameList, metricResultList))
    metricNameSuccessDescDict = dict(zip(metricNameList, metricNameSuccessDescList))
    # print(metricNameResultDict)

def passFailMetric():
    global burnMultipleResult, CACPaybackResult, NRRResult, growthDiffResult, rule40Result
    burnMultipleResult = check_metric(burnMultiple, burnMultipleBench, 0, burnMultipleName)
    sleep(metricCalculateSleep)
    CACPaybackResult = check_metric(CACPayback, CACPaybackBench, 0, CACPaybackName)
    sleep(metricCalculateSleep)
    NRRResult = check_metric(NRRPercent, NRRBench, 1, NRRName)
    sleep(metricCalculateSleep)
    growthDiffResult = check_metric(growthDiffPercent, 0, 1, growthName)
    sleep(metricCalculateSleep)
    rule40Result = check_metric(rule40, rule40Bench, 1, rule40Name)
    sleep(metricCalculateSleep)

    updateHelperDicts()

def addDict(startingIndex, metricDict, descList):
    # print("starting desc List index: " + str(startingIndex))

    descListIndex = startingIndex
    metricIndex = startingIndex + 1

    if descListIndex == len(descList):
        descListIndex = 0

    if metricIndex == len(metricNameList):
        metricIndex = 0

    # print("metric name list index: " + str(metricIndex))

    count = 0
    while count < len(descList):
        metricDict[metricNameList[metricIndex]] = descList[descListIndex]
        metricIndex = incrementIndex(metricIndex, metricNameList)
        descListIndex = incrementIndex(descListIndex, descList)
        count += 1

    global diagMetricDict
    diagMetricDict[metricNameList[startingIndex]] = metricDict

def setUpBurnDict():
    # for Burn Multiple
    startingIndex = metricNameList.index(burnMultipleName)
    dictBurn = {}
    burnDiff = calculate_diff(burnMultiple, burnMultipleBench)

    burnBaseDesc = 'Your Burn Multiple is {burnMultiple:.2f}x, which is {burnDiff:.2f}% worse than {burnMultipleBench}x, ' \
                   'the benchmark of excellent overall company efficiency.\n'.format(burnMultiple=burnMultiple,
                                                                                     burnDiff=burnDiff,
                                                                                     burnMultipleBench=burnMultipleBench)

    # update metric name -> base desc dictionary
    metricNameBaseDescDict[burnMultipleName] = burnBaseDesc

    burnCACDesc = "Since your CAC Payback Period is also high, " \
                  "the problem most likely lies in the company's high net burn, specifically due to too high of spending used to acquire new customers."

    burnNRRDesc = "Since your Net Retention Rate is low, the problem most likely lies in the company's low ARR growth, specifically due to a high rate of churn. A leaky bucket makes it hard to grow efficiently."
    burnGrowthDesc = "Your low growth rate may be indicative that you need to go back to the drawing board to ensure that your product or service is what the market truly needs."
    burnRule40Desc = "Since your gross margins are low, the problem most likely lies in the company's high net burn, specifically due to high spending COGS. If there’s not operating leverage in the business, the Burn Multiple will not improve with scale."

    descBurnList = [burnCACDesc, burnNRRDesc, burnGrowthDesc, burnRule40Desc]
    addDict(startingIndex, dictBurn, descBurnList)

def setUpCACDict():
    startingIndex = metricNameList.index(CACPaybackName)
    # print("starting index: " + str(startingIndex))
    dictCAC = {}
    CACDiff = calculate_diff(CACPayback, CACPaybackBench)

    CACBaseDesc = 'Your CAC Payback Multiple is {CACPayBack:.2f}, which is {cacDiff:.2f}% worse than {CACPaybackBench}, ' \
                  'the benchmark of excellent company sales efficiency.\n'.format(CACPayBack=CACPayback,
                                                                                  cacDiff=CACDiff,
                                                                                  CACPaybackBench=CACPaybackBench)

    metricNameBaseDescDict[CACPaybackName] = CACBaseDesc

    CACBurnDesc = 'Since your burn multiple is high, the problem is most likely due to high spending on sales and marketing to acquire customers, specifically a high customer acquisition costs'
    CACNRRDesc = 'Since your net retention rates are low, the problem may lie in low average MRR per customer, to specifically due to high churn and contractions before you have recovered their acquisition costs '
    CACGrowthDesc = "Since your growth rates are lower than ideal, the problem is most likely due to low returns, specifically a low average MRR per customer"
    CACRule40Desc = 'Since you have not passed the Rule of 40, the problem is most likely due to low gross margins, specifically because of high COGS spending.'

    descCACList = [CACBurnDesc, CACNRRDesc, CACGrowthDesc, CACRule40Desc]

    addDict(startingIndex, dictCAC, descCACList)

def setUpNRRDict():
    startingIndex = metricNameList.index(NRRName)
    # print("starting index: " + str(startingIndex))
    dictNRR = {}

    # update nrr base description
    NRRDiff = calculate_diff(NRRPercent, NRRBench)
    NRRBaseDesc = 'Your Net Retention Rate is {NRRPercent:.2f}, which is {NRRDiff:.2f}% worse than {NRRBench}, ' \
                  'the benchmark of excellent product retention.\n'.format(NRRPercent=NRRPercent, NRRDiff=NRRDiff,
                                                                           NRRBench=NRRBench)

    # update metric name -> base desc dictionary
    metricNameBaseDescDict[NRRName] = NRRBaseDesc

    NRRBurnDesc = 'Since your burn multiple is high, the problem most likely lies in low net new MRR, specifically due to low rates of expansions and upsells'
    NRRCACDesc = 'Since your CAC Payback Ratio is high, the problem most likely lies in high churn and contractions, specifically due to a high, restrictive Customer Acquisition Cost'
    NRRGrowthDesc = 'Since your growth rates are lower than ideal, the problem lies in low returns, specifically due to the combination of low expansion and upsells and high churn and contractions'
    NRRRule40Desc = "While the Rule of 40 can't sufficiently pinpoint why your NRR is low, failing the Rule of 40 may be indicative that you are not growing fast enough. Check your growth rates."

    descNRRList = [NRRBurnDesc, NRRCACDesc, NRRGrowthDesc, NRRRule40Desc]

    addDict(startingIndex, dictNRR, descNRRList)

def setUpGrowthDict():
    startingIndex = metricNameList.index(growthName)
    # print("starting index: " + str(startingIndex))
    dictGrowth = {}
    growthBaseDesc = 'Your growth rate after {totalYears} years is {ARR}, which is {growthDiff:.2f}% worse than {growthBench}, ' \
                     'the benchmark of excellent {growthCategory} at your company stage.\n'.format(
        totalYears=totalYears, ARR=netARR, growthDiff=growthDiffPercent, growthBench=growthBench,
        growthCategory=metricNameCategoryDict['T2D3'])

    metricNameBaseDescDict[growthName] = growthBaseDesc

    growthBurnDesc = "The low burn multiple is only further evidence that your growth rates are lower than ideal, It may also indicate that you aren't spending your cash as efficienctly as possible to achieve your low growth rates"
    growthCACDesc = "Your high CAC Payback ratio further substantiates the fact that you're acquiring a low number of customers and/or generating low average returns per acquired customer"
    growthNRRDesc = 'The low NRR is indicative of a combination of high churn rates and/or low expansions and upsells of your products.'
    growthRule40Desc = "Your failure of the Rule of 40 means that your gross margins aren't high enough to compensate for low growth. Please check the Profitability aspects of the report to see what are some potential ways to increase your gross margins."

    descGrowthList = [growthBurnDesc, growthCACDesc, growthNRRDesc, growthRule40Desc]

    addDict(startingIndex, dictGrowth, descGrowthList)

def setUpProfitDict():
    startingIndex = metricNameList.index(rule40Name)
    # print("starting index: " + str(startingIndex))
    dictRule40 = {}
    # update nrr base description
    rule40Diff = calculate_diff(rule40, rule40Bench)
    rule40BaseDesc = 'Your Rule of 40 is {rule40}, which is {rule40Diff:.2f}% worse than {rule40Bench}, ' \
                     'the benchmark of excellent foundation for sustainable company success.\n'.format(
        rule40=rule40, rule40Diff=rule40Diff,
        rule40Bench=rule40Bench)

    # update metric name -> base desc dictionary
    metricNameBaseDescDict[rule40Name] = rule40BaseDesc

    rule40BurnDesc = 'Since your burn multiple is also high, the problem most likely lies in a combination of low growth and low % gross margins, specifically due to low growth with a high cash burn.'
    rule40CACDesc = 'Since your CAC Pauback Ratio is also high, the problem most likely lies in the low % gross margin, specifically due to high sales and marketing spending.'
    rule40NRRDesc = 'Since your retention rates are also low, the problem most likely lies in the low % MRR growth, specifically due to high churn of your product'
    rule40GrowthDesc = "Your low growth rates means that your groth rates aren't high enough to compensate for low gross margins. Please check the growth aspects of the report to see what are some potential ways to increase your growth."
    descRule40List = [rule40BurnDesc, rule40CACDesc, rule40NRRDesc, rule40GrowthDesc]

    addDict(startingIndex, dictRule40, descRule40List)

def operateSuccessMetrics():
    metricSuccessList = []
    for metric in metricNameList:
        if metricNameResultDict[metric] == 1:
            metricSuccessList.append(metric)

    index = 0

    write("\n\nReport: \n")

    while index < len(metricSuccessList):
        write(metricNameCategoryDict[metricSuccessList[index]] + '\n')
        metricSuccess = metricSuccessList[index]
        metricDiff = calculate_diff(metricNameInputDict[metricSuccess], metricNameBenchDict[metricSuccess])
        if metricNameComparableDict[metricSuccess] == 1:
            write(
                "Your {metricSuccess} is {metricInput:.2f}, which is {metricDiff}% higher than {metricBench}, the benchmark of excellent {metricName}.".format(
                    metricSuccess=metricSuccess, metricInput=metricNameInputDict[metricSuccess],
                    metricDiff=metricDiff, metricBench=metricNameBenchDict[metricSuccess],
                    metricName=metricNameCategoryDict[metricSuccess]))
        else:
            write(
                "Your {metricSuccess} is {metricInput:.2f}, which is {metricDiff}% lower than {metricBench}, the benchmark of excellent {metricName}.".format(
                    metricSuccess=metricSuccess, metricInput=metricNameInputDict[metricSuccess],
                    metricDiff=metricDiff, metricBench=metricNameBenchDict[metricSuccess],
                    metricName=metricNameCategoryDict[metricSuccess]))
        write(metricNameSuccessDescDict[metricSuccess])
        index += 1

# go through result dictionary and see if each passes and put in fail list as queue
# go through fail list, get metric name, go to diag, push from queue as key, get value and print
def operateFailMetrics():
    metricFailList = []
    # put all failed metrics in a list
    for metric in metricNameList:
        if metricNameResultDict[metric] == 0:
            metricFailList.append(metric)
    # print("metric fail list: " + str(metricFailList))

    # get the base desc for each failed metric
    index1stLevel = 0
    while index1stLevel < len(metricFailList):
        metricFail1stLevel = metricFailList[index1stLevel]
        baseDesc = metricNameBaseDescDict[metricFail1stLevel]
        write('\n' + metricNameCategoryDict[metricFail1stLevel] + '\n')
        write(baseDesc)

        index2ndLevel = index1stLevel + 1
        # if there's no other 2nd level metric, then the 1st level metric must have already been addressed in the previous sections
        if index2ndLevel >= len(metricFailList):
            write("Refer to the report above for further information on " + str(
                metricFailList[index1stLevel]) + ".\n")
            index1stLevel += 1
            break

        # print the corresponding 2nd level metric description for the 1st level metric
        while index2ndLevel < len(metricFailList):
            metricFail2ndLevel = metricFailList[index2ndLevel]
            desc = diagMetricDict[metricFail1stLevel][metricFail2ndLevel]

            # try to print the action steps if there - then pop it out
            # if no action steps there, that means already printed in earlier section
            try:
                write(desc)
                write(metricNameActionStepsDict[metricFail2ndLevel])
                metricNameActionStepsDict.pop(metricFail2ndLevel)
            except Exception:
                write("Refer to the previous sections above for potential solutions on how to improve your " +
                      metricNameCategoryDict[metricFail2ndLevel] + ".\n")
                index2ndLevel += 1
            else:
                index2ndLevel += 1
                continue
        index1stLevel += 1

def setUpDiagMetricDict():
    setUpBurnDict()
    setUpCACDict()
    setUpNRRDict()
    setUpGrowthDict()
    setUpProfitDict()
    # print(diagMetricDict)

def run():
    introDirections()
    userInput()
    calculateMetrics()
    passFailMetric()
    setUpDiagMetricDict()
    operateSuccessMetrics()
    operateFailMetrics()

if __name__ == '__main__':
    run()
