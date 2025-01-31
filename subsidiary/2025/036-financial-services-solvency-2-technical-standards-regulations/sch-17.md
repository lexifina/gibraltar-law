SCHEDULE 17 METHOD-SPECIFIC DATA REQUIREMENTS AND METHOD SPECIFICATIONS FOR UNDERTAKINGSPECIFIC PARAMETERS OF THE STANDARD FORMULA

Article 220

PART 1 GENERAL PROVISIONS

Interpretation.

1.(1)  In this Schedule–

“accident year” means, with respect to a payment for an insurance or reinsurance claim, the year in which the insured event that gave rise to that claim took place;

“adjustment factor for non-proportional reinsurance (non-life)” means the adjustment factor for non-proportional reinsurance referred to in Article 117(3) and (4);

“adjustment factor for non-proportional reinsurance (NSLT health)” means the adjustment factor for non-proportional reinsurance referred to in Article 148(3);

“aggregated losses” for the purposes of Part 2, means the payments made and the best estimates of the provision for insurance and reinsurance claims outstanding in segment s after the first development year of the accident year of those claims;

“credibility factor” means the applicable credibility factor determined in accordance with Part 6;

“cumulative claims amounts” means the cumulative payment amounts for insurance and reinsurance claims in segment s;

“development year” means, with respect to a payment for an insurance or reinsurance claim, the difference between the year of that payment and the accident year of that payment;

“financial year” means, with respect to a payment for an insurance or reinsurance claim, the year in which this payment took place;

“increase in the amount of annuity benefits (health)” means the increase in the amount of annuity benefits referred to in Article 158;

“increase in the amount of annuity benefits (life)” means the increase in the amount of annuity benefits referred to in Article 141;

“non-proportional reinsurance method 1” means the method set out in Chapter 1 of Part 5;

“non-proportional reinsurance method 2” means the method set out in Chapter 2 of Part 5;

“premium risk method” means the method set out in Part 2;

“recognisable excess of loss reinsurance contract” means the recognisable excess of loss reinsurance contract provided for in paragraph 11(2);

“recognisable stop loss reinsurance contract” means the recognisable stop loss reinsurance contract provided for in paragraph 14(2);

“reporting year” means, with respect to a payment for an insurance or reinsurance claim, the year in which the insured event that gave rise to that claim was notified to the insurance or reinsurance undertaking;

“reserve risk method 1” means the method set out in Chapter 1 of Part 3;

“reserve risk method 2” means the method set out in Chapter 2 of Part 3;

“revision risk method” means the method set out in Part 4;

“segment s” denotes the segment for which the undertaking specific parameter is determined, a segment set out in Schedule 2 or a segment set out in Article 147A, as specified in the undertaking’s USP approval;

“standard deviation for non-life gross premium risk” means the standard deviation for non- life gross premium risk referred to in Article 117(3);

“standard deviation for non-life premium risk” means the standard deviation for non-life premium risk referred to in Article 117(2)(a);

“standard deviation for non-life reserve risk” means the standard deviation for non-life reserve risk referred to in Article 117(2)(b);

“standard deviation for NSLT health gross premium risk” means the standard deviation for NSLT health gross premium risk referred to in Article 148(3);

“standard deviation for NSLT health premium risk” means the standard deviation for NSLT health premium risk referred to in Article 148(2)(a);

“standard deviation for NSLT health reserve risk” means the standard deviation for NSLT health reserve risk referred to in Article 148(2)(b); and

“USP undertaking” means an insurance undertaking or reinsurance undertaking which has approval to apply an undertaking specific parameter (“USP approval”) given by the GFSC in accordance with regulation 276A of the Insurance Companies Regulations.

(2)  [Not used]

PART 2 PREMIUM RISK METHOD

Input data and USP method-specific data requirements.

2.(1)  A USP undertaking using the premium risk method to calculate an undertaking specific parameter must ensure that the data for estimating the standard deviation of segment s only consist of the following–

(a) aggregated losses; and

(b) the earned premiums in segment s.

(2)  The aggregated losses and earned premiums referred to in sub-paragraph (1) must be available separately for each accident year of the insurance and reinsurance claims in segment s.

(3)  A USP undertaking using the premium risk method must ensure that the data used to calculate an undertaking specific parameter satisfy all the following USP method-specific data requirements–

