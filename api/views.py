from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
<<<<<<< HEAD
from data_processing.prediction import make_prediction  
from data_management.calculate_thi import calculate_thi
import json  # Add this import at the top of your file

class PredictionAPIView(APIView):
    def post(self, request):
        data = request.data
        result = make_prediction(data)
        return Response({"prediction": result})
=======
# from data_processing.prediction import make_prediction  
from data_management.calculate_thi import calculate_thi
import json  # Add this import at the top of your file

# class PredictionAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         result = make_prediction(data)
#         return Response({"prediction": result})
>>>>>>> origin/New_ui

class CalculateTHIAPIView(APIView):
    def get(self, request):
        try:
            thi_data = calculate_thi()
            # Convert DataFrame to JSON
            thi_json = thi_data.to_json(orient='records', date_format='iso')
            return JsonResponse(thi_json, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class CalculateTHIDataAPIView(APIView):
    def get(self, request):
        try:
            germany_thi_data, poland_thi_data = calculate_thi()
            germany_thi_json = germany_thi_data.to_json(orient='records', date_format='iso')
            poland_thi_json = poland_thi_data.to_json(orient='records', date_format='iso')
            
            # Combine both datasets into a single response
            response_data = {
                'Germany': json.loads(germany_thi_json),
                'Poland': json.loads(poland_thi_json)
            }
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
