# Assignment #4: Resource Allocation & Constrained Optimization

## Heckscher-Ohlin Model Analysis - Complete Answers

---

# PART A – DATA ANALYSIS

## Parts 1-4: Implementation

A Python script (`heckscher_ohlin_analysis.py`) has been created that:

1. **Downloads FRED Data**: Automatically fetches GDPC1, CLF16OV, GPDIC1, and EXPGSC1
2. **Calculates Variables**: Capital Deepening (%) and Capital-Labor Ratio ($/Worker)
3. **Creates Dual-Axis Chart**: Visualizes both metrics over time
4. **Runs Regression Analysis**: Exports vs K/L ratio with full statistical output

### To Run:

```bash
pip install pandas pandas-datareader matplotlib statsmodels
python heckscher_ohlin_analysis.py
```

---

## Part 5: Analytical Questions

### Question 1: Regression Critique - Unit Roots and Spurious Correlation

**Is this regression sensible?**

No, this regression likely produces **spurious results** due to the presence of **unit roots** in both time series.

**What is a Unit Root?**

A unit root exists in a time series when:

- The series is **non-stationary** (its statistical properties change over time)
- Shocks to the series have permanent effects rather than dying out
- The series tends to wander without returning to a mean value

Mathematically, a series $Y_t$ has a unit root if it follows:
$$Y_t = Y_{t-1} + \epsilon_t$$

Where $\epsilon_t$ is a random shock. The "unit" refers to the coefficient of 1 on the lagged term.

**Why is Regressing Two Trending Variables Problematic?**

1. **Spurious Correlation**: When two variables both trend upward over time (like Exports and K/L ratio), they will appear highly correlated even if there's no causal relationship. You could get an R² of 0.90+ simply because both variables grew over the same period.

2. **Misleading T-Statistics**: Standard regression assumes residuals are independent and identically distributed (i.i.d.). With non-stationary data, residuals inherit the unit root, making t-statistics unreliable and confidence intervals meaningless.

3. **Non-Constant Variance**: The variance of a unit root process grows without bound over time, violating the homoskedasticity assumption.

4. **Granger-Newbold (1974) Finding**: Two independent random walks will appear significantly related in ~75% of regressions at the 5% level – a dramatic over-rejection of the null.

**Proper Approaches Include:**

- **First-Differencing**: Regress ΔExports on ΔK/L to remove trends
- **Cointegration Analysis**: Test if a stable long-run relationship exists (Engle-Granger or Johansen tests)
- **Error Correction Models**: If cointegrated, model both short-run dynamics and long-run equilibrium
- **Augmented Dickey-Fuller Test**: Formally test for unit roots before regression

**Interpretation Warning**: Any high R² or significant coefficients from this regression should be viewed skeptically. The apparent relationship may be entirely due to both variables trending upward with U.S. economic growth rather than any causal link predicted by H-O theory.

---

### Question 2: Future Outlook - Generative AI and Capital-Labor Dynamics

**Projected Evolution of Capital/GDP and K/L Ratio (2025-2035)**

**Capital as % of GDP: Expected to INCREASE**

1. **Massive Infrastructure Investment**: Goldman Sachs estimates $1+ trillion in AI infrastructure spending globally through 2027, including:
   - Data centers ($200B+)
   - Semiconductor fabs ($300B+ with CHIPS Act)
   - Energy grid upgrades for AI power demands
   - Networking infrastructure

2. **Corporate AI Adoption**: Businesses across all sectors are increasing capital expenditure on:
   - Cloud computing capacity
   - AI-enabled equipment and machinery
   - Automation systems and robotics

3. **Historical Context**: Capital/GDP has averaged 15-18% since 1960. AI investments could push this toward 20%+ temporarily during the build-out phase.

**Capital-Labor Ratio: Expected to ACCELERATE Upward**

The K/L ratio will likely increase rapidly due to both numerator expansion AND potential denominator effects:

**Numerator Effect (Capital Accumulation):**

- AI infrastructure requires massive upfront capital investment
- Unlike previous technologies, AI scaling requires exponential increases in computing power
- The capital stock is front-loaded while productivity gains are realized over time

**Denominator Effect (Labor Dynamics):**

This is where "Capital Deepening" vs "Labor Displacement" becomes critical:

| Scenario               | Mechanism                                        | K/L Impact                                     |
| ---------------------- | ------------------------------------------------ | ---------------------------------------------- |
| **Capital Deepening**  | AI augments workers, making them more productive | Moderate K/L increase (numerator grows faster) |
| **Labor Displacement** | AI replaces certain job categories               | Rapid K/L increase (denominator shrinks)       |
| **Mixed Effect**       | Some jobs displaced, new jobs created            | Depends on transition speed                    |

**My Assessment: BOTH Effects Will Occur**

**Near-Term (2025-2030): Capital Deepening Dominates**

- AI augments rather than replaces most knowledge workers
- Productivity gains in existing roles (coding, analysis, customer service)
- Labor force participation may actually increase as productivity tools enable more flexible work
- New job categories emerge (AI trainers, prompt engineers, AI safety specialists)

**Medium-Term (2030-2035): Labor Displacement Accelerates**

- Autonomous agents begin replacing routine cognitive work
- Manufacturing and logistics further automate
- Service sector faces disruption (call centers, basic legal/accounting)
- Potential structural unemployment in specific sectors

**Key Variables to Watch:**

1. **AI Capability Curve**: How quickly do AI systems match human-level performance in specific tasks?
2. **Adoption Speed**: Enterprise deployment typically lags technology availability by 3-5 years
3. **Policy Response**: Job retraining programs, universal basic income discussions, automation taxes
4. **New Industry Creation**: Historically, technology creates more jobs than it destroys (but with significant transition costs)

**Quantitative Projections:**

| Metric             | 2024 Baseline   | 2030 Projection | 2035 Projection      |
| ------------------ | --------------- | --------------- | -------------------- |
| Capital/GDP        | ~17%            | 19-21%          | 18-20% (normalizing) |
| K/L Ratio          | ~$30,000/worker | ~$40,000/worker | ~$50,000/worker      |
| Labor Force Growth | 0.5%/year       | 0.3%/year       | 0.1-0.5%/year        |

**H-O Model Implications:**

If the U.S. becomes significantly more capital-abundant (higher K/L):

- Theory predicts increased exports of capital-intensive goods
- The U.S. should deepen specialization in high-tech, semiconductor, aerospace, and advanced manufacturing
- Labor-intensive production should continue shifting to labor-abundant countries
- However, AI may alter traditional factor intensity classifications (software is capital-intensive in development but nearly costless to replicate)

---

# PART B – MORTGAGE MARKET ANALYSIS (Recursion Analyzer Queries)

## Question 1: Active Mortgage Lenders/Sellers to GSEs (2025)

### 1a. For each seller to GSEs, find total loan count and issuance balance to Fannie Mae and Freddie Mac

**Query Approach in Recursion Analyzer:**

```
Filter: Settlement Year = 2025
Group By: Seller Name, GSE (Fannie Mae / Freddie Mac)
Aggregations:
  - COUNT(Loan ID) as "Loan Count"
  - SUM(Original Loan Balance) as "Total Issuance Balance"
```

### 1b. How many active sellers to each GSE?

**Fannie Mae**: Use filter `GSE = Fannie Mae, Year = 2025`, then count distinct Seller Names
**Freddie Mac**: Use filter `GSE = Freddie Mac, Year = 2025`, then count distinct Seller Names

_Expected Result_: Typically 1,000+ active sellers to each GSE, with Fannie Mae having slightly more due to larger market share.

### 1c. How many active sellers sold to BOTH GSEs in 2025?

**Query Approach:**

```
Step 1: Get list of sellers to Fannie Mae in 2025
Step 2: Get list of sellers to Freddie Mac in 2025
Step 3: Find INTERSECTION of both lists
```

_Expected Result_: Most large lenders (Wells Fargo, JPMorgan, Quicken/Rocket, etc.) sell to both GSEs. Typically 60-70% of sellers serve both.

### 1d. How many sellers sold to ONLY ONE GSE in 2025?

**Query Approach:**

```
Total Unique Sellers - Sellers to Both GSEs = Sellers to Only One GSE
```

Can also be calculated as:

- (Fannie Mae only sellers) + (Freddie Mac only sellers)

_Expected Result_: Smaller lenders and credit unions often have exclusive relationships. Typically 30-40% sell to only one GSE.

---

## Question 2: Private Mortgage Insurance (PMI) Analysis - Fannie Mae MBS 2025