(a) the data are representative of the premium risk that the insurance or reinsurance undertaking is exposed to during the following 12 months;

(b) data are available for at least five consecutive accident years;

(c) where the premium risk method is applied to replace the standard parameters for either the standard deviation for non-life gross premium risk or the standard deviation for NSLT health gross premium risk, the aggregated losses and earned premiums are not adjusted for recoverables from reinsurance contracts and special purpose vehicles or premiums from reinsurance contracts;

(d) where the premium risk method is applied to replace the standard parameters for either the standard deviation for non-life premium risk or the standard deviation for NSLT health premium risk–

(i) the aggregated losses are adjusted for amounts recoverable from reinsurance contracts and special purpose vehicles which are consistent with the reinsurance contracts and special purpose vehicles that are in place to provide cover for the following 12 months; and

(ii) the earned premiums are adjusted for premiums from reinsurance contracts which are consistent with the reinsurance contracts and special purpose vehicles that are in place to provide cover for the following 12 months;

(e) the aggregated losses are adjusted for catastrophe claims to the extent that the risk of those claims is reflected in the non-life catastrophe risk sub-module referred to in Article 119 or the health catastrophe risk sub-module referred to in Article 160;

(f) the aggregated losses include the expenses incurred in servicing the insurance and reinsurance obligations; and

(g) the data are consistent with the following assumptions–

(i) expected aggregated losses in a particular segment and accident year are linearly proportional in earned premiums in a particular accident year;

(ii) the variance of aggregated losses in a particular segment and accident year is quadratic in earned premiums in a particular accident year;

(iii) aggregated losses follow a lognormal distribution; and

(iv) maximum likelihood estimation is appropriate.

USP method specification.

3.(1)  For the purposes of sub-paragraphs (2) to (5), the following notations apply–

(a) accident years are denoted by consecutive numbers starting with 1 for the first accident year for which data are available;

(b) T denotes the latest accident year for which data are available;

(c) for all accident years, the aggregated losses in segment s in a particular accident year t are denoted by yt; and

(d) for all accident years, the earned premiums in segment s in a particular accident year t are denoted by xt.

(2)  A USP undertaking using the premium risk method must calculate the standard deviation of segment s in accordance with the following formula–

where–

(a) c denotes the credibility factor;

(b) denotes the standard deviation function set out in sub-paragraph (3);

(c) denotes the mixing parameter set out in sub-paragraph (4);

(d) denotes the logarithmic variation coefficient set out in sub-paragraph (4); and

(e) σ(prem,s) denotes the standard parameter that is replaced by the undertaking’s undertaking-specific parameter in respect of segment s.

(3)  The standard deviation function must be equal to the following function of two variables– where–

(a) and  are defined in sub-paragraph (2)(c) and (d), respectively;

(b) exp denotes the exponential function;

(c) ln denotes the natural logarithm function; and

(d) πt denotes the following function of two variables–

where–

(i) and are defined in sub-paragraph (2)(c) and (d), respectively; and;

(ii) denotes the following amount–

(4)  The mixing parameter and the logarithmic variation coefficient must be the values and respectively for which the following amount becomes minimal–

where–

(a) ln denotes the natural logarithm function;

(b) πt denotes the function set out in sub-paragraph (3)(d);

(c) denotes the standard deviation function set out in sub-paragraph (3); and

(d) denotes the following amount–

(5)  For the purposes of sub-paragraph (4), a USP undertaking must ensure that no values for the mixing parameter less than zero or exceeding 1 are considered for the determination of the minimal amount.

PART 3 RESERVE RISK

Chapter 1 Method 1

Input data and USP method-specific data requirements.

4.(1)  A USP undertaking using reserve risk method 1 to calculate an undertaking specific parameter must ensure that the data for estimating the standard deviation of segment s consist of the following–

(a) the sum of the best estimate provision at the end of the financial year for claims that were outstanding in segment s at the beginning of the financial year and the payments made during the financial year for claims that were outstanding in segment s at the beginning of the financial year; and

(b) the best estimate of the provision for claims outstanding in segment s at the beginning of the financial year.

(2)  The amounts referred to in sub-paragraphs (1)(a) and (b) must be available separately for different financial years.

(3)  A USP undertaking using reserve risk method 1 must ensure that the data used to calculate an undertaking specific parameter satisfy all the following USP method-specific data requirements–

