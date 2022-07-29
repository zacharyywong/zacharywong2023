# This script tests the gen report class
from GenReport import *
from Input import *

#
file = './VCToolDemo-Report.txt'
# Pause Times
writeList = []
metricCalculateSleep = 0.5
userInputSleep = 2

# Growth Inputs
Year0ARR = 2000000
Year1ARR = 6000000 - 2000000
Year2ARR = 18000000 - 6000000
Year3ARR = 36000000 - 18000000
Year4ARR = 72000000 - 36000000
Year5ARR = 1440000000 - 72000000
T2D3StartARR = 2
upperEarlyStage = 10000000
upperGrowthStage = 50000000

# Help Glossary
helpGlossary = """
    MRR = Monthly Recurring Revenue
    ARR = Annual Recurring Revenue
    CAC = Customer Acquisition Cost
    Upsells/Expansions = The amount of revenue gained either due to customers upgrading to a more expensive subscription or purchasing expanded features
    Churn/Contractions = The amount of revenue lost either due to customers cancelling their subscriptions or downgrading to a less expensive version
    % Gross Margin = ((Revenue - the cost of goods sold) / revenue) * 100 
    % Growth Rate = ((Ending ARR last month- Ending ARR two months ago)  / Ending ARR two months ago) * 100
"""

# Metric Benchmarks
burnMultipleBench = 1
CACPaybackBench = 1
NRRBench = 100
growthBench = None
rule40Bench = 40

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

# Metric Comparables
# 0 if it's pass to be below benchmark, 1 if it's pass to be above benchmark
burnMultipleComp = 0
CACPaybackComp = 0
NRRComp = 1
growthComp = 1
rule40Comp = 1

# Descriptions


burnCACDesc = 'burnCACDesc '
burnNRRDesc = 'burnNRRDesc'
burnGrowthDesc = 'burnGrowthDesc'
burnRule40Desc = 'burnRule40Desc'


#CAC Fail descriptions
CACBurnDesc = 'CACBurnDesc'
CACNRRDesc = 'CACNRRDesc'
CACGrowthDesc = 'CACGrowthDesc'
CACRule40Desc = 'CACRule40Desc'


#NRR Fail Descriptions
NRRBurnDesc = 'NRRBurnDesc'
NRRCACDesc ='NRRCACDesc'
NRRGrowthDesc ='NRRGrowthDesc'
NRRRule40Desc = 'NRRRule40Desc'


# Growth Fail Descriptions
growthBurnDesc = 'growthBurnDesc'
growthCACDesc ='growthCACDesc'
growthNRRDesc ='growthNRRDesc'
growthRule40Desc ='growthRule40Desc'


# Rule 40 Fail Descriptions
rule40BurnDesc = 'rule40BurnDesc'
rule40CACDesc = 'rule40CACDesc'
rule40NRRDesc = 'rule40NRRDesc'
rule40GrowthDesc = 'rule40GrowthDesc'

# Burn Fail Descriptions
burnCACDesc = "Since your CAC Payback Period is also high, " \
                  #"the problem most likely lies in the company's high net burn, specifically due to too high of spending used to acquire new customers."

burnNRRDesc = "Since your Net Retention Rate is low, the problem most likely lies in the company's low ARR growth, specifically due to a high rate of churn. A leaky bucket makes it hard to grow efficiently."
burnGrowthDesc = "Your low growth rate may be indicative that you need to go back to the drawing board to ensure that your product or service is what the market truly needs."
burnRule40Desc = "Since your gross margins are low, the problem most likely lies in the company's high net burn, specifically due to high spending COGS. If there’s not operating leverage in the business, the Burn Multiple will not improve with scale."


# CAC Fail descriptions
CACBurnDesc = 'Since your burn multiple is high, the problem is most likely due to high spending on sales and marketing to acquire customers, specifically a high customer acquisition costs'
CACNRRDesc = 'Since your net retention rates are low, the problem may lie in low average MRR per customer, specifically due to high churn and contractions before you have recovered their acquisition costs '
CACGrowthDesc = "Since your growth rates are lower than ideal, the problem is most likely due to low returns, specifically a low average MRR per customer"
CACRule40Desc = 'Since you have not passed the Rule of 40, the problem is most likely due to low gross margins, specifically because of high COGS spending.'


# NRR Fail Descriptions
NRRBurnDesc = 'Since your burn multiple is high, the problem most likely lies in low net new MRR, specifically due to low rates of expansions and upsells'
NRRCACDesc = 'Since your CAC Payback Ratio is high, the problem most likely lies in high churn and contractions, specifically due to a high, restrictive Customer Acquisition Cost'
NRRGrowthDesc = 'Since your growth rates are lower than ideal, the problem lies in low returns, specifically due to the combination of low expansion and upsells and high churn and contractions'
NRRRule40Desc = "While the Rule of 40 can't sufficiently pinpoint why your NRR is low, failing the Rule of 40 may be indicative that you are not growing fast enough. Check your growth rates."


# Growth Fail Descriptions
growthBurnDesc = "The low burn multiple is only further evidence that your growth rates are lower than ideal, It may also indicate that you aren't spending your cash as efficienctly as possible to achieve your low growth rates"
growthCACDesc = "Your high CAC Payback ratio further substantiates the fact that you're acquiring a low number of customers and/or generating low average returns per acquired customer"
growthNRRDesc = 'The low NRR is indicative of a combination of high churn rates and/or low expansions and upsells of your products.'
growthRule40Desc = "Your failure of the Rule of 40 means that your gross margins aren't high enough to compensate for low growth. Please check the Profitability aspects of the report to see what are some potential ways to increase your gross margins."


