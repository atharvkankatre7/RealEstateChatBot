"""
Utility functions for query parsing and analysis generation
"""
import re
import os
import json
from typing import List, Dict, Any
import pandas as pd

# OpenAI integration (optional)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def parse_query_intent(query: str, available_localities: List[str]) -> Dict[str, Any]:
    """
    Parse the user query to extract intent and localities.
    
    Returns:
        {
            'type': 'single' or 'comparison',
            'localities': list of locality names,
            'metrics': list of metrics to show (price, demand, etc.)
        }
    """
    query_lower = query.lower()
    
    # Find mentioned localities
    found_localities = []
    for locality in available_localities:
        if locality.lower() in query_lower:
            found_localities.append(locality)
    
    # Determine metrics to show
    metrics = []
    if 'price' in query_lower or 'rate' in query_lower or 'cost' in query_lower:
        metrics.append('price')
    if 'demand' in query_lower or 'sold' in query_lower or 'sales' in query_lower:
        metrics.append('demand')
    
    # If no specific metric mentioned, show both
    if not metrics:
        metrics = ['price', 'demand']
    
    # Determine type
    intent_type = 'comparison' if len(found_localities) > 1 else 'single'
    
    return {
        'type': intent_type,
        'localities': found_localities,
        'metrics': metrics
    }


def filter_data_by_locality(df: pd.DataFrame, locality: str) -> pd.DataFrame:
    """Filter DataFrame by locality name."""
    return df[df['final location'] == locality].sort_values('year')


def extract_chart_data(df: pd.DataFrame, localities: List[str], metrics: List[str]) -> Dict[str, Any]:
    """
    Extract chart data from the filtered DataFrame.
    
    Returns:
        {
            'years': [...],
            'prices': [...],  # or prices_by_locality for comparison
            'demand': [...],  # or demand_by_locality for comparison
        }
    """
    chart_data = {
        'years': []
    }
    
    if len(localities) == 1:
        # Single locality
        locality_df = filter_data_by_locality(df, localities[0])
        chart_data['years'] = locality_df['year'].tolist()
        
        if 'price' in metrics:
            # Use flat weighted average rate as price metric
            chart_data['prices'] = locality_df['flat - weighted average rate'].round(2).tolist()
        
        if 'demand' in metrics:
            # Use flat_sold - igr as demand metric
            chart_data['demand'] = locality_df['flat_sold - igr'].tolist()
    
    else:
        # Multiple localities - comparison
        years = sorted(df['year'].unique())
        chart_data['years'] = years
        
        if 'price' in metrics:
            chart_data['prices_by_locality'] = {}
            for locality in localities:
                locality_df = filter_data_by_locality(df, locality)
                prices = []
                for year in years:
                    year_data = locality_df[locality_df['year'] == year]
                    if not year_data.empty:
                        prices.append(round(year_data['flat - weighted average rate'].iloc[0], 2))
                    else:
                        prices.append(None)
                chart_data['prices_by_locality'][locality] = prices
        
        if 'demand' in metrics:
            chart_data['demand_by_locality'] = {}
            for locality in localities:
                locality_df = filter_data_by_locality(df, locality)
                demands = []
                for year in years:
                    year_data = locality_df[locality_df['year'] == year]
                    if not year_data.empty:
                        demands.append(int(year_data['flat_sold - igr'].iloc[0]))
                    else:
                        demands.append(None)
                chart_data['demand_by_locality'][locality] = demands
    
    return chart_data


def format_table_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert DataFrame to list of dictionaries for JSON response."""
    # Select relevant columns
    columns_to_include = [
        'final location', 'year', 'city',
        'total_sales - igr', 'total sold - igr',
        'flat_sold - igr', 'flat - weighted average rate',
        'total units', 'total carpet area supplied (sqft)'
    ]
    
    # Filter to only existing columns
    existing_columns = [col for col in columns_to_include if col in df.columns]
    
    # Convert to dict
    result = df[existing_columns].to_dict('records')
    
    # Clean up the data (remove commas from numbers if they're strings)
    for row in result:
        for key, value in row.items():
            if isinstance(value, str):
                # Try to clean numeric values
                cleaned = value.replace(',', '').strip()
                try:
                    if '.' in cleaned:
                        row[key] = float(cleaned)
                    else:
                        row[key] = int(cleaned)
                except ValueError:
                    row[key] = value
    
    return result


def generate_summary_with_openai(intent: Dict[str, Any], chart_data: Dict[str, Any], df: pd.DataFrame, mock_summary: str) -> str:
    """
    Generate summary using OpenAI API if available, otherwise return mock summary.
    """
    if not OPENAI_AVAILABLE:
        return mock_summary
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return mock_summary
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Prepare data context for OpenAI
        localities = intent['localities']
        data_context = []
        
        for locality in localities:
            locality_df = filter_data_by_locality(df, locality)
            if not locality_df.empty:
                data_context.append({
                    'locality': locality,
                    'years': locality_df['year'].tolist(),
                    'prices': locality_df['flat - weighted average rate'].tolist(),
                    'demand': locality_df['flat_sold - igr'].tolist(),
                    'total_sales': locality_df['total_sales - igr'].sum()
                })
        
        prompt = f"""Analyze the following real estate data and provide a comprehensive, natural language summary:

Data: {json.dumps(data_context, indent=2)}

