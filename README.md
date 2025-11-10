# Flight Data Analysis - Data Preprocessing

## 📊 Dataset Information

**Source:** [Kaggle - Flight Delay and Cancellation Dataset (2019-2023)](https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023/data)

### Original Dataset Statistics
- **Total Records:** 3,000,000 flight records
- **Total Columns:** 32 features
- **Time Period:** 2019-2023
- **File:** `flights_sample_3m.csv`

### Dataset Features
The original dataset contains comprehensive flight information including:
- Flight identification (dates, airline codes, flight numbers)
- Airport information (origin, destination, cities)
- Timing data (departure, arrival, taxi times)
- Delay information (various delay categories)
- Flight status (cancelled, diverted)

---

## 🎯 Phase I: Data Preprocessing (15%)

This phase focuses on preparing raw flight data for comprehensive analysis through systematic data preprocessing techniques.

### Objectives

**1. Data Collection & Quality Assessment**
- Data gathering and initial exploration
- Data type definition and validation
- Quality assessment and integrity checks

**2. Data Transformation**
- Data integration and aggregation
- Strategic sampling for efficient processing
- Data cleaning and missing value treatment

**3. Feature Engineering**
- Dimension reduction and feature selection
- New feature creation
- Discretization, binarization, and transformation

---

## 🔧 Preprocessing Pipeline

### 1. Data Types Definition
- Converted `FL_DATE` to datetime format
- Categorized airline and airport codes
- Ensured numeric types for delay and time columns

### 2. Data Quality Assessment

Initial State:
- 3,000,000 rows × 32 columns
- Total missing values: 16,062,854
- Identified 17 columns with missing data

**Key Findings:**
- `CANCELLATION_CODE`: 97.36% missing
- Delay attribution columns: 82.20% missing
- Operational columns: 2.59-2.87% missing

### 3. Missing Values Treatment

**Strategy Applied:**
- **Numeric columns:** Imputed with mean/median based on data distribution
- **Categorical columns:** Imputed with mode values
- **Result:** 100% data completeness achieved

### 4. Sampling
- Applied stratified sampling by airline
- Reduced dataset: **3,000,000 → 499,998 records**
- Maintained proportional airline distribution
- Sampling rate: 16.7%

### 5. Dimension Reduction

**Process:**
1. **Low Variance Removal:** Removed columns with variance < 0.01
2. **High Correlation Removal:** Eliminated features with correlation > 0.95
3. **Manual Redundancy Removal:** Dropped unnecessary/duplicate columns

**Results:**
- Original: 32 columns
- Final: 22 columns
- Reduction: 10 columns removed (31.2% reduction)

**Removed Columns:**
- Redundant time fields (CRS_DEP_TIME, DEP_TIME, etc.)
- Duplicate airport identifiers
- Low-variance indicators (DIVERTED)
- Highly correlated features (WHEELS_OFF, ARR_TIME, AIR_TIME, DISTANCE)

### 6. Feature Selection

**Key Variables for Analysis:**
- `ARR_DELAY` - Arrival delay (minutes)
- `DEP_DELAY` - Departure delay (minutes)
- `CANCELLED` - Flight cancellation indicator
- `ORIGIN` - Origin airport code
- `DEST` - Destination airport code
- `AIRLINE` - Airline identifier

### 7. Feature Engineering

**Created 5 New Features:**

1. **`delay_flag`** (Binary)
   - Logic: `(ARR_DELAY > 15).astype(int)`
   - Purpose: Binary delay indicator for flights delayed >15 minutes
   - Distribution: 85,401 delayed flights (17.1%)

2. **`elapsed_diff`** (Numeric)
   - Formula: `ELAPSED_TIME - CRS_ELAPSED_TIME`
   - Purpose: Difference between actual and scheduled flight duration

3. **`taxi_ratio`** (Numeric)
   - Formula: `(TAXI_OUT + TAXI_IN) / ELAPSED_TIME`
   - Purpose: Ground operation efficiency metric
   - Safe division: Handled zero/infinite values

4. **`avg_airline_delay`** (Numeric)
   - Calculation: Group mean of `ARR_DELAY` by `AIRLINE`
   - Purpose: Airline-specific delay tendency indicator

5. **`ROUTE`** (Categorical)
   - Format: `"ORIGIN-DEST"` (e.g., "LAX-JFK")
   - Purpose: Route identifier for origin-destination pairs

### 8. Discretization

**Delay Categorization:**
```
bins = [-999, 0, 15, 60, 999]
labels = ["Early", "OnTime", "MinorDelay", "SevereDelay"]
```

**Distribution:**
- Early: 337,301 flights (67.5%)
- OnTime: 77,296 flights (15.5%)
- MinorDelay: 56,439 flights (11.3%)
- SevereDelay: 28,810 flights (5.8%)

