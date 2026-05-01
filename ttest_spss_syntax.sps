* NOTE: If your variable names are too long in SPSS, use Variable View to rename them, then adapt this syntax.

* Independent-samples t-test by Gender (Male vs Female).

* Make sure Gender is coded as strings 'Male'/'Female' or recode to 0/1.

T-TEST GROUPS=Gender('Male' 'Female') /VARIABLES=RSES_total /MISSING=ANALYSIS.

T-TEST GROUPS=Gender('Male' 'Female') /VARIABLES=Attachment_mean /MISSING=ANALYSIS.

T-TEST GROUPS=Gender('Male' 'Female') /VARIABLES=Relationship_approx_mean /MISSING=ANALYSIS.

* ---------------------------------------------.
* Correlations for objectives (relationships).
* ---------------------------------------------.
CORRELATIONS
 /VARIABLES=RSES_total Attachment_mean Relationship_approx_mean
 /PRINT=TWOTAIL SIG
 /MISSING=PAIRWISE.

* Spearman (non-parametric rank correlations).
NONPAR CORR
 /VARIABLES=RSES_total Attachment_mean Relationship_approx_mean
 /PRINT=SPEARMAN TWOTAIL
 /MISSING=PAIRWISE.
