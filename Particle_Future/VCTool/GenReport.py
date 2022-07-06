from time import sleep


class GenReport:

    metricCalculateSleep = None
    numMetrics = None

    #stage
    stage1 = False
    stage2 = False
    stage3 = False
    growthCalculate = False

    # Metric Numbers
    metric1 = None
    metric2 = None
    metric3 = None
    metric4 = None
    metric5 = None

    # metric results (1 for pass, 0 for fail)
    metricResult1 = None
    metricResult2 = None
    metricResult3 = None
    metricResult4 = None
    metricResult5 = None

    # Hash Tables and lists
    metricNameList = []
    diagMetricDict = {}

    metricNameCategoryDict = {}
    metricNameComparableDict = {}
    metricNameBenchDict = {}
    metricNameInputDict = {}
    metricNameResultDict = {}
    metricNameBaseDescDict = {}
    metricNameSuccessDescDict = {}
    metricNameActionStepsDict = {}



    def __init__(self, metricCalculateSleep, numMetric = None):
        self.metricCalculateSleep = metricCalculateSleep
        self.numMetric = numMetric

    def write(self, text):
        print(text)

    def inputStage(self, stage):
        if stage == 'early':
            self.stage1 = True
            #self.stageReport = 'You have inputted that you are an early stage company.\n'
        elif stage == 'growth':
            self.stage2 = True
            #self.stageReport = 'You have inputted that you are a growth stage company.\n'
        elif stage == 'late':
            self.stage3 = True
            #self.stageReport = 'You have inputted that you are a late stage company.\n'

    # Calculate which stage the company is in
    def calculateStage(self, startARR, ARR, upperStage1, upperStage2):
        if 0 <= ARR < upperStage1:
            self.stage1 = True
            if ARR >= startARR:
                self.growthCalculate = True

            # see whether to start calculating growth by T2D3


        elif upperStage1 <= ARR <= upperStage2:
            self.stage2 = True
        else:
            self.stage3 = True

    def writeStage(self, netARR):
        if self.stage1:
            self.write('Since you earned {ARR:.0f} ARR in the last 12 full months, you are an early stage company.\n'.format(
                 ARR= netARR))

            if self.growthCalculate:
                self.write(
                   'Since you earned {ARR:.0f} ARR in the last 12 full months, the tool will be measuring your growth against the T2D3 standard.'.format(
                   ARR=netARR))

        elif self.stage2:
            self.write('Since you earned {ARR:.0f} ARR in the last 12 full months, you are a growth stage company.\n'.format(
                 ARR= netARR))

        elif self.stage3:
             self.write('Since you earned {ARR:.0f} ARR in the last 12 full months, you are a late stage company.\n'.format(
                ARR= netARR))


    def calculateDiff(self, input, benchmark):
        metricDiff = ((abs(input - benchmark)) / ((input + benchmark) / 2)) * 100
        if benchmark > input:
            return -round(metricDiff, 2)
        else:
            return round(metricDiff, 2)

    def incrementIndex(self, index, list):
        if index + 1 == len(list):
            metricIndex = 0
            # print(metricIndex)
            return metricIndex
        else:
            metricIndex = index + 1
            # print(metricIndex)
            return metricIndex


    # calculate metrics and check whether pass or fail the benchmarks
    #return metrics
    def calculateMetrics(self, T2D3Dict, years, netARR, netBurn, growthRate, MRRperCustomer, totalMRR, upsellRevenue, grossMargin, numberofCustomersAcquired
                         ,salesMarketingCosts, churnContractionCosts):

        self.metric1 = netBurn / netARR
        self.metric2 = (salesMarketingCosts / numberofCustomersAcquired) * (1 / (MRRperCustomer * grossMargin))
        self.metric3 = ((totalMRR + upsellRevenue - churnContractionCosts) / totalMRR) * 100
        growthBench = T2D3Dict[years]
        self.metric4 = self.calculateDiff(netARR, growthBench)
        self.metric5 = growthRate + grossMargin

    # comparable is 1 when input >= benchmark counts as a pass and 0 when input <= benchmark counts as pass
    def checkMetric(self, input, benchmark, comparable, metricName):
        if comparable == 0:
            if input <= benchmark:
                self.write("Passed " + metricName)
                return 1
            else:
                self.write("Failed " + metricName)
                return 0

        if comparable == 1:
            if input >= benchmark:
                self.write("Passed " + metricName)
                return 1
            else:
                self.write("Failed " + metricName)
                return 0

    def passFailMetric(self,  name1, name2, name3, name4, name5,
                       bench1, bench2, bench3, bench4, bench5,
                       comp1, comp2, comp3, comp4, comp5):
        self.metricResult1 = self.checkMetric(self.metric1, bench1, comp1, name1)
        sleep(self.metricCalculateSleep)
        self.metricResult2 = self.checkMetric(self.metric2, bench2, comp2, name2)
        sleep(self.metricCalculateSleep)
        self.metricResult3 = self.checkMetric(self.metric3, bench3, comp3, name3)
        sleep(self.metricCalculateSleep)
        self.metricResult4 = self.checkMetric(self.metric4, bench4, comp4, name4)
        sleep(self.metricCalculateSleep)
        self.metricResult5 = self.checkMetric(self.metric5, bench5, comp5, name5)
        sleep(self.metricCalculateSleep)


    def updateHelperDicts(self, metricName1, metricName2, metricName3, metricName4, metricName5,
                          metricCategory1, metricCategory2, metricCategory3, metricCategory4, metricCategory5,
                          metricBench1, metricBench2, metricBench3, metricBench4, metricBench5,
                          metricComp1, metricComp2, metricComp3, metricComp4, metricComp5,
                          actionSteps1, actionSteps2, actionSteps3, actionSteps4, actionSteps5,
                          succesDesc1, successDesc2, successDesc3, successDesc4, successDesc5):

        self.metricNameList = [metricName1, metricName2, metricName3, metricName4, metricName5]
        metricCategoryList = [metricCategory1, metricCategory2, metricCategory3, metricCategory4, metricCategory5]
        metricBenchList = [metricBench1, metricBench2, metricBench3, metricBench4, metricBench5]
        metricComparableList = [metricComp1, metricComp2, metricComp3, metricComp4, metricComp5]

        metricInputList = [self.metric1, self.metric2, self.metric3, self.metric4, self.metric5]
        metricResultList = [self.metricResult1, self.metricResult2, self.metricResult3, self.metricResult4, self.metricResult5]

        metricNameSuccessDescList = [succesDesc1, successDesc2, successDesc3, successDesc4, successDesc5]
        metricNameActionStepsList = [actionSteps1, actionSteps2, actionSteps3, actionSteps4, actionSteps5]

        self.metricNameCategoryDict = dict(zip(self.metricNameList, metricCategoryList))
        self. metricNameComparableDict = dict(zip(self.metricNameList, metricComparableList))
        self.metricNameBenchDict = dict(zip(self.metricNameList, metricBenchList))
        self.metricNameInputDict = dict(zip(self.metricNameList, metricInputList))
        self.metricNameResultDict = dict(zip(self.metricNameList, metricResultList))
        self.metricNameSuccessDescDict = dict(zip(self.metricNameList, metricNameSuccessDescList))
        self. metricNameActionStepsDict = dict(zip(self.metricNameList, metricNameActionStepsList))
        # print(metricNameResultDict)

        #return metricNameList, metricNameCategoryDict, metricNameComparableDict, metricNameBenchDict, metricNameInputDict, \
        #       metricNameResultDict, metricNameSuccessDescDict, metricNameActionStepsDict

    def addDict(self, startingIndex, metricDict, descList):
        # print("starting desc List index: " + str(startingIndex))

        descListIndex = startingIndex
        metricIndex = startingIndex + 1

        if descListIndex == len(descList):
            descListIndex = 0

        if metricIndex == len(self.metricNameList):
            metricIndex = 0

        # print("metric name list index: " + str(metricIndex))

        count = 0
        while count < len(descList):
            metricDict[self.metricNameList[metricIndex]] = descList[descListIndex]
            metricIndex = self.incrementIndex(metricIndex, self.metricNameList)
            descListIndex = self.incrementIndex(descListIndex, descList)
            count += 1

        self.diagMetricDict[self.metricNameList[startingIndex]] = metricDict

    # set up all metric Dicts to set up for failed dictionaries
    def setUpMetricDict(self,
                        desc1, desc2, desc3, desc4):

        for metricName in self.metricNameList:
            startingIndex = self.metricNameList.index(metricName)
            metricDict = {}
            metricInput = self.metricNameInputDict[metricName]
            metricBench = self.metricNameBenchDict[metricName]
            metricCategory = self.metricNameCategoryDict[metricName]
            metricDiff = self.calculateDiff(metricInput, metricBench)

            metricBaseDesc = 'Your {metricName} is {metric}, which is {metricDiff:.2f}% worse than {metricBench}, ' \
                      'the benchmark of {metricCategory}.\n'.format(metricName = metricName, metric = metricInput, metricDiff = metricDiff, metricBench = metricBench, metricCategory = metricCategory)
            # update metric name -> base desc dictionary
            self.metricNameBaseDescDict[metricName] = metricBaseDesc

            descMetricList = [desc1, desc2, desc3, desc4]
            self.addDict(startingIndex, metricDict, descMetricList)

    def operateSuccessMetrics(self):
        metricSuccessList = []
        for metric in self.metricNameList:
            if self.metricNameResultDict[metric] == 1:
                metricSuccessList.append(metric)

        index = 0

        self.write("\n\nReport: \n")

        while index < len(metricSuccessList):
            self.write(self.metricNameCategoryDict[metricSuccessList[index]] + '\n')
            metricSuccess = metricSuccessList[index]
            metricDiff = self.calculateDiff(self.metricNameInputDict[metricSuccess],
                                            self.metricNameBenchDict[metricSuccess])
            if self.metricNameComparableDict[metricSuccess] == 1:
                self.write(
                    "Your {metricSuccess} is {metricInput:.2f}, which is {metricDiff}% higher than {metricBench}, the benchmark of excellent {metricName}.".format(
                        metricSuccess=metricSuccess, metricInput=self.metricNameInputDict[metricSuccess],
                        metricDiff=metricDiff, metricBench=self.metricNameBenchDict[metricSuccess],
                        metricName=self.metricNameCategoryDict[metricSuccess]))
            else:
                self.write(
                    "Your {metricSuccess} is {metricInput:.2f}, which is {metricDiff}% lower than {metricBench}, the benchmark of excellent {metricName}.".format(
                        metricSuccess=metricSuccess, metricInput= self.metricNameInputDict[metricSuccess],
                        metricDiff=metricDiff, metricBench = self.metricNameBenchDict[metricSuccess],
                        metricName= self.metricNameCategoryDict[metricSuccess]))
            self.write(self.metricNameSuccessDescDict[metricSuccess])
            index += 1


    # go through result dictionary and see if each passes and put in fail list as queue
    # go through fail list, get metric name, go to diag, push from queue as key, get value and print
    def operateFailMetrics(self):
        metricFailList = []
        # put all failed metrics in a list
        for metric in self.metricNameList:
            if self.metricNameResultDict[metric] == 0:
                metricFailList.append(metric)
        # print("metric fail list: " + str(metricFailList))

        # get the base desc for each failed metric
        index1stLevel = 0
        while index1stLevel < len(metricFailList):
            metricFail1stLevel = metricFailList[index1stLevel]
            baseDesc = self.metricNameBaseDescDict[metricFail1stLevel]
            self.write('\n' + self.metricNameCategoryDict[metricFail1stLevel] + '\n')
            self.write(baseDesc)

            index2ndLevel = index1stLevel + 1
            # if there's no other 2nd level metric, then the 1st level metric must have already been addressed in the previous sections

            if index2ndLevel >= len(metricFailList):
                self.write("Refer to the report above for further information on " + str(
                    metricFailList[index1stLevel]) + ".\n")
                index1stLevel += 1
                break

            # print the corresponding 2nd level metric description for the 1st level metric
            while index2ndLevel < len(metricFailList):
                metricFail2ndLevel = metricFailList[index2ndLevel]
                desc = self.diagMetricDict[metricFail1stLevel][metricFail2ndLevel]

                # try to print the action steps if there - then pop it out
                # if no action steps there, that means already printed in earlier section
                try:
                    self.write(desc)
                    self.write(self.metricNameActionStepsDict[metricFail2ndLevel])
                    self.metricNameActionStepsDict.pop(metricFail2ndLevel)
                except Exception:
                    self.write("Refer to the previous sections above for potential solutions on how to improve your " +
                                self.metricNameCategoryDict[metricFail2ndLevel] + ".\n")
                    index2ndLevel += 1
                else:
                    index2ndLevel += 1
                    continue
            index1stLevel += 1
