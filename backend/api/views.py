"""
API Views for Real Estate Chatbot
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .apps import ApiConfig
from .utils import (
    parse_query_intent,
    filter_data_by_locality,
    extract_chart_data,
    format_table_data,
    generate_summary
)


@api_view(['POST'])
def query_analysis(request):
    """
    Process natural language query and return analysis.
    
    POST /api/query/
    Body: { "query": "Analyze Wakad" }
    
    Returns: {
        "summary": "text summary",
        "chartData": {...},
        "tableData": [...],
        "localities": [...]
    }
    """
    try:
        query = request.data.get('query', '')
        
        if not query:
            return Response(
                {'error': 'Query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get DataFrame from app config
        df = ApiConfig.real_estate_df
        
        if df is None or df.empty:
            return Response(
                {'error': 'Real estate data not loaded'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get available localities
        available_localities = df['final location'].unique().tolist()
        
        # Parse query intent
        intent = parse_query_intent(query, available_localities)
        
        if not intent['localities']:
            return Response({
                'summary': f"I couldn't identify any localities in your query. Available localities are: {', '.join(available_localities)}. Please try again with a specific locality.",
                'chartData': {'years': []},
                'tableData': [],
                'localities': []
            })
        
        # Filter data for requested localities
        filtered_df = df[df['final location'].isin(intent['localities'])]
        
        if filtered_df.empty:
            return Response({
                'summary': f"No data found for the requested localities: {', '.join(intent['localities'])}",
                'chartData': {'years': []},
                'tableData': [],
                'localities': intent['localities']
            })
        
        # Extract chart data
        chart_data = extract_chart_data(df, intent['localities'], intent['metrics'])
        
        # Format table data
        table_data = format_table_data(filtered_df)
        
        # Generate summary
        summary = generate_summary(intent, chart_data, df)
        
        return Response({
            'summary': summary,
            'chartData': chart_data,
            'tableData': table_data,
            'localities': intent['localities'],
            'metrics': intent['metrics'],
            'type': intent['type']
        })
    
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_localities(request):
    """
    Get list of all available localities.
    
    GET /api/localities/
    
    Returns: {
        "localities": ["Akurdi", "Ambegaon Budruk", ...]
    }
    """
    try:
        df = ApiConfig.real_estate_df
        
        if df is None or df.empty:
            return Response(
                {'error': 'Real estate data not loaded'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        localities = sorted(df['final location'].unique().tolist())
        
        return Response({
            'localities': localities,
            'count': len(localities)
        })
    
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint.
    
    GET /api/health/
    """
    df = ApiConfig.real_estate_df
    
    return Response({
        'status': 'ok',
        'data_loaded': df is not None and not df.empty,
        'rows': len(df) if df is not None else 0
    })


@api_view(['POST'])
def download_data(request):
    """
    Download data in CSV or JSON format.
    
    POST /api/download/
    Body: {
        "tableData": [...],
        "format": "csv" or "json"
    }
    """
    from django.http import HttpResponse
    import csv
    import json
    
    try:
        table_data = request.data.get('tableData', [])
        format_type = request.data.get('format', 'csv').lower()
        
        if not table_data:
            return Response(
                {'error': 'No data provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if format_type == 'json':
            response = HttpResponse(
                json.dumps(table_data, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = 'attachment; filename="real_estate_data.json"'
            return response
        
        elif format_type == 'csv':
            if not table_data:
                return Response(
                    {'error': 'No data to export'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get all unique keys from the data
            fieldnames = set()
            for row in table_data:
                fieldnames.update(row.keys())
            fieldnames = sorted(list(fieldnames))
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="real_estate_data.csv"'
            
            writer = csv.DictWriter(response, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(table_data)
            
            return response
        
        else:
            return Response(
                {'error': 'Invalid format. Use "csv" or "json"'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )