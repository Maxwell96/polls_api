from .serializers import PollSerializer, VoteSerializer, ChoiceSerializer, UserSerializer
from .models import Poll, Choice
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied


# A list of all polls
class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    # Authenticated users can delete only polls they have created
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You can not delete this poll.')
        return super().destroy(request, *args, **kwargs)


# A detail View for all polls
class PollDetail(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

        # Authenticated users can delete only polls they have created
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You can not delete this poll.')
        return super().destroy(request, *args, **kwargs)


# A list of all choices related to a specific poll
class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    # Only displaying choices associated with a specific poll by filtering with the poll id
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset

    # Authenticated users can create choices only for polls they have created
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You cannot create choice for this poll.')
        return super().post(request, *args, **kwargs)


# A view for voting(creating votes)
class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User account creation
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


# User login
class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