### 9. Binarization

**Binary Indicators Created:**
- `CANCELLED`: Flight cancellation (13,311 flights, 2.7%)
- `delay_flag`: Significant delay indicator (85,401 flights, 17.1%)
- `is_weekend`: Weekend flight indicator (136,772 flights, 27.4%)

### 10. Transformation & Scaling

**Applied Techniques:**

1. **MinMax Scaling:**
   - Scaled columns: `ARR_DELAY`, `DEP_DELAY`, `taxi_ratio`, `elapsed_diff`
   - Range: [0, 1]

2. **Log Transformation:**
   - Applied to skewed columns (skewness > 1)
   - Created `*_log` versions for better distribution

---

## 📈 Final Dataset Statistics

### Dimensions
- Shape: 499,998 rows × 45 columns
- Missing Values: 0 (100% complete)

### Column Breakdown
- **Numeric Columns:** 35
- **Categorical Columns:** 4
- **Binary Columns:** 6
- **New Features Created:** 7

### Data Quality Metrics
- ✅ Zero missing values
- ✅ All data types properly defined
- ✅ Normalized numeric features
- ✅ Categorical variables encoded
- ✅ Derived features integrated

---

## 📁 Output Files

### 1. flights_final_optimized.csv
- Complete preprocessed dataset
- All 499,998 records
- 45 features (22 original + 23 engineered/transformed)
- Ready for analysis and modeling

### 2. flights_final_preview.csv
- Sample dataset (5,000 records)
- Maintains data distribution
- Quick reference and validation

---

## 🎯 Preprocessing Summary

### Transformation Pipeline

```
Original Dataset (3M × 32)
    ↓
Type Definition & Quality Check
    ↓
Missing Value Treatment (16M+ values imputed)
    ↓
Stratified Sampling (500K × 32)
    ↓
Dimension Reduction (500K × 22)
    ↓
Feature Engineering (+7 features)
    ↓
Transformation & Scaling (+7 features)
    ↓
Final Dataset (500K × 45)
```

### Key Achievements
- ✅ **Data Completeness:** 100% (zero missing values)
- ✅ **Dimension Optimization:** 31.2% column reduction
- ✅ **Sample Efficiency:** 83.3% size reduction with maintained distribution
- ✅ **Feature Enrichment:** +40% more analytical features
- ✅ **Data Quality:** Normalized, scaled, and ready for ML

### Preprocessing Methods Applied
1. ✓ Data type definition
2. ✓ Data quality assessment
3. ✓ Missing value treatment (mean/median/mode imputation)
4. ✓ Stratified sampling
5. ✓ Dimension reduction (variance/correlation analysis)
6. ✓ Feature selection (reliability & delay focus)
7. ✓ Feature engineering (5 derived features)
8. ✓ Discretization (delay categorization)
9. ✓ Binarization (binary indicators)
10. ✓ Transformation & scaling (MinMax + log transform)

---

## 🚀 Next Steps

The preprocessed dataset is now ready for:
- **Exploratory Data Analysis (EDA)**
- **Statistical Analysis**
- **Machine Learning Model Development**
- **Predictive Analytics**
- **Visualization and Reporting**

---

## 📝 Technical Notes

### Dependencies
- `pandas >= 1.3.0`
- `numpy >= 1.21.0`
- `matplotlib >= 3.4.0`
- `seaborn >= 0.11.0`
- `scikit-learn >= 0.24.0`

### Processing Environment
- Python 3.8+
- Jupyter Notebook
- Memory-optimized for large datasets

---

## 👥 Project Information

**Course:** PVDH - Data Mining and Data Warehousing
**Phase:** I - Data Preprocessing (15%)
**Dataset:** Flight Delay and Cancellation (2019-2023)
**Objective:** Prepare flight data for reliability and delay analysis

---

## 📊 Data Dictionary (Selected Features)

| Feature | Type | Description |
|---------|------|-------------|
| FL_DATE | datetime | Flight date |
| AIRLINE | category | Airline name |
| ORIGIN | category | Origin airport code |
| DEST | category | Destination airport code |
| DEP_DELAY | float [0,1] | Departure delay (scaled) |
| ARR_DELAY | float [0,1] | Arrival delay (scaled) |
| CANCELLED | binary | Cancellation indicator |
| delay_flag | binary | Delay >15min indicator |
| elapsed_diff | float [0,1] | Actual vs scheduled duration difference |
| taxi_ratio | float [0,1] | Ground operations efficiency |
| avg_airline_delay | float | Airline average delay |
| ROUTE | string | Origin-Destination pair |
| delay_category | category | Delay severity classification |
| is_weekend | binary | Weekend flight indicator |

---

**Status:** ✅ Phase I Complete - Ready for Analysis
