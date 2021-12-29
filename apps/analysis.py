import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, f_oneway

def app():
    st.title('Past Flight Information Analysis')
    df = pd.read_csv('Airasia Domestic Flight Tickets Cleaned (for EDA).csv')
    
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3693611/
    st.write('In general, it is said that Central Limit Theorem “kicks in” at an N of about 30. In other words, as long as the sample is based on 30 or more observations, the sampling distribution of the mean can be safely assumed to be normal. For large sample sizes, significant results would be derived even in the case of a small deviation from normality, although this small deviation will not affect the results of a parametric test ([Reference](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3693611/)).')
    st.markdown('**So we will not checked for normality.**')
    st.write("For all tests, I assume 95% confidence interval and significance level of 0.05.")
    
    # Q1
    st.subheader('1. Is the number of stops causing a significant difference in ticket price?')
    # https://statistics.laerd.com/spss-tutorials/independent-t-test-using-spss-statistics.php
    st.write('Independent Sample T-Test is used to answer this questions as it compares the means between two unrelated, independent groups on the same continuous dependent variable. It requires the dependent variable to be measured on a continuous scale, which is the case for Price. It also needs the independent variable experimented to consist of two categorical, independent groups, which is the case for Stop (0 stands for direct flight and 1 stands for 1 intermediate stop).')
    
    mean_0 = df.loc[df['Stop'] == 0, 'Price (RM)'].mean()
    mean_1 = df.loc[df['Stop'] == 1, 'Price (RM)'].mean()
    # t_stat, pval = ttest_ind(stop_0, stop_1)
    
    t_stat = -90.67
    pval = 0.0
    
    st.write('Mean Price for Direct Flights: RM', round(mean_0,2))
    st.write('Mean Price for One Stop Flights: RM', round(mean_1,2))
    st.write('Test Statistics:', t_stat)
    st.write('P value:', pval)
    if pval > 0.05:
    	st.markdown('Since p value is greater than the critical value 0.05, the number of stops **does not cause a significant difference in ticket price**.')
    else:
        st.markdown('Since p value is smaller than the critical value 0.05, the number of stops **causes a significant difference in ticket price**.')
    st.write("Note that the negative sign in the test statistics can be safely ignored. It indicates that the first group that we plug into the test is the one with lower mean.")
    st.write("As the variances are not approximately equal across groups and the sample sizes for each group differ, the p value is not trustworthy. Thus, the Welch t Test statistic is used. This statistic is also included in the Independent Sample T Test output that is not based on assuming equal population variances. This alternative statistic may be used when equal variances among populations cannot be assumed ([Reference](https://libguides.library.kent.edu/spss/independentttest)).")
    
    
    # Q2
    st.subheader('2. Is there a statistically significant relationship between duration of flights and ticket price?')
    # https://statistics.laerd.com/spss-tutorials/pearsons-product-moment-correlation-using-spss-statistics.php
    st.write('I use **Pearson\'s Correlation** to answer this question as both the dependent variable (Price) and the independent variable (Duration) are continuous.')

    pc = 0.344
    pval = 0.0
    
    st.write('Pearson Correlation Coefficient:', pc)
    st.write('P value:', pval)
    if pval > 0.05:
        st.markdown('Since p value is greater than the critical value 0.05, there is **no significant relationship** between the duration of flights and ticket price**.')
    else:
        st.markdown('Since p value is smaller than the critical value 0.05, there **is a statistically significant relationship between the duration of flights and ticket price**.')
    st.write('There is a positive correlation between duration of flights and ticket price.')
    
    
    # Q3
    st.subheader('3. Is there a statistically significant difference between each departure hour and ticket price?')
    # https://statistics.laerd.com/spss-tutorials/one-way-anova-using-spss-statistics.php
    st.write("Intially, One Way ANOVA seems very suitable for this task as there are two or more categorical independent groups (Note that although duration is in integer value, I treat it as categorical as there will be only a maximum of 24 values allowed for this variable) and the dependent variable (price) is continuous. However, after testing the homogeneity of variance for each comparison group, it outputs a significant result (p < 0.05, signifies that the variances for each comparison group are different and the ANOVA test will not be considered as robust.")
    
    st.image('Q3 - Homogeneity of Variances.PNG')
    # https://statistics.laerd.com/spss-tutorials/kruskal-wallis-h-test-using-spss-statistics.php
    st.write('Thus, **Kruskal Wallis H Test**, the nonparametric alternative to One Way ANOVA is used to answer this question as the dependent variable (Price) is continuous and the independent variable (Departure Hour) consists of 24 categorical independent groups .')
    
    kw = 6687.539
    pval = 0.0
    
    st.write('Test Statistics:',kw)
    st.write('P value:', pval)
    if pval > 0.05:
        st.markdown('Since p value is greater than the critical value 0.05, there is **no significant relationship** between the departure hour and ticket price**.')
    else:
        st.markdown('Since p value is smaller than the critical value 0.05, there **is a statistically significant relationship between the departure hour and ticket price**.')
    st.write("Below is the mean price plot for every duration hour:")
    st.image("Q3 - Means Plot.PNG")
    
    
    # Q4
    st.subheader("4. Is there a statistically significant difference between each departure month and ticket price?")
    # https://statistics.laerd.com/spss-tutorials/one-way-anova-using-spss-statistics.php
    st.write("Intially, One Way ANOVA seems very suitable for this task as there are two or more categorical independent groups (Note that although departure month is in integer value, I treat it as categorical as there will be only a maximum of 12 values allowed for this variable) and the dependent variable (price) is continuous. However, after testing the homogeneity of variance for each comparison group, it outputs a significant result (p < 0.05, signifies that the variances for each comparison group are different and the ANOVA test will not be considered as robust.")
    
    st.image('Q4 - Homogeneity of Variances.PNG')
    # https://statistics.laerd.com/spss-tutorials/kruskal-wallis-h-test-using-spss-statistics.php
    st.write('Thus, **Kruskal Wallis H Test**, the nonparametric alternative to One Way ANOVA is used to answer this question as the dependent variable (Price) is continuous and the independent variable (Departure Hour) consists of a maximum of 12 categorical independent groups .')
    
    kw = 1189.934
    pval = 0.0
    
    st.write('Test Statistics:',kw)
    st.write('P value:', pval)
    if pval > 0.05:
        st.markdown('Since p value is greater than the critical value 0.05, there is **no significant relationship** between the departure month and ticket price**.')
    else:
        st.markdown('Since p value is smaller than the critical value 0.05, there **is a statistically significant relationship between the departure month and ticket price**.')
    st.write("Below is the mean price plot for every departure month:")
    st.image("Q4 - Means Plot.PNG")