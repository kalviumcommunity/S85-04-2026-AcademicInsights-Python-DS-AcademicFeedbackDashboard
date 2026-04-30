## 📊 1. Project Insights
By translating raw survey data into a visual dashboard, the following key patterns emerged:
* **Overall Sentiment is Measurable:** The satisfaction histogram revealed the baseline health of the student body, allowing us to track general sentiment shifts over time rather than relying on anecdotal complaints.
* **Departmental Outliers Drive Action:** The boxplot analysis demonstrated that average scores hide extreme realities. We identified specific outlier courses within departments (dots outside the IQR) that require immediate administrative review.
* **Difficulty ≠ Dissatisfaction:** The correlation scatter plot showed that high course difficulty does not automatically guarantee low student satisfaction, suggesting that students value rigorous courses provided the teaching quality remains high.

## 🧠 2. Documenting Assumptions
To proceed with the analysis, the following structural assumptions were made:
* **Missing Data Logic:** We assumed that a missing value in the `Comments_Length` column meant the student intentionally skipped the text box, justifying the decision to impute these null values with zero rather than dropping the row entirely.
* **Metric Linearity:** We assumed the 1-to-5 rating scale provided equidistant psychological intervals for the students (e.g., the jump from 3 to 4 means the same as 4 to 5).
* **Data Relevance:** We assumed the dataset accurately reflects the current academic environment and that historical curriculum changes have not rendered the older survey rows obsolete.

## ⚠️ 3. Acknowledging Limitations
While this dashboard provides actionable direction, it is constrained by the following limitations:
* **Voluntary Response Bias:** Survey data inherently suffers from response bias. Usually, only students with extremely positive or extremely negative experiences submit feedback, leaving the "silent majority" unrepresented in the data.
* **Lack of Contextual Features:** The dataset lacks demographic and academic history context. A student failing the prerequisite might rate a course as overly difficult, skewing the data against the professor unfairly.
* **Subjective Metrics:** "Teaching Quality" is an entirely subjective metric defined by the student, not a standardized evaluation of the professor's actual pedagogical effectiveness.