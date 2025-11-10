
<table border="0">
 <tr>
    <td><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/University_of_Prishtina_logo.svg/1200px-University_of_Prishtina_logo.svg.png" width="150" alt="University Logo" /></td>
    <td>
      <p>Universiteti i Prishtinës</p>
      <p>Fakulteti i Inxhinierisë Elektrike dhe Kompjuterike</p>
      <p>Inxhinieri Kompjuterike dhe Softuerike - Programi Master</p>
      <p>Profesor: Prof. Mergim Hoti</p>
      <p>Studentë: Endrita Vllasalii
                   Gent Zushi
                   Milot Qorolli</p>
    </td>
 </tr>
</table>

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


### 6. Feature Engineering

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

### 7. Discretization

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

### 8. Binarization

**Binary Indicators Created:**
- `CANCELLED`: Flight cancellation 
- `delay_flag`: Significant delay indicator
- `is_weekend`: Weekend flight indicator 


## 📈 Final Dataset Statistics

### Dimensions
- Shape: 499,998 rows × 29 columns
- Missing Values: 0 (100% complete)


### Data Quality Metrics
- Zero missing values
- All data types properly defined
- Normalized numeric features
- Categorical variables encoded
- Derived features integrated