Query Type: {'Comparison' if intent['type'] == 'comparison' else 'Single Analysis'}
Metrics Requested: {', '.join(intent['metrics'])}

Provide a detailed, professional analysis covering:
1. Key trends and patterns
2. Price movements and growth rates
3. Demand patterns
4. Market insights and recommendations
5. Comparative analysis (if multiple localities)

Format the response in a clear, readable manner with proper sections."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a real estate market analyst providing data-driven insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return mock_summary


def generate_summary(intent: Dict[str, Any], chart_data: Dict[str, Any], df: pd.DataFrame) -> str:
    """
    Generate a natural language summary of the analysis.
    Tries OpenAI first, falls back to mock summary.
    """
    localities = intent['localities']
    metrics = intent['metrics']
    
    if not localities:
        return "No localities found in the query. Please specify a locality like Wakad, Aundh, Akurdi, or Ambegaon Budruk."
    
    if intent['type'] == 'single':
        locality = localities[0]
        locality_df = filter_data_by_locality(df, locality)
        
        if locality_df.empty:
            return f"No data found for {locality}."
        
        # Get first and last year data
        first_year = locality_df.iloc[0]
        last_year = locality_df.iloc[-1]
        
        summary_parts = [f"📊 **Analysis of {locality}**\n"]
        
        if 'price' in metrics:
            first_price = first_year['flat - weighted average rate']
            last_price = last_year['flat - weighted average rate']
            price_change = ((last_price - first_price) / first_price) * 100
            
            summary_parts.append(
                f"**Price Trends ({first_year['year']}-{last_year['year']}):**\n"
                f"The average flat price in {locality} has changed from ₹{first_price:,.2f} per sqft "
                f"in {first_year['year']} to ₹{last_price:,.2f} per sqft in {last_year['year']}, "
                f"showing a {'growth' if price_change > 0 else 'decline'} of {abs(price_change):.1f}%.\n"
            )
        
        if 'demand' in metrics:
            first_demand = first_year['flat_sold - igr']
            last_demand = last_year['flat_sold - igr']
            demand_change = ((last_demand - first_demand) / first_demand) * 100
            
            summary_parts.append(
                f"**Demand Trends ({first_year['year']}-{last_year['year']}):**\n"
                f"Flat sales in {locality} changed from {first_demand:,} units "
                f"in {first_year['year']} to {last_demand:,} units in {last_year['year']}, "
                f"showing a {'growth' if demand_change > 0 else 'decline'} of {abs(demand_change):.1f}%.\n"
            )
        
        # Add total sales info
        total_sales = locality_df['total_sales - igr'].sum()
        total_units = locality_df['total sold - igr'].sum()
        
        summary_parts.append(
            f"**Overall Performance:**\n"
            f"Total sales value over the period: ₹{total_sales:,.0f}\n"
            f"Total units sold: {total_units:,} units"
        )
        
        mock_summary = "\n".join(summary_parts)
        
        # Try OpenAI, fallback to mock
        return generate_summary_with_openai(intent, chart_data, df, mock_summary)
    
    else:
        # Comparison
        summary_parts = [f"📊 **Comparison: {' vs '.join(localities)}**\n"]
        
        if 'price' in metrics and 'prices_by_locality' in chart_data:
            summary_parts.append("**Price Comparison:**")
            for locality in localities:
                locality_df = filter_data_by_locality(df, locality)
                if not locality_df.empty:
                    first_price = locality_df.iloc[0]['flat - weighted average rate']
                    last_price = locality_df.iloc[-1]['flat - weighted average rate']
                    price_change = ((last_price - first_price) / first_price) * 100
                    summary_parts.append(
                        f"- {locality}: ₹{first_price:,.2f} → ₹{last_price:,.2f} "
                        f"({'+' if price_change > 0 else ''}{price_change:.1f}%)"
                    )
            summary_parts.append("")
        
        if 'demand' in metrics and 'demand_by_locality' in chart_data:
            summary_parts.append("**Demand Comparison:**")
            for locality in localities:
                locality_df = filter_data_by_locality(df, locality)
                if not locality_df.empty:
                    first_demand = locality_df.iloc[0]['flat_sold - igr']
                    last_demand = locality_df.iloc[-1]['flat_sold - igr']
                    demand_change = ((last_demand - first_demand) / first_demand) * 100
                    summary_parts.append(
                        f"- {locality}: {first_demand:,} → {last_demand:,} units "
                        f"({'+' if demand_change > 0 else ''}{demand_change:.1f}%)"
                    )
            summary_parts.append("")
        
        # Find best performer
        best_locality = None
        best_growth = float('-inf')
        
        for locality in localities:
            locality_df = filter_data_by_locality(df, locality)
            if not locality_df.empty:
                if 'price' in metrics:
                    first_price = locality_df.iloc[0]['flat - weighted average rate']
                    last_price = locality_df.iloc[-1]['flat - weighted average rate']
                    growth = ((last_price - first_price) / first_price) * 100
                    if growth > best_growth:
                        best_growth = growth
                        best_locality = locality
        
        if best_locality:
            summary_parts.append(
                f"**Key Insight:**\n"
                f"{best_locality} shows the strongest price growth at {best_growth:.1f}% over the analyzed period."
            )
        
        mock_summary = "\n".join(summary_parts)
        
        # Try OpenAI, fallback to mock
        return generate_summary_with_openai(intent, chart_data, df, mock_summary)
