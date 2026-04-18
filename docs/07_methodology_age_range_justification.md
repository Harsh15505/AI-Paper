# 07 - Methodology Note: Age Range Justification

## Inclusion and Exclusion Criteria

- Include: pediatric inpatients age 2-12 years
- Exclude: age <2 years
- Exclude: age >=13 years
- Study period: February 2025 to January 2026
- Setting: [Hospital Name], Paldi, Ahmedabad

## Why 2-12 Years

- Excluding <2 years reduces confounding from infant-specific respiratory syndromes (especially bronchiolitis patterns).
- Excluding >=13 years avoids puberty-related physiological heterogeneity and different care-seeking/admission behavior.
- Age 2-12 gives a more homogeneous pre-pubertal group while preserving sample size for stable modeling.

## How Age Is Controlled in Analysis

- Include age in years as a continuous covariate in all models.
- Use age-group sensitivity analysis:
  - Toddler: 2-4
  - Young Child: 5-7
  - Older Child: 8-12

## Reviewer-Ready Responses (Short Form)

### Why not only 5-12 for homogeneity?

- 2-12 improves statistical power and generalizability while still controlling age explicitly in models.

### How is heterogeneity between younger and older children handled?

- Continuous age adjustment plus age-group sensitivity analyses.

### Why exclude adolescents if sample size matters?

- Added heterogeneity from puberty and different healthcare utilization outweighs marginal sample-size gain.

## Suggested Limitations Text

The 2-12 age span may introduce developmental heterogeneity in susceptibility and healthcare-seeking behavior. Although age is modeled explicitly, residual age-related confounding may remain.

## Suggested Sample-Size Justification Text

Institutional admission patterns suggest approximately 250 respiratory and 800-1000 non-respiratory admissions in the 2-12 age group over the study window, which is adequate for multivariable predictive modeling.

## Ethics/Protocol Language (Short)

Age range 2-12 was selected to balance validity and sample-size adequacy while reducing heterogeneity from infant and adolescent physiology. Age is modeled continuously to account for developmental differences.

## Submission Checklist

- [ ] Age range 2-12 stated in abstract and methods
- [ ] Exclusion criteria (<2, >=13) explicitly stated
- [ ] Age variable included in all model specifications
- [ ] Age-group sensitivity plan documented
- [ ] Age heterogeneity listed as limitation
- [ ] Ethics/protocol text aligned with final scope