(a) the data are representative of the reserve risk that the insurance or reinsurance undertaking is exposed to during the following 12 months

(b) data are available for at least five consecutive financial years;

(c) the data are adjusted for amounts recoverable from reinsurance contracts and special purpose vehicles which are consistent with the reinsurance contracts and special purpose vehicles that are in place to provide cover for the following 12 months;

(d) the data includes the expenses incurred in servicing the insurance and reinsurance obligations; and

(e) the data are consistent with the following assumptions–

(i) the amount referred to sub-paragraph (1)(a) in that particular segment and financial year is linearly proportional in the best estimate of the provision for claims outstanding in that particular segment and financial year;

(ii) the variance of the amount referred to sub-paragraph (1)(a) in a particular segment and financial year is quadratic in the provision for claims outstanding in a particular segment and financial year;

(iii) the amount referred to sub-paragraph (1)(a) follows a lognormal distribution; and

(iv) maximum likelihood estimation is appropriate.

USP Method specification.

5.(1)  For the purposes of sub-paragraphs (2) to (5), the following notations apply–

(a) the financial years are denoted by consecutive numbers starting with 1 for the first financial year for which data are available;

(b) T denotes the latest financial year for which data are available;

(c) for all financial years, the amount referred to paragraph 4(1)(a) in segment s in a particular financial year t is denoted by yt; and

(d) for all financial years, the best estimate of the provision for claims outstanding in segment s in a particular financial year t is denoted by xt.

(2)  A USP undertaking using reserve risk method 1 must calculate the standard deviation of segment s in accordance with the following formula–

(a) c denotes the credibility factor;

(b) denotes the standard deviation function set out in sub-paragraph (3);

(c) denotes the mixing parameter set out in sub-paragraph (4);

(d) denotes the logarithmic variation coefficient set out in sub-paragraph (4); and

(e) denotes the standard parameter that is replaced by the undertaking’s undertaking-specific parameter in respect of segment s.

(3)  The standard deviation function must be equal to the following function of two variables–

where–

(a) and are defined in sub-paragraph (2)(c) and (d), respectively;

(b) exp denotes the exponential function;

(c) ln denotes the natural logarithm function; and

(d) πt denotes the following function of two variables–

where–

(i) and are defined in sub-paragraph (2)(c) and (d), respectively;

(ii) denotes the following amount–

(4)  The mixing parameter and the logarithmic variation coefficient must be the values and respectively for which the following amount becomes minimal–

where–

(a) ln denotes the natural logarithm function;

(b) πt denotes the function set out in sub-paragraph (3)(d);

(c) denotes the standard deviation function set out in sub-paragraph (3); and

(d) denotes the following amount–

(5)  For the purposes of sub-paragraph (4), a USP undertaking must ensure that no values for the mixing parameter less than zero or exceeding 1 are considered for the determination of the minimal amount.

Chapter 2 Method 2

Input data and USP method-specific data requirements.

6.(1)  A USP undertaking using reserve risk method 2 to calculate an undertaking specific parameter must ensure that the data for estimating the standard deviation of segment s consist of cumulative claims amounts, separately for each accident year and development year of the payments.

(2)  A USP undertaking using reserve risk method 2 must ensure that the data used to calculate an undertaking specific parameter satisfy all the following USP method-specific data requirements–

(a) the data are representative of the reserve risk that the insurance or reinsurance undertaking is exposed to during the following 12 months;

(b) data are available for at least five consecutive accident years;

(c) in the first accident year, data are available for at least five consecutive development years;

(d) in the first accident year the cumulative claims amounts of the latest  development year for which data are available includes all the payments of the accident year except an immaterial amount;

(e) the number of consecutive accident years for which data are available is not less than the number of consecutive development years in the first accident year for which data are available;

(f) the cumulative claims amounts are adjusted for amounts recoverable from reinsurance contracts and special purpose vehicles which are consistent with the reinsurance contracts and special purpose vehicles that are in place to provide cover for the following 12 months;

(g) the cumulative claims amounts must include the expenses incurred in servicing the insurance or reinsurance obligations; and

(h) the data are consistent with the following assumptions about the stochastic nature of cumulative claims amounts–

(i) cumulative claims amounts for different accident years are mutually stochastically independent;

(ii) for all accident years the implied incremental claim amounts are stochastically independent;

(iii) for all accident years the expected value of the cumulative claims amount for a development year is proportional to the cumulative claims amount for the preceding development year; and