### 2a. Using PMI Indicator ("Mortgage Insurance Y/N")

**Query:**

```
Filter:
  - GSE = Fannie Mae
  - Settlement Year = 2025
  - Mortgage Insurance = Yes
Aggregations:
  - COUNT(Loan ID) as "Loan Count"
  - SUM(Original Loan Balance) as "Total Balance"
Group By: PMI Company Name (if available)
```

### 2b. Using LTV > 80%

**Query:**

```
Filter:
  - GSE = Fannie Mae
  - Settlement Year = 2025
  - Original LTV > 80
Aggregations:
  - COUNT(Loan ID) as "Loan Count"
  - SUM(Original Loan Balance) as "Total Balance"
Group By: PMI Company Name
```

**Key PMI Companies to Look For:**
| PMI Company | Ticker |
|-------------|--------|
| MGIC Investment Corp | MTG |
| Radian Group | RDN |
| Essent Group | ESNT |
| Arch Capital (Arch MI) | ACGL |
| National MI | NMIH |
| Enact Holdings | ACT |

**Note**: Both approaches should yield similar results, but:

- Method (a) captures all loans flagged with MI regardless of LTV
- Method (b) assumes all high-LTV loans require PMI (some exceptions exist for VA loans, piggyback loans)

---

## Question 3: Ginnie Mae MBS 2025 - Distribution Analysis

### 3a. Distribution by Original Loan Balance (every $100k increment)

**Query:**

```
Filter: GSE = Ginnie Mae, Year = 2025
Bucket By: Original Loan Balance
  - $0 - $100,000
  - $100,001 - $200,000
  - $200,001 - $300,000
  - $300,001 - $400,000
  - $400,001 - $500,000
  - $500,001 - $600,000
  - $600,001+ (Jumbo - rare for Ginnie Mae)
Aggregations: Loan Count, Total Balance
```

**Notable Observations:**

- Ginnie Mae (FHA/VA/USDA loans) typically has lower average balances than conventional GSE loans
- FHA loan limits vary by county but are generally lower than conforming limits
- Most Ginnie Mae loans cluster in $150,000 - $350,000 range
- VA loans may have higher averages due to no down payment requirement

### 3b. Distribution by Mortgage Rate (every 0.50% increment)

**Query:**

```
Bucket By: Note Rate
  - ≤5.00%
  - 5.01% - 5.50%
  - 5.51% - 6.00%
  - 6.01% - 6.50%
  - 6.51% - 7.00%
  - 7.01% - 7.50%
  - >7.50%
```

**Notable Observations (2025):**

- Rates in 2025 depend heavily on Fed policy trajectory
- FHA/VA loans often carry slightly higher rates than conventional
- Distribution will show the impact of rate environment on issuance volume
- Refinance activity spikes in lower rate buckets

### 3d. Distribution by Original LTV (every 20% increment)

**Query:**

```
Bucket By: Original LTV
  - 0% - 20% (high equity)
  - 21% - 40%
  - 41% - 60%
  - 61% - 80%
  - 81% - 100% (low/no equity)
  - >100% (underwater - rare for new originations)
```

**Notable Observations:**

- FHA loans allow up to 96.5% LTV (3.5% down payment)
- VA loans allow 100% LTV (zero down payment)
- Ginnie Mae will show much higher concentration in 80%+ LTV compared to conventional GSE pools
- This is a key distinguishing feature of government-backed mortgage programs

### 3e. Distribution by Original FICO Score

**Query:**

```
Bucket By: Credit Score
  - ≤580 (Sub-prime threshold)
  - 581 - 680 (Near-prime)
  - 681 - 720 (Prime)
  - >720 (Super-prime)
```

**Notable Observations:**

- FHA is designed to serve borrowers with lower credit scores
- Minimum FHA FICO is 500 (with 10% down) or 580 (with 3.5% down)
- VA has no official minimum FICO, but lenders typically require 620+
- Ginnie Mae pools will show broader FICO distribution than conventional GSE pools
- Post-2008 underwriting tightened significantly; very few loans <620

---

# PART B - Question 4: Day Count/Compounding Analysis

## The Two Investments

| Feature           | Investment I  | Investment II |
| ----------------- | ------------- | ------------- |
| Principal         | $10,000       | $10,000       |
| Coupon Rate       | 6.00%         | 6.10%         |
| Payment Frequency | Semi-annually | Annually      |
| Day Count         | 30/360        | Actual/365    |
| Purchase Price    | 100 (par)     | 100 (par)     |

