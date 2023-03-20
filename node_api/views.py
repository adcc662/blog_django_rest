from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from node_api.models import NoteModel
from node_api.serializers import NoteSerializer
import math
from datetime import datetime



class Notes(generics.GenericAPIView):
    serializer_class = NoteSerializer
    queryset = NoteModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get('page', 1))
        limit_num = int(request.GET.get('limit', 10))
        start_num = int(page_num -1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get('search')
        note = NoteModel.objects.all()
        total_notes = note.count()
        if search_param:
            note = note.filter(title__icontains=search_param)
        serializer = NoteSerializer(note[start_num:end_num], many=True)
        return Response({
            'status': 'success',
            'total': total_notes,
            'page': page_num,
            'last_page': math.ceil(total_notes / limit_num),
            'notes': serializer.data
        })


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Note created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'error',
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class NoteDetail(generics.GenericAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer

    def get_note(self, pk):
        try:
            return NoteModel.objects.get(pk = pk)
        except:
            return None
        

    def get(request, self, pk):
        note = self.get_note(pk = pk)
        if note == None:
            return Response({"status": 'Failed', 'message': f"Message with ID: {pk} not found", 'status': status.HTTP_404_NOT_FOUND})
        serializer = self.serializer_class(note)
        return Response({'status': 'Succeed', 'note': serializer.data})
    

    def patch(request, self, pk):
        note = self.get_note(pk)
        if note == None:
            return Response({"status": 'Failed', 'message': f"Message with ID: {pk} not found", 'status': status.HTTP_404_NOT_FOUND})
        serializer = self.serializer_class(
            note, data = request.data, partial = True
        )
        if serializer.is_valid():
            serializer.validated_data['updated_at'] = datetime.now()
            serializer.save()
            return Response({'status': 'Succeed', 'note': serializer.data})
        return Response({'status': 'Failed', 'message': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        note = self.get_note(pk)
        if note == None:
            return Response({'status': 'Failed', 'message': f"Note with Id: {pk} not found"}, status = status.HTTP_404_NOT_FOUND)
        
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

    