(iv) for all accident years the variance of the cumulative claims amount for a development year is proportional to the cumulative claims amount for the preceding development year.

(3)  For the purposes of sub-paragraph (2)(d), a payment must be considered material where ignoring it in the calculation of the undertaking-specific parameter could influence the decision-making or the judgement of the users of that information, including the GFSC.

USP Method specification.

7.(1)  For the purposes of sub-paragraphs (2) and (3), the following notations apply–

(a) the accident years are denoted by consecutive numbers starting with 0 for the first accident year for which data are available;

(b) I denotes the latest accident year for which data are available;

(c) J denotes the latest development year in the first accident year for which data are available; and

(d) C(i,j) denotes the cumulative claims for accident year i and development year j.

(2)  A USP undertaking using reserve risk method 2 must calculate the standard deviation for segment s in accordance with the following formula– where–

(a) c denotes the credibility factor;

(b) MSEP denotes the mean squared error of prediction as specified in sub-paragraph (3); (c) for all accident years and development years, denotes the cumulative claims estimate for the specific accident year i and development year j, being defined as follows–

where for all development years denotes for development factor estimate of the specific development year j, being defined as follows–

(d) σ(res,s) denotes the standard parameter that is replaced by the undertaking’s undertaking specific parameter in respect of segment s.

(3)  The mean squared error of prediction must be equal to the following–

where–

(a) for all accident years and development years, denotes the cumulative claim estimate in the specific accident year i and development year j, as set out in sub- paragraph (2)(c).

(b) for all development years, Sj denotes for a specific development year j the following amount–

(c) for all development years, S′j denotes for a specific development year j the following amount–

(d) for all development years, 123 denotes for a specific development year j the following amount–

where–

(i) 453 denotes the development factor estimate of development year j as set out in sub-paragraph (2)(c); and

(ii) 673 8denotes the following amount–

PART 4 REVISION RISK METHOD

General provisions.

8.(1)  A USP undertaking must only use the revision risk method for–

(a) the life revision risk sub-module referred to in Article 141; or

(b) the health revision risk sub-module referred to in Article 158, if the annuities within the scope of the relevant sub-module are not subject to material inflation risk.

(2)  For the purposes of sub-paragraph (1), an undertaking must treat inflation risk as material where ignoring it in the calculation of the sub-modules referred to in sub-paragraph (1)(a) and (b) could influence the decision-making or the judgment of the users of the information, including the GFSC.

Input data and USP method-specific data requirements.

9.(1)  A USP undertaking using the revision risk method to calculate an undertaking specific parameter must ensure that the data for estimating the increase in the amount of annuity benefits consist of annual amounts of annuity benefits of annuity insurance obligations where the benefits payable could increase as a result of changes in the legal environment or in the state of health of the person insured, separately for consecutive financial years and each beneficiary.

(2)  A USP undertaking using the revision risk method must ensure that the data used to calculate an undertaking specific parameter satisfy all the following USP method-specific data requirements–

(a) the data are representative of the revision risk that an insurance or reinsurance undertaking is exposed to during the following 12 months;

(b) data are available for at least five consecutive financial years;

(c) the annuity benefits are gross, without deduction of the amounts recoverable from reinsurance contracts and special purpose vehicles;

(d) the annuity benefits must include the expenses incurred in servicing the annuity obligations; and

(e) the data are consistent with the following assumptions about the stochastic nature of increases in the amount of annuity benefits–

(i) the annual number of increases in annuity benefits follows a negative binomial distribution, including in the tail of the distribution;

(ii) the amount of an increase in annuity benefits follows a lognormal distribution, including in the tail of the distribution; and

(iii) the annual number of increases in annuity benefits and the amounts of the increases in annuity are mutually stochastically independent.

USP Method specification.

10.(1)  For the purposes of sub-paragraphs (2) to (6), the following notations apply–

(a) the financial years are denoted by consecutive numbers starting with 1 for the first financial year for which data are available;

(b) T denotes the latest financial year for which data are available;

(c) A(i,t) denotes the annuity benefits of beneficiary i in financial year t; and

(d) D(i,t) denotes the change of annuity benefits after financial year t, being equal to the following difference–

(2)  A USP undertaking using the revision risk method must calculate the increase in the amount of annuity benefits in accordance with the following formula–

where–

