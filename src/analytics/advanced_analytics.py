#!/usr/bin/env python3
"""
Advanced Healthcare Analytics
============================
Comprehensive advanced analytics for healthcare data including
predictive modeling, statistical analysis, and business intelligence.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedHealthcareAnalytics:
    """Advanced analytics for healthcare data"""
    
    def __init__(self):
        """Initialize advanced analytics"""
        self.scaler = StandardScaler()
        self.pca = PCA()
        
    def cohort_analysis(self, df: pd.DataFrame, patient_col: str, date_col: str, 
                       value_col: str) -> Dict[str, Any]:
        """Perform cohort analysis for patient retention"""
        try:
            # Convert date column to datetime
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Create cohort groups based on first visit
            df['cohort'] = df.groupby(patient_col)[date_col].transform('min')
            df['cohort_period'] = (df[date_col] - df['cohort']).dt.days
            
            # Create cohort table
            cohort_table = df.groupby(['cohort', 'cohort_period'])[patient_col].nunique().unstack(0)
            
            # Calculate retention rates
            cohort_sizes = cohort_table.iloc[0]
            retention_table = cohort_table.divide(cohort_sizes, axis=1)
            
            # Calculate average retention
            avg_retention = retention_table.mean(axis=1)
            
            return {
                'cohort_table': cohort_table,
                'retention_table': retention_table,
                'avg_retention': avg_retention,
                'cohort_sizes': cohort_sizes
            }
            
        except Exception as e:
            logger.error(f"Error in cohort analysis: {e}")
            return {}
    
    def rfm_analysis(self, df: pd.DataFrame, patient_col: str, date_col: str, 
                    value_col: str) -> Dict[str, Any]:
        """Perform RFM (Recency, Frequency, Monetary) analysis"""
        try:
            # Convert date column to datetime
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Calculate RFM metrics
            rfm = df.groupby(patient_col).agg({
                date_col: lambda x: (datetime.now() - x.max()).days,  # Recency
                patient_col: 'count',  # Frequency
                value_col: 'sum'  # Monetary
            }).rename(columns={
                date_col: 'recency',
                patient_col: 'frequency',
                value_col: 'monetary'
            })
            
            # Create RFM scores (1-5 scale)
            rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
            rfm['f_score'] = pd.qcut(rfm['frequency'], 5, labels=[1,2,3,4,5])
            rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])
            
            # Combine scores
            rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
            
            # Segment patients
            rfm['segment'] = rfm['rfm_score'].map({
                '555': 'Champions', '554': 'Champions', '544': 'Champions',
                '555': 'Champions', '554': 'Champions', '544': 'Champions',
                '543': 'Loyal Customers', '542': 'Loyal Customers', '541': 'Loyal Customers',
                '533': 'Potential Loyalists', '532': 'Potential Loyalists', '531': 'Potential Loyalists',
                '522': 'New Customers', '521': 'New Customers', '511': 'New Customers',
                '444': 'Promising', '443': 'Promising', '442': 'Promising',
                '433': 'Need Attention', '432': 'Need Attention', '431': 'Need Attention',
                '422': 'About to Sleep', '421': 'About to Sleep', '411': 'About to Sleep',
                '333': 'At Risk', '332': 'At Risk', '331': 'At Risk',
                '322': 'Cannot Lose Them', '321': 'Cannot Lose Them', '311': 'Cannot Lose Them',
                '222': 'Hibernating', '221': 'Hibernating', '211': 'Hibernating',
                '111': 'Lost'
            })
            
            return {
                'rfm_data': rfm,
                'segment_counts': rfm['segment'].value_counts(),
                'avg_metrics': rfm.groupby('segment')[['recency', 'frequency', 'monetary']].mean()
            }
            
        except Exception as e:
            logger.error(f"Error in RFM analysis: {e}")
            return {}
    
    def time_series_decomposition(self, df: pd.DataFrame, date_col: str, 
                                 value_col: str) -> Dict[str, Any]:
        """Perform time series decomposition"""
        try:
            # Convert date column to datetime
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Sort by date
            df = df.sort_values(date_col)
            
            # Create time series
            ts = df.set_index(date_col)[value_col]
            
            # Resample to daily frequency
            ts_daily = ts.resample('D').sum()
            
            # Decompose time series
            from statsmodels.tsa.seasonal import seasonal_decompose
            
            decomposition = seasonal_decompose(ts_daily, model='additive', period=7)
            
            return {
                'original': decomposition.observed,
                'trend': decomposition.trend,
                'seasonal': decomposition.seasonal,
                'residual': decomposition.resid,
                'decomposition': decomposition
            }
            
        except Exception as e:
            logger.error(f"Error in time series decomposition: {e}")
            return {}
    
    def patient_segmentation(self, df: pd.DataFrame, features: List[str]) -> Dict[str, Any]:
        """Perform patient segmentation using clustering"""
        try:
            # Prepare features
            X = df[features].fillna(0)
            
            # Standardize features
            X_scaled = self.scaler.fit_transform(X)
            
            # Determine optimal number of clusters
            inertias = []
            for k in range(1, 11):
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(X_scaled)
                inertias.append(kmeans.inertia_)
            
            # Perform clustering with optimal k
            optimal_k = 4  # You can implement elbow method here
            kmeans = KMeans(n_clusters=optimal_k, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Add cluster labels
            df['cluster'] = clusters
            
            # Analyze clusters
            cluster_analysis = df.groupby('cluster')[features].mean()
            
            return {
                'clusters': clusters,
                'cluster_centers': kmeans.cluster_centers_,
                'cluster_analysis': cluster_analysis,
                'inertias': inertias
            }
            
        except Exception as e:
            logger.error(f"Error in patient segmentation: {e}")
            return {}
    
    def statistical_analysis(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis"""
        try:
            stats_results = {}
            
            for col in numeric_cols:
                if col in df.columns:
                    data = df[col].dropna()
                    
                    # Descriptive statistics
                    desc_stats = {
                        'count': len(data),
                        'mean': data.mean(),
                        'median': data.median(),
                        'std': data.std(),
                        'min': data.min(),
                        'max': data.max(),
                        'q25': data.quantile(0.25),
                        'q75': data.quantile(0.75),
                        'skewness': data.skew(),
                        'kurtosis': data.kurtosis()
                    }
                    
                    # Normality test
                    shapiro_stat, shapiro_p = stats.shapiro(data)
                    
                    # Outlier detection (IQR method)
                    Q1 = data.quantile(0.25)
                    Q3 = data.quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = data[(data < Q1 - 1.5 * IQR) | (data > Q3 + 1.5 * IQR)]
                    
                    stats_results[col] = {
                        'descriptive': desc_stats,
                        'normality_test': {
                            'shapiro_stat': shapiro_stat,
                            'shapiro_p': shapiro_p,
                            'is_normal': shapiro_p > 0.05
                        },
                        'outliers': {
                            'count': len(outliers),
                            'values': outliers.tolist()
                        }
                    }
            
            return stats_results
            
        except Exception as e:
            logger.error(f"Error in statistical analysis: {e}")
            return {}
    
    def correlation_analysis(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, Any]:
        """Perform correlation analysis"""
        try:
            # Select numeric columns
            numeric_df = df[numeric_cols].select_dtypes(include=[np.number])
            
            # Calculate correlation matrix
            correlation_matrix = numeric_df.corr()
            
            # Find high correlations
            high_correlations = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:  # High correlation threshold
                        high_correlations.append({
                            'var1': correlation_matrix.columns[i],
                            'var2': correlation_matrix.columns[j],
                            'correlation': corr_value
                        })
            
            return {
                'correlation_matrix': correlation_matrix,
                'high_correlations': high_correlations
            }
            
        except Exception as e:
            logger.error(f"Error in correlation analysis: {e}")
            return {}
    
    def predictive_analytics(self, df: pd.DataFrame, target_col: str, 
                           feature_cols: List[str]) -> Dict[str, Any]:
        """Perform predictive analytics"""
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_squared_error, r2_score
            
            # Prepare data
            X = df[feature_cols].fillna(0)
            y = df[target_col].fillna(0)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return {
                'model': model,
                'predictions': y_pred,
                'mse': mse,
                'r2_score': r2,
                'feature_importance': feature_importance
            }
            
        except Exception as e:
            logger.error(f"Error in predictive analytics: {e}")
            return {}
    
    def generate_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate business insights from data"""
        insights = []
        
        try:
            # Data quality insights
            total_records = len(df)
            missing_data = df.isnull().sum().sum()
            missing_percentage = (missing_data / (total_records * len(df.columns))) * 100
            
            if missing_percentage > 10:
                insights.append(f" High missing data: {missing_percentage:.1f}% of records have missing values")
            else:
                insights.append(f" Data quality good: {missing_percentage:.1f}% missing data")
            
            # Temporal insights
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                date_range = (df['timestamp'].max() - df['timestamp'].min()).days
                insights.append(f" Data spans {date_range} days")
            
            # Patient insights
            if 'patient_id' in df.columns:
                unique_patients = df['patient_id'].nunique()
                insights.append(f" {unique_patients} unique patients")
            
            # Value insights
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                for col in numeric_cols[:3]:  # Top 3 numeric columns
                    if col in df.columns:
                        mean_val = df[col].mean()
                        insights.append(f" {col} average: {mean_val:.2f}")
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            insights.append(" Error generating insights")
        
        return insights

def main():
    """Main function to demonstrate advanced analytics"""
    print("Advanced Healthcare Analytics")
    print("=" * 30)
    
    # Initialize analytics
    analytics = AdvancedHealthcareAnalytics()
    
    # Sample data
    np.random.seed(42)
    n_patients = 1000
    n_days = 365
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    data = []
    for i in range(n_patients):
        patient_id = f"P{i:03d}"
        for j in range(np.random.randint(1, 10)):  # 1-9 visits per patient
            date = np.random.choice(dates)
            data.append({
                'patient_id': patient_id,
                'date': date,
                'age': np.random.randint(18, 80),
                'heart_rate': np.random.randint(60, 120),
                'blood_pressure': np.random.randint(100, 180),
                'temperature': np.random.uniform(97, 100),
                'visit_cost': np.random.uniform(100, 1000)
            })
    
    df = pd.DataFrame(data)
    
    print(f"Generated {len(df)} records for {df['patient_id'].nunique()} patients")
    
    # Test analytics functions
    print("\n1. Cohort Analysis")
    cohort_results = analytics.cohort_analysis(df, 'patient_id', 'date', 'visit_cost')
    print(f"   Cohort analysis completed: {len(cohort_results)} results")
    
    print("\n2. RFM Analysis")
    rfm_results = analytics.rfm_analysis(df, 'patient_id', 'date', 'visit_cost')
    print(f"   RFM analysis completed: {len(rfm_results)} results")
    
    print("\n3. Statistical Analysis")
    stats_results = analytics.statistical_analysis(df, ['age', 'heart_rate', 'blood_pressure'])
    print(f"   Statistical analysis completed: {len(stats_results)} variables")
    
    print("\n4. Correlation Analysis")
    corr_results = analytics.correlation_analysis(df, ['age', 'heart_rate', 'blood_pressure', 'temperature'])
    print(f"   Correlation analysis completed: {len(corr_results)} results")
    
    print("\n5. Business Insights")
    insights = analytics.generate_insights(df)
    for insight in insights:
        print(f"   {insight}")
    
    print("\n Advanced analytics features demonstrated successfully!")

if __name__ == "__main__":
    main()
