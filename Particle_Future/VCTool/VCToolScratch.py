from math import *
from time import sleep

# path

path = '/Users/zacharywong/github/zacharywong2023/Particle_Future'

# basic info
totalYears = 3
startingYear = 3
ARR = 20
growthBench = 36
numMetric = 5
def write(text):
    print(text)

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

# calculate % diff between ARR and benchmark
# make growth diff negative if failing benchmark
# metric
burnMultiple = 1.1
CACPayback = 1.48
NRRPercent = 110
growthDiffPercent = calculate_diff(ARR, growthBench)
rule40 = 46

# metric benchmarks
burnMultipleBench = 1
CACPaybackBench = 1
NRRBench = 100
rule40Bench = 40

# Metric Success Desc

burnSuccessDesc = 'burnSuccessDesc\n'
CACSuccessDesc = 'CACSuccessDesc\n'
NRRSuccessDesc = 'This means that your revenue in expansions and upsells are greater than your revenue lost in churns and contractions. ' \
                 'However, check the overall efficiency and profitability of your company since this metric does not account for your gross margins or overall net burn.\n'
growthSuccessDesc = 'growthSuccessDesc\n'
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
finalDescList = []



def incrementIndex(index, list):
    if index + 1 == len(list):
        metricIndex = 0
        #print(metricIndex)
        return metricIndex
    else:
        metricIndex = index + 1
        #print(metricIndex)
        return metricIndex

def updateHelperDicts():
    global metricNameResultDict, metricNameList, metricNameActionStepsDict, metricNameSuccessDescDict, metricNameInputDict, metricNameBenchDict, metricNameComparableDict, metricNameCategoryDict

    metricNameList = [burnMultipleName, CACPaybackName, NRRName, growthName, rule40Name]
    metricBenchList = [burnMultipleBench, CACPaybackBench, NRRBench, growthBench, rule40Bench]
    metricComparableList = [0, 0, 1, 1, 1]
    metricResultList = [burnMultipleResult, CACPaybackResult, NRRResult, growthDiffResult, rule40Result]
    metricNameActionStepsList = [burnActionStepsDesc, CACActionStepsDesc, NRRActionStepsDesc, growthActionStepsDesc, rule40ActionStepsDesc]
    metricNameSuccessDescList = [burnSuccessDesc, CACSuccessDesc, NRRSuccessDesc, growthSuccessDesc, rule40SuccessDesc]
    metricInputList = [burnMultiple, CACPayback, NRRPercent, growthDiffPercent, rule40]
    metricCategoryList = [burnMultipleCategory, CACPaybackCategory, NRRCategory, growthCategory, rule40Category]

    metricNameInputDict = dict(zip(metricNameList, metricInputList))
    metricNameBenchDict = dict(zip(metricNameList, metricBenchList))
    metricNameCategoryDict = dict(zip(metricNameList, metricCategoryList))
    metricNameComparableDict = dict(zip(metricNameList, metricComparableList))
    metricNameActionStepsDict = dict(zip(metricNameList, metricNameActionStepsList))
    metricNameResultDict = dict(zip(metricNameList, metricResultList))
    metricNameSuccessDescDict = dict(zip(metricNameList, metricNameSuccessDescList))
    #print(metricNameResultDict)

def passFailMetric():
    global burnMultipleResult, CACPaybackResult, NRRResult, growthDiffResult, rule40Result
    burnMultipleResult = check_metric(burnMultiple, burnMultipleBench, 0, burnMultipleName)
    sleep(0.5)
    CACPaybackResult = check_metric(CACPayback, CACPaybackBench, 0, CACPaybackName)
    sleep(0.5)
    NRRResult = check_metric(NRRPercent, NRRBench, 1, NRRName)
    sleep(0.5)
    growthDiffResult = check_metric(growthDiffPercent, 0, 1, growthName)
    sleep(0.5)
    rule40Result = check_metric(rule40, rule40Bench, 1, rule40Name)
    sleep(0.5)

    updateHelperDicts()


def addDict(startingIndex, metricDict, descList):
    #print("starting desc List index: " + str(startingIndex))

    descListIndex = startingIndex
    metricIndex = startingIndex + 1

    if descListIndex == len(descList):
        descListIndex = 0

    if metricIndex == len(metricNameList):
        metricIndex = 0

    #print("metric name list index: " + str(metricIndex))


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

    burnBaseDesc = 'Your Burn Multiple is {burnMultiple}x, which is {burnDiff}% worse than {burnMultipleBench}x, ' \
                   'the benchmark of excellent overall company efficiency.\n'.format(burnMultiple = burnMultiple, burnDiff = burnDiff, burnMultipleBench = burnMultipleBench)

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
    #print("starting index: " + str(startingIndex))
    dictCAC = {}
    CACDiff = calculate_diff(CACPayback, CACPaybackBench)

    CACBaseDesc = 'Your CAC Payback Multiple is {CACPayBack}, which is {cacDiff:.2f}% worse than {CACPaybackBench}, ' \
                   'the benchmark of excellent company sales efficiency.'.format(CACPayBack = CACPayback, cacDiff = CACDiff, CACPaybackBench = CACPaybackBench)

    metricNameBaseDescDict[CACPaybackName] = CACBaseDesc

    CACBurnDesc = 'High CAC'
    CACNRRDesc = 'CACNRRDesc'
    CACGrowthDesc = "Since your growth rates are lower than ideal, the problem is most likely due to low returns, specifically a low average MRR per customer"
    CACRule40Desc = 'Bad CAC Payback -> low gross margin% -> high COGS spending-> low profitability'

    descCACList = [CACBurnDesc, CACNRRDesc, CACGrowthDesc, CACRule40Desc]

    addDict(startingIndex, dictCAC, descCACList)


