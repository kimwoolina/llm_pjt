from django.shortcuts import render
import pandas as pd
from .serializers import LocationDataSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.conf import settings

def index(request):
    return render(request, "myapp/index.html")


class LocationDataView(APIView):
    def get(self, request, *args, **kwargs):
        # 엑셀 파일의 절대 경로를 설정
        excel_file_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'myapp', 'location.xlsx')
        
        # 디버깅: 경로 확인
        print(f"엑셀 파일 경로: {excel_file_path}")

        # 엑셀 파일을 읽어들임
        df = pd.read_excel(excel_file_path)

        location_data = []

        # 각 행을 순회하며 딕셔너리로 변환
        for _, row in df.iterrows():
            level1 = row['1단계'] if pd.notna(row['1단계']) else None
            level2 = row['2단계'] if pd.notna(row['2단계']) else None
            level3 = row['3단계'] if pd.notna(row['3단계']) else None
            x = row['격자 X']
            y = row['격자 Y']

            if pd.notna(level3):
                location_data.append({'name': level3, 'x': x, 'y': y})
            elif pd.notna(level2):
                location_data.append({'name': level2, 'x': x, 'y': y})
            elif pd.notna(level1):
                location_data.append({'name': level1, 'x': x, 'y': y})

        # 데이터를 직렬화하고 응답으로 보냄
        serializer = LocationDataSerializer(location_data, many=True)
        return Response(serializer.data)