# Rule 40 Fail Descriptions
rule40BurnDesc = 'Since your burn multiple is also high, the problem most likely lies in a combination of low growth and low % gross margins, specifically due to low growth with a high cash burn.'
rule40CACDesc = 'Since your CAC Payback Ratio is also high, the problem most likely lies in the low % gross margin, specifically due to high sales and marketing spending.'
rule40NRRDesc = 'Since your retention rates are also low, the problem most likely lies in the low % MRR growth, specifically due to high churn of your product'
rule40GrowthDesc = "Your low growth rates means that your groth rates aren't high enough to compensate for low gross margins. Please check the growth aspects of the report to see what are some potential ways to increase your growth."



# Metric Success Descriptions
burnSuccessDesc = 'This means that the amount of revenue that you are earning is greater than the amount of cash you are spending to achieve this growth. ' \
                  'However, check the growth rate of your company. A company with a great burn multiple but low growth means it is not spending enough to achieve its highest potential growth rate. \n'

CACSuccessDesc = "This means that either the costs to acquire your customer is low and/or the amount of revenue you are gaining for each customer acquired is enough to cover your customer acquisition costs in a short time.' \
                 'However, check the retention rates of your product since this metric does not account for churn rates after you have recovered the each customer's acquisition costs. \n"

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

def manualInput():
    totalYears = 4
    netARR = 600000
    netBurn = 5000000
    growthRate = 85
    MRRperCustomer= 10000
    totalMRR = 833333
    upsellRevenue = 1000000
    grossMargin = 85
    numberofCustomersAcquired = 6
    salesMarketingCosts = 200000
    churnContractionCosts = 167777
    return totalYears, netARR, netBurn, growthRate, MRRperCustomer, totalMRR, upsellRevenue, grossMargin, \
        numberofCustomersAcquired, salesMarketingCosts, churnContractionCosts
# Run program with intro, input, and report generator
def run():
    # Intro + Input
    global writeList
    #input = Input(userInputSleep, helpGlossary, file, writeList)
    #input.introDirections()
    #totalYears, netARR, netBurn, growthRate, MRRperCustomer, totalMRR, upsellRevenue, grossMargin, \
    #numberofCustomersAcquired, salesMarketingCosts, churnContractionCosts = input.runUserInput()
    #writeList = input.writeLines()
    #writeList.append('\n')

    totalYears, netARR, netBurn, growthRate, MRRperCustomer, totalMRR, upsellRevenue, grossMargin, \
    numberofCustomersAcquired, salesMarketingCosts, churnContractionCosts = manualInput()

    # Set up Infra
    report = GenReport(metricCalculateSleep, netARR, file, writeList)
    report.calculateStage(T2D3StartARR, netARR, upperEarlyStage, upperGrowthStage)
    T2D3Dict = {0: Year0ARR, 1: Year1ARR, 2: Year2ARR, 3: Year3ARR, 4: Year4ARR, 5: Year5ARR}
    global growthBench
    growthBench = T2D3Dict[totalYears]
    report.calculateMetrics(growthBench, netARR, netBurn, growthRate, MRRperCustomer, totalMRR, upsellRevenue, grossMargin, numberofCustomersAcquired, salesMarketingCosts, churnContractionCosts)
    report.passFailMetric(burnMultipleName, CACPaybackName, NRRName, growthName, rule40Name, burnMultipleBench, CACPaybackBench, NRRBench, growthBench, rule40Bench,
                            burnMultipleComp, CACPaybackComp, NRRComp, growthComp, rule40Comp)
    report.updateHelperDicts(burnMultipleName, CACPaybackName, NRRName, growthName, rule40Name,
                          burnMultipleCategory, CACPaybackCategory, NRRCategory, growthCategory, rule40Category,
                          burnMultipleBench, CACPaybackBench, NRRBench, growthBench, rule40Bench,
                          burnMultipleComp, CACPaybackComp, NRRComp, growthComp, rule40Comp,
                          burnActionStepsDesc, CACActionStepsDesc, NRRActionStepsDesc, growthActionStepsDesc, rule40ActionStepsDesc,
                          burnSuccessDesc, CACSuccessDesc, NRRSuccessDesc, growthSuccessDesc, rule40SuccessDesc)
    # burn Dictionary
    report.setUpMetricDict(burnCACDesc, burnNRRDesc, burnGrowthDesc, burnRule40Desc, burnMultipleName)
    # CAC Dictionary
    report.setUpMetricDict(CACBurnDesc, CACNRRDesc, CACGrowthDesc, CACRule40Desc, CACPaybackName)
    # NRR Dictionary
    report.setUpMetricDict(NRRBurnDesc, NRRCACDesc, NRRGrowthDesc, NRRRule40Desc, NRRName)
    # Growth Dictionary
    report.setUpMetricDict(growthBurnDesc, growthCACDesc, growthNRRDesc, growthRule40Desc, growthName)
    # Rule40 Dictionary
    report.setUpMetricDict(rule40BurnDesc, rule40CACDesc, rule40NRRDesc, rule40GrowthDesc, rule40Name)

    # Generate Report
    #report.writeStage(netARR)
    report.operateSuccessMetrics()
    report.operateFailMetrics()
    writeList = report.writeLines()

    with open(file, 'w') as f:
        f.writelines(writeList)

if __name__ == '__main__':
    run()
