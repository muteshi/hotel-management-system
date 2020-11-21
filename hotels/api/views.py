from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
    ListCreateAPIView,
)

from hotels.models import (
    Hotels,
    HotelTypes,
    PackageTypes,
    Packages,
    HotelPackages,
    Itinirery,
    Room,
    RoomTypes,
    Photo,
    RoomPhoto,
    PackagePhoto,

)
from .serializers import (
    HotelAdminCreateSerializer,
    HotelOwnerCreateSerializer,
    HotelSerializers,
    HotelTypesSerializers,
    HotelFacilitiesSerializers,
    HotelSettingsSerializers,
    HotelPolicySerializers,
    HotelDetailSerializer,
    RoomSerializer,
    RoomDetailSerializer,
    RoomTypesSerializers,
    RoomAmmenitiesSerializers,
    RoomSettingsSerializers,
    PackageTypeSerializers,
    PackageSerializer,
    PackagePhotoSerializer,
    ItinirerySerializer,
    HotelPackageSerializer,
    PhotoSerializer,
    RoomPhotoSerializer
)
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import UpdateModelMixin
from rest_framework import status, permissions
from django.db.models import Q
from rest_framework.response import Response
from django.http import Http404
from .permissions import IsAdminOrOwner, IsAdmin
from .helper import (
    modify_input_for_multiple_files,
    modify_input_for_multiple_room_files,
    modify_input_for_multiple_package_files
)

# Start hotel object API CRUD classes


class HotelTypeListAPIView(ListAPIView):
    """Displays list of hotel types"""
    queryset = HotelTypes.objects.all()
    serializer_class = HotelTypesSerializers
    permission_classes = (permissions.AllowAny,)


class HotelCreateAPIView(CreateAPIView):
    """Create a new hotel object"""
    queryset = Hotels.objects.all()
    # serializer_class = HotelCreateSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return HotelAdminCreateSerializer
        return HotelOwnerCreateSerializer

    def perform_create(self, serializer):
        serializer.save(contact_person=self.request.user)


class HotelDetailAPIView(RetrieveAPIView):
    """Display details of a single hotel"""
    queryset = Hotels.objects.all()
    serializer_class = HotelDetailSerializer
    permission_classes = ()
    lookup_field = 'slug'


class HotelUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of a hotel object"""
    queryset = Hotels.objects.all()
    serializer_class = HotelSerializers
    permission_classes = (IsAdminOrOwner,)
    lookup_field = 'slug'

    def perform_update(self, serializers):
        serializers.save(contact_person=self.request.user)


class HotelFacilitiesUpdateAPIView(RetrieveUpdateAPIView):
    """Updates facility details of a hotel object"""
    queryset = Hotels.objects.all()
    serializer_class = HotelFacilitiesSerializers
    permission_classes = (IsAdminOrOwner,)
    lookup_field = 'slug'

    def perform_update(self, serializers):
        serializers.save(contact_person=self.request.user)


class HotelSettingsUpdateAPIView(RetrieveUpdateAPIView):
    """Updates setting details of a hotel object"""
    queryset = Hotels.objects.all()
    serializer_class = HotelSettingsSerializers
    permission_classes = (IsAdminOrOwner,)
    lookup_field = 'slug'

    def perform_update(self, serializers):
        serializers.save(contact_person=self.request.user)


class HotelPolicyUpdateAPIView(RetrieveUpdateAPIView):
    """Updates setting details of a hotel's policy object"""
    queryset = Hotels.objects.all()
    serializer_class = HotelPolicySerializers
    permission_classes = (IsAdminOrOwner,)
    lookup_field = 'slug'

    def perform_update(self, serializers):
        serializers.save(contact_person=self.request.user)


class HotelPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    For enabling partial update of the model by admins
    '''
    queryset = Hotels.objects.all()
    serializer_class = HotelSerializers
    permission_classes = (IsAdmin,)
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class HotelDeleteAPIView(DestroyAPIView):
    """Deletes a hotel object"""
    queryset = Hotels.objects.all()
    serializer_class = HotelSerializers
    permission_classes = (IsAdminOrOwner,)

    def destroy(self, request, *args, **kwargs):
        """Override default destroy method"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class HotelsListAPIView(ListAPIView):
    """Returns hotels for specific web user"""

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return HotelAdminCreateSerializer
        return HotelOwnerCreateSerializer

    permission_classes = ()

    def get_queryset(self, *args, **kwargs):
        if (self.request.user and self.request.user.is_superuser) or (self.request.user.is_staff == False):
            hotels = Hotels.objects.all()
        else:
            hotels = Hotels.objects.filter(
                Q(contact_person=self.request.user.id))

        return hotels


class HotelsAPIView(ListAPIView):
    """Displays all hotels on the mobile device"""
    queryset = Hotels.objects.all()
    serializer_class = HotelAdminCreateSerializer
    permission_classes = (permissions.AllowAny,)


class ConferenceHotelsListAPIView(ListAPIView):

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return HotelAdminCreateSerializer
        return HotelOwnerCreateSerializer

    permission_classes = ()

    def get_queryset(self, *args, **kwargs):

        return Hotels.objects.filter(
            Q(has_conference=True))


# Start Room Object CRUD API classes


class RoomTypeListAPIView(ListAPIView):
    """Displays list of hotel types"""
    queryset = RoomTypes.objects.all()
    serializer_class = RoomTypesSerializers
    permission_classes = (permissions.AllowAny,)


class RoomCreateAPIView(CreateAPIView):
    """Create a new room object"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAdminOrOwner,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RoomsListAPIView(ListAPIView):
    """Displays list of hotel rooms"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """Filter hotels based on the hotel"""
        return Room.objects.filter(hotel=self.kwargs['pk'])


class RoomDetailAPIView(RetrieveAPIView):
    """Displays details of a hotel room"""
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    permission_classes = (permissions.AllowAny,)


class RoomUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of a hotel room"""
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    permission_classes = (permissions.AllowAny,)


class RoomDeleteAPIView(DestroyAPIView):
    """Deletes a hotel room object"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.AllowAny,)


class RoomAmmenitiesUpdateAPIView(RetrieveUpdateAPIView):
    """Updates amenity details of a room object"""
    queryset = Room.objects.all()
    serializer_class = RoomAmmenitiesSerializers
    permission_classes = (IsAdminOrOwner,)

    def perform_update(self, serializers):
        serializers.save(user=self.request.user)


class RoomSettingsUpdateAPIView(RetrieveUpdateAPIView):
    """Updates setting details of a hotel object"""
    queryset = Room.objects.all()
    serializer_class = RoomSettingsSerializers
    permission_classes = (IsAdminOrOwner,)

    def perform_update(self, serializers):
        serializers.save(user=self.request.user)


# Start Packages Object CRUD classes

class PackagePartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    For enabling partial update of the model by admins
    '''
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PackageTypeListAPIView(ListAPIView):
    """Displays list of package types"""
    queryset = PackageTypes.objects.all()
    serializer_class = PackageTypeSerializers
    permission_classes = ()


class PackageCreateAPIView(CreateAPIView):
    """Create a new package object"""
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (IsAdminOrOwner,)
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PackagesListAPIView(ListAPIView):
    """Displays list of hotel packages"""
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (permissions.AllowAny,)


class PackageDetailAPIView(RetrieveAPIView):
    """Displays details of a hotel package"""
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'


class PackageUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of a hotel package"""
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'


class PackageDeleteAPIView(DestroyAPIView):
    """Deletes  a hotel package"""
    queryset = Packages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (IsAdminOrOwner,)
    lookup_field = 'slug'


class HotelPackageCreateAPIView(CreateAPIView):
    """Create a new hotel package object"""
    queryset = HotelPackages.objects.all()
    serializer_class = HotelPackageSerializer
    permission_classes = (IsAdminOrOwner,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HotelPackageListAPIView(ListAPIView):
    """Displays list of hotels in a package"""
    queryset = HotelPackages.objects.all()
    serializer_class = HotelPackageSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """Filter hotel packages based on the package"""
        return HotelPackages.objects.filter(package=self.kwargs['pk'])


class HotelPackageDetailAPIView(RetrieveAPIView):
    """Displays details of a hotel package"""
    queryset = HotelPackages.objects.all()
    serializer_class = HotelPackageSerializer
    permission_classes = (permissions.AllowAny,)


class HotelPackageUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of a hotel package"""
    queryset = HotelPackages.objects.all()
    serializer_class = HotelPackageSerializer
    permission_classes = (permissions.AllowAny,)