(a) c denotes the credibility factor;

(b) denotes the expected value of increases in annuity benefits set out in sub- paragraph (3);

(c) VaR0,995(R) denotes the 99.5% quantile of the distribution of increases in annuity benefits set out in sub-paragraph (4);

(d) S is–

(i) equal to 3% where the calculation relates to the life revision risk sub- module referred to in Article 141; and

(ii) equal to 4% where the calculation relates to the health revision risk sub- module referred to in Article 158.

(3)  The expected value of increases in annuity benefits must be equal to the following–

where–

(a) 9: denotes the estimated average change in annuity benefits, restricted to those changes in  annuity benefits that are larger than zero; and

(b) ;< denotes the estimated average number, per financial year, of changes in annuity benefits that are larger than zero.

(4)  The increases in annuity benefits must be equal to the following–

where–

(a) N denotes the annual number of increases in annuity benefits and follows a negative binominal distribution with an expected value that is equal to the estimated number of changes in annuity benefits set out in sub-paragraph (3)(b) and with a standard deviation that is equal to the estimated standard deviation of the number of changes in annuity benefits set out in sub-paragraph (5);

(b) Xk denotes the amount of an increase in annuity benefits and follows a lognormal distribution with an expected value that is equal to the estimated average change in annuity benefits set out in paragraph (3)(a) and with a standard deviation that is equal to the estimated standard deviation of changes in annuity benefits set out in sub-paragraph (6); and

(c) the annual number of increases in annuity benefits and the amounts of the increase in annuity benefits are mutually stochastically independent.

(5)  The estimated standard deviation of the number of changes in annuity benefits must be equal to the following–

where–

(a) Nt denotes the number of changes in annuity benefits in financial years t that are larger than zero; and

(b) ;< denotes the estimated average change in annuity benefits set out in sub- paragraph (3)(b).

(6)  The estimated standard deviation of changes in annuity benefits must be equal to the following–

where–

(a) the sum includes only those beneficiaries i and financial years t for which D(i,t) is larger than zero;

(b) n denotes the number of summands of the sum referred to in paragraph (a); and

(c)  9: denotes the estimated average change in annuity benefits set out in sub- paragraph (3)(a).

PART 5 NON-PROPORTIONAL REINSURANCE METHODS

Chapter 1 Method 1

General Provisions.

11.(1)  A USP undertaking must only use non-proportional reinsurance method 1 if there is a recognisable excess of loss reinsurance contract in place.

(2)  A “recognisable excess of loss reinsurance contract”–

(a)  means an excess of loss reinsurance contract which–

(i) provides for complete compensation up to a specified limit or without limit for losses of the cedant that relate either to single insurance claims, or to all insurance claims under the same contract of insurance during a specified time period, and that are larger than a specified retention;

(ii) covers all insurance claims that the undertaking may incur in the segment or homogenous risk groups within the segment during the following 12 months;

(iii) allows for a sufficient number of reinstatements so as to ensure that all claims of multiple events incurred during the following months are covered; and

(iv) complies with Articles 209, 210, 211 and 213; and

(b) includes–

(i) arrangements with special purpose vehicles that provide risk transfer which is equivalent to that referred to in sub-paragraphs (i) to (iv); and

(ii) a combination of reinsurance contracts (which may be considered as one recognisable excess of loss reinsurance contract) where an undertaking has concluded several excess of loss reinsurance contracts that–

(aa) individually meet the requirement set out in sub-paragraph (iv); and

(bb) in combination meet the requirements set out in sub-paragraphs (i) to (iii).

Input data and method-specific data requirements.

12.(1)  A USP undertaking using non-proportional reinsurance method 1 to calculate an undertaking specific parameter must ensure that the data for estimating an adjustment factor for non-proportional reinsurance consist of the ultimate claim amounts of insurance and reinsurance claims that were reported to the insurance or reinsurance undertaking in segment s during the last financial years, separately for each insurance and reinsurance claim.

(2)  A USP undertaking using non-proportional reinsurance method 1 must ensure that the data used to calculate an undertaking specific parameter satisfy all of the following USP method-specific data requirements–

(a) the data are representative of the premium risk that the insurance or reinsurance undertaking is exposed to during the following 12 months;

(b) the data do not indicate a higher premium risk than reflected in the standard deviation for premium risk used to calculate the Solvency Capital Requirement using the standard formula;

