from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from api.serializers import RoomSerializer

# Creating url path directly in views:

# @api_view(['GET'])
# def get_routes(request):
#     routes = [
#         'GET /api'
#         'GET /api/rooms',
#         'GET /api/rooms/:id'
#     ]
#     return Response(routes)


# For all rooms:
@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) # many stands for multiple objects we need to serialize
    return Response(serializer.data)


# For 1 room:
@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