def setUpNRRDict():
    startingIndex = metricNameList.index(NRRName)
    #print("starting index: " + str(startingIndex))
    dictNRR = {}

    NRRBurnDesc = 'Low overall company efficiency: Bad NRR -> high churn -> low net new MRR -> bad burn multiple -> low company efficiency'
    NRRCACDesc = 'Bad NRR ->  high churn / contractions -> high CAC -> low # of new customers acquired / high marketing/sales spend-> low sales efficiency'
    NRRGrowthDesc = 'Bad NRR -> high churn / contractions -> lower revenue -> unsustainable / low growth'
    NRRRule40Desc = 'NRRRule40Desc'

    descNRRList = [NRRBurnDesc, NRRCACDesc, NRRGrowthDesc, NRRRule40Desc]

    addDict(startingIndex, dictNRR, descNRRList)


def setUpGrowthDict():
    startingIndex = metricNameList.index(growthName)
    #print("starting index: " + str(startingIndex))
    dictGrowth = {}
    growthBaseDesc = 'Your growth rate after {totalYears} years is {ARR}, which is {growthDiff:.2f}% worse than {growthBench}, ' \
                   'the benchmark of excellent {growthCategory} at your company stage.'.format(totalYears = totalYears, ARR = ARR, growthDiff = growthDiffPercent, growthBench = growthBench, growthCategory = metricNameCategoryDict['T2D3'])

    metricNameBaseDescDict[growthName] = growthBaseDesc

    growthBurnDesc = 'Bad growth -> low net new ARR -> bad burn multiple -> low company efficiency'
    growthCACDesc = 'Bad Growth -> low # of new customers acquired or low avg MRR -> high CAC Payback Period -> low sales efficiency'
    growthNRRDesc = 'Bad Growth -> low expansions / high churn -> bad NRR -> low product stickiness '
    growthRule40Desc = 'growthRule40Desc'

    descGrowthList = [growthBurnDesc, growthCACDesc, growthNRRDesc, growthRule40Desc]

    addDict(startingIndex, dictGrowth, descGrowthList)


def setUpProfitDict():
    startingIndex = metricNameList.index(rule40Name)
    #print("starting index: " + str(startingIndex))
    dictProfit = {}

    profitBurnDesc = 'Bad Rule of 40 ->  low %Gross Margin-> high COGS spending-> high burn -> bad Burn multiple -> low overall company efficiency'
    profitCACDesc = 'Bad Rule of 40 -> low %gross margin -> high Sales/marketing spending -> Bad CAC Payback time -> low sales efficiency'
    profitNRRDesc = 'Bad Rule of 40 -> low % MRR growth -> high churn -> low product stickiness'
    profitGrowthDesc = 'Bad Rule of 40 -> low % MRR growth -> unsustainable growth'

    descProfitList = [profitBurnDesc, profitCACDesc, profitNRRDesc, profitGrowthDesc]

    addDict(startingIndex, dictProfit, descProfitList)

# def printDesc(metricFailList):
#     for metricFail in metricFailList:
#         baseDesc = metricNameBaseDescDict[metricFail]
#         print(baseDesc)
#         print(finalDescList)

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
            write("Your {metricSuccess} is {metricInput}, which is {metricDiff}% higher than {metricBench}, the benchmark of excellent {metricName}.".format(metricSuccess = metricSuccess, metricInput = metricNameInputDict[metricSuccess], metricDiff = metricDiff, metricBench = metricNameBenchDict[metricSuccess], metricName = metricNameCategoryDict[metricSuccess]))
        else:
            write("Your {metricSuccess} is {metricInput}, which is {metricDiff}% lower than {metricBench}, the benchmark of excellent {metricName}.".format(metricSuccess = metricSuccess, metricInput = metricNameInputDict[metricSuccess], metricDiff = metricDiff, metricBench = metricNameBenchDict[metricSuccess], metricName = metricNameCategoryDict[metricSuccess]))
        write(metricNameSuccessDescDict[metricSuccess])
        index += 1

# go through result dictionary and see if each passes and put in fail list as queue
# go through fail list, get metric name, go to diag, push from queue as key, get value and print
def operateFailMetrics():
    metricFailList = []
    for metric in metricNameList:
        if metricNameResultDict[metric] == 0:
            metricFailList.append(metric)
    #print("metric fail list: " + str(metricFailList))
    index1stLevel = 0
    while index1stLevel < len(metricFailList):
        metricFail1stLevel = metricFailList[index1stLevel]
        baseDesc = metricNameBaseDescDict[metricFail1stLevel]
        write('\n' + metricNameCategoryDict[metricFail1stLevel] + '\n')
        write(baseDesc)
        index2ndLevel = index1stLevel + 1
        if index2ndLevel >= len(metricFailList):
            write("Refer to the report above for further information on " + str(metricFailList[index1stLevel]) + ".\n")
            index1stLevel += 1
            break
        while index2ndLevel < len(metricFailList):
            metricFail2ndLevel = metricFailList[index2ndLevel]
            desc = diagMetricDict[metricFail1stLevel][metricFail2ndLevel]

            # try to print the action steps if there - then pop it out
            try:
                #print(metricNameActionStepsDict)
                write(desc)
                write(metricNameActionStepsDict[metricFail2ndLevel])
                metricNameActionStepsDict.pop(metricFail2ndLevel)
            except Exception:
                write("\nRefer to the previous sections above for potential solutions on how to improve your " + metricNameCategoryDict[metricFail2ndLevel] + ".\n")
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
    #print(diagMetricDict)

def run():
    passFailMetric()
    setUpDiagMetricDict()
    operateSuccessMetrics()
    operateFailMetrics()

if __name__ == '__main__':
    run()