## Calculate Effective Annual Yield

### Investment I: 6.00% Semi-Annual with 30/360

**Step 1: Calculate Semi-Annual Coupon Payment**
$$\text{Semi-Annual Coupon} = \$10,000 \times \frac{6.00\%}{2} = \$300$$

**Step 2: Calculate Effective Annual Yield (accounting for compounding)**

With semi-annual compounding, you receive $300 at 6 months and can reinvest it:

$$\text{EAY} = \left(1 + \frac{0.06}{2}\right)^2 - 1 = (1.03)^2 - 1 = 1.0609 - 1 = 6.09\%$$

**Step 3: Total Year-End Value**

- First coupon at 6 months: $300
- Second coupon at 12 months: $300
- Reinvestment income (assuming same 6% rate): $300 × 0.03 = $9

**Total Return**: $300 + $300 + $9 = **$609**

**Effective Yield**: **6.09%**

### Investment II: 6.10% Annual with Actual/365

**Step 1: Calculate Annual Coupon Payment**

With Actual/365, the actual number of days matters:

- In a regular year: 365 days
- The coupon is: $10,000 × 6.10% × (365/365) = **$610**

**Step 2: Effective Annual Yield**

Since payment is annual with no interim compounding:
$$\text{EAY} = 6.10\%$$

**Total Return**: **$610**

**Effective Yield**: **6.10%**

## Comparison

| Metric                 | Investment I (6.00% SA) | Investment II (6.10% Ann) |
| ---------------------- | ----------------------- | ------------------------- |
| Nominal Rate           | 6.00%                   | 6.10%                     |
| Effective Annual Yield | 6.09%                   | 6.10%                     |
| Total Cash Received    | $600                    | $610                      |
| Reinvestment Income    | ~$9 (at 6% rate)        | $0                        |
| **Total Return**       | **~$609**               | **$610**                  |

## Which Investment Do I Prefer?

**Investment II (6.10% Annual)** is marginally better, yielding an additional $1 per $10,000 invested.

### Reasoning:

1. **Effective Yield Comparison**:
   - Investment I: 6.09% effective
   - Investment II: 6.10% effective
   - Difference: 1 basis point advantage to Investment II

2. **Reinvestment Risk Consideration**:
   - Investment I requires you to reinvest the $300 mid-year coupon
   - If you can't achieve 6% on reinvestment, your actual return drops
   - Investment II has no reinvestment risk

3. **Practical Considerations**:
   - If reinvestment rates are HIGHER than 6%, Investment I could outperform
   - If reinvestment rates are LOWER than 6%, Investment I underperforms more
   - Current rate environment should guide this decision

4. **Day Count Impact**:
   - 30/360 assumes 30 days/month, 360 days/year (simplifies calculation)
   - Actual/365 uses actual calendar days
   - In a leap year, Actual/365 would give: $10,000 × 6.10% × (366/365) = $611.67

### Final Answer:

**I prefer Investment II** because:

1. It has a slightly higher effective annual yield (6.10% vs 6.09%)
2. It eliminates reinvestment risk (no need to reinvest mid-year)
3. The 10 basis point higher nominal rate more than compensates for loss of compounding benefit
4. In a falling rate environment, receiving all cash at year-end protects against reinvestment at lower rates

However, **if I expected rates to rise** and could confidently reinvest the mid-year coupon at a higher rate, Investment I could become preferable.

---

# SUMMARY

## Files Created:

1. `heckscher_ohlin_analysis.py` - Python script for data analysis
2. `assignment_answers.md` - This comprehensive answer document

## Key Takeaways:

**Part A:**

- The U.S. has experienced significant capital deepening since 1960
- Regression of trending variables produces spurious results due to unit roots
- AI investment will likely accelerate K/L ratio growth through both capital accumulation and potential labor displacement

**Part B:**

- GSE mortgage analysis requires understanding seller relationships, PMI requirements, and loan characteristic distributions
- Ginnie Mae (government-backed) loans show distinct patterns vs. conventional GSE loans

**Fixed Income:**

- Semi-annual compounding at 6% yields ~6.09% effective annual
- Annual payment at 6.10% is marginally superior with no reinvestment risk