(c) the ultimate claim amounts are estimated in the year the insurance and reinsurance claims were reported;

(d) data are available for at least five reporting years;

(e) where the recognisable excess of loss reinsurance contract applies to gross claims, the ultimate claim amounts are gross;

(f) where the recognisable excess of loss reinsurance contract applies to claims after deduction of the recoverables from certain other reinsurance contracts and special purpose vehicles, the amounts receivable from those reinsurance contracts and special purpose vehicles are deducted from the ultimate claim amounts;

(g) the ultimate claim amounts must not include expenses incurred in servicing the insurance and reinsurance obligations; and

(h) the data are consistent with the assumption that ultimate claim amounts follow a lognormal distribution, including in the tail of the distribution.

USP method specification.

13.(1)  For the purpose of sub-paragraphs (2) to (5), the following notations apply–

(a) insurance and reinsurance claims for which data are available are denoted by consecutive numbers starting with 1;

(b) n denotes the number of insurance and reinsurance claims for which data are available;

(c) Yi denotes the ultimate claim amount of the insurance and reinsurance claims i;

(d) μ and ω denote the first and second moment, respectively, of the claim amount distribution, being equal to the following amounts–

(e) b1 denotes the amount of the retention of the recognisable excess of loss reinsurance contract;

(f) where the recognisable excess of loss reinsurance contract provides compensation only up to a specified limit, b2 denotes the amount of that limit.

(2)  A USP undertaking using non-proportional reinsurance method 1 must calculate the adjustment factor for non-proportional reinsurance in accordance with the following formula– where–

(a) c denotes the credibility factor;

(b) NP′ denotes the estimated adjustment factor for non-proportional reinsurance set out in sub-paragraph (3); and

(c) NP denotes the standard parameter that is replaced by the insurance or reinsurance undertaking’s undertaking specific parameter.

(3)  The estimated adjustment factor for non-proportional reinsurance must be equal to the following–

where sub-paragraph (1)(f) applies,

otherwise.

where the parameters μ2, ω1 and ω2 are set out in sub-paragraph (4).

(4)  The parameters, μ2, ω1 and ω2 must be equal to the following, respectively–

where–

(a) N denotes the cumulative distribution function of the normal distribution;

(b) ln denotes the natural logarithm function; and

(c) the parameters θ and η are equal to the following, respectively–

(5)  Despite sub-paragraph (3), where non-proportional reinsurance covers homogeneous risk groups within a segment, the estimated adjustment factor for non-proportional reinsurance must be equal to the following–

where–

(a) V(prem,h) denotes the volume measure for premium risk of the homogeneous risk group h determined in accordance with Article 116(3); and

(b) NP′(h) denotes the estimated adjustment factor for non-proportional reinsurance of homogeneous risk group h determined in accordance with sub-paragraph (3).

Chapter 2 Method 2

General provisions.

14.(1)  A USP undertaking must only use non-proportional reinsurance method 2 if there is a recognisable stop loss reinsurance contract in place.

(2)  A “recognisable stop loss reinsurance contract”–

(a) means a stop loss reinsurance contract which–

(i) provides for complete compensation up to a specified limit or without limit for aggregated losses of the cedant that relate to all insurance claims in the segment or homogeneous risk groups within the segment during a specified time period and that are larger than a specified retention; and

(ii) covers all insurance claims that the undertaking may incur in the segment or homogenous risk groups within the segment during the following 12 months;

(iii) allows for a sufficient number of reinstatements so as to ensure that all claims of multiple events incurred during the following months are covered; and

(iv) complies with Articles 209, 210, 211 and 213; and

(b) includes–

(i) arrangements with special purpose vehicles that provide risk transfer which is equivalent to that referred to in sub-paragraphs (i) to (iv); and

(ii) a combination of reinsurance contracts (which may be considered as one recognisable stop loss reinsurance contract) where an undertaking has concluded several stop loss reinsurance contracts that–

(aa) individually meet the requirement set out in sub-paragraph (iv); and

(bb) in combination meet the requirements set out in sub-paragraphs (i) to (iii).

Input data and USP method-specific data requirements.

15.(1)  A USP undertaking using the non-proportional reinsurance method 2 to calculate an undertaking specific parameter must ensure that data for estimating an adjustment factor for non-proportional reinsurance consist of the aggregated annual losses of insurance and reinsurance claims that were reported to the insurance or reinsurance undertaking in segment s during the preceding financial years.