class HotelPackageDeleteAPIView(DestroyAPIView):
    """Deletes  a hotel package"""
    queryset = HotelPackages.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (IsAdminOrOwner,)


class ItinireryCreateAPIView(CreateAPIView):
    """Create a new itinirery object"""
    queryset = Itinirery.objects.all()
    serializer_class = ItinirerySerializer
    permission_classes = (IsAdminOrOwner,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItinireryListAPIView(ListAPIView):
    """Displays list of itinirery in a package"""
    queryset = Itinirery.objects.all()
    serializer_class = ItinirerySerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """Filter itinirery based on the package"""
        return Itinirery.objects.filter(package=self.kwargs['pk'])


class ItinireryDetailAPIView(RetrieveAPIView):
    """Displays details of Itinirery"""
    queryset = Itinirery.objects.all()
    serializer_class = ItinirerySerializer
    permission_classes = (permissions.AllowAny,)


class ItinireryUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of Itinirery"""
    queryset = Itinirery.objects.all()
    serializer_class = ItinirerySerializer
    permission_classes = (permissions.AllowAny,)


class ItinireryDeleteAPIView(DestroyAPIView):
    """Deletes  Itinirery"""
    queryset = Itinirery.objects.all()
    serializer_class = ItinirerySerializer
    permission_classes = (IsAdminOrOwner,)


class PhotoUploadView(ListCreateAPIView):
    """
    This API view handles multiple images upload form
    It will also display images for specific hotel
    """
    parser_classes = (MultiPartParser, FormParser)
    # http_method_names = ['get', 'post', 'head']

    def get(self, request):
        all_images = Photo.objects.all()
        permission_classes = (IsAdminOrOwner,)
        serializer_class = PhotoSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        hotel = request.data.get('hotel')
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(hotel, img_name)
            file_serializer = PhotoSerializer(data=modified_data)

            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class PhotoListAPIView(ListAPIView):
    """Displays list of photos for a hotel object"""
    queryset = Photo.objects.all().prefetch_related('hotel')
    serializer_class = PhotoSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        return Photo.objects.filter(hotel=self.kwargs['pk'])


class RoomPhotoUploadView(APIView):
    """
    This API view handles multiple images upload form
    It will also display images for specific room
    """
    parser_classes = (MultiPartParser, FormParser)
    # http_method_names = ['get', 'post', 'head']

    def get(self, request):
        all_images = RoomPhoto.objects.all()
        permission_classes = (IsAdminOrOwner,)
        serializer_class = RoomPhotoSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        room = request.data.get('room')
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_room_files(
                room, img_name)
            file_serializer = RoomPhotoSerializer(data=modified_data)

            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class RoomPhotoListAPIView(ListAPIView):
    """Displays list of photos for a room object"""
    queryset = RoomPhoto.objects.all().prefetch_related('room')
    serializer_class = RoomPhotoSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return RoomPhoto.objects.filter(room=self.kwargs['pk'])


class PackagePhotoUploadView(APIView):
    """
    This API view handles multiple images upload form
    It will also display images for specific package
    """
    parser_classes = (MultiPartParser, FormParser)
    # http_method_names = ['get', 'post', 'head']

    def get(self, request):
        all_images = PackagePhoto.objects.all()
        permission_classes = (IsAdminOrOwner,)
        serializer_class = PackagePhotoSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        package = request.data.get('package')
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_package_files(
                package, img_name)
            file_serializer = PackagePhotoSerializer(data=modified_data)

            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class PackagePhotoListAPIView(ListAPIView):
    """Displays list of photos for a package object"""
    queryset = PackagePhoto.objects.all().prefetch_related('package')
    serializer_class = PackagePhotoSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return PackagePhoto.objects.filter(package=self.kwargs['pk'])