(2)  A USP undertaking using the non-proportional reinsurance method 2 must ensure that the data used to calculate an undertaking specific parameter satisfy all the following USP method-specific data requirements––

(a) the data are representative of the premium risk that the insurance or reinsurance undertaking is exposed to during the following 12 months;

(b) the data do not indicate a higher premium risk than reflected in the corresponding standard deviation for premium risk used to calculate the Solvency Capital Requirement using the standard formula;

(c) the aggregated annual losses are estimated in the year insurance and reinsurance claims were reported;

(d) data are available for at least 5 reporting years;

(e) where the recognisable stop loss reinsurance contract applies to gross claims, the aggregated annual losses are gross;

(f) where the recognisable stop loss reinsurance contract applies to claims after deduction of the recoverables from certain other reinsurance contracts and special purpose vehicles, the amounts receivable from those reinsurance contracts and special purpose vehicles are deducted from the aggregated annual losses;

(g) the aggregated annual losses must not include expenses incurred in servicing the insurance and reinsurance obligations; and

(h) the data are consistent with the assumption that aggregated annual losses follow a lognormal distribution, including in the tail of the distribution.

USP method specification.

16.(1)  For the purposes of sub-paragraphs (2) to (5), the following notations apply–

(a) n denotes the number of financial years for which aggregated annual losses data are available;

(b) Yi denotes the aggregated losses in financial year i;

(c) μ and ω denote the first and second moment, respectively, of the aggregated annual losses distribution, being equal to the following amounts–

(d) b1 denotes the amount of the retention of the recognisable stop loss reinsurance contract; and

(e) where the recognisable stop loss reinsurance contract provides compensation only up to a specified limit, b2 denotes the amount of that limit.

(2)  A USP undertaking using the non-proportional reinsurance method 2 must calculate the adjustment factor for non-proportional reinsurance in accordance with the following formula–

where–

(a) c denotes the credibility factor;

(b) NP′ denotes the estimated adjustment factor for non-proportional reinsurance set out in sub-paragraph (3); and

(c) NP denotes the standard parameter that is replaced by the insurance or reinsurance undertaking’s undertaking specific parameter.

(3)  The estimated adjustment factor for non-proportional reinsurance must be equal to the following–

where sub- paragraph (1)(e) applies

otherwise.

where the parameters μ1 , μ2 , ω1 and ω2 are set out in sub-paragraph (4).

(4)  The parameters μ 1 , μ 2 , ω 1 and ω 2 must be equal to the following, respectively– where–

(a) N denotes the cumulative distribution function of the normal distribution;

(b) ln denotes the natural logarithm function; and

(c) the parameters θ and η are equal to the following, respectively–

(5)  Despite sub-paragraph (3), where non-proportional reinsurance covers homogeneous risk groups within a segment, the estimated adjustment factor for non-proportional reinsurance must be equal to the following– where–

(a) V(prem,h) denotes the volume measure for premium risk of the homogeneous risk group h determined in accordance with Article 116(3); and

(b) NP′(h) denotes the estimated adjustment factor for non-proportional reinsurance of homogeneous risk group h determined in accordance with sub-paragraph (3).

PART 6 CREDIBILITY FACTOR

17.(1)  The credibility factor for segments 1, 5 and 6 set out in Schedule 2 must be equal to the following–

Time lengths in years Credibility factor c 5 34% 6 43% 7 51% 8 59% 9 67% 10 74% 11 81% 12 87% 13 92% 14 96% 15 and larger 100%

(2)  The credibility factor for–

(a) segments 2 to 4 and 7 to 12 set out in Schedule 2;

(b) the segments set out in Article 147A; and

(c) the revision risk method,

must be equal to the following–

Time lengths in years Credibility factor c 5 34% 6 51% 7 67% 8 81% 9 92% 10 and larger 100%

(3)  For the purposes of sub-paragraphs (1) and (2), the time length must be equal to the following–

(a) for the premium risk method, the number of accident years for which data are available;

(b) for reserve risk method 1, the number of financial years for which data are available;

(c) for reserve risk method 2, the number of accident years for which data are available;

(d) for the revision risk method, the number of financial years for which data are available; and

(e) for non-proportional reinsurance method 1 and non-proportional reinsurance method 2, the number of reporting years for which data are available.
