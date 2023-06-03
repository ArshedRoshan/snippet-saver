from django.shortcuts import render
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from . models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError

# Create your views here.
@api_view(['POST'])
def signup(request):
    try:
        if request.method == 'POST':
            serializer = userserilalizer(data=request.data)  #Creates an instance of the userserilalizer serializer with the request data.
            if serializer.is_valid(): #Checks if the serializer data is valid
                serializer.save() # Saves the serializer data to create a new user
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Invalid request method", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


    
@api_view(['GET','POST'])       
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]  
    
    return Response(routes)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, User):
        token = super().get_token(User)

        # Add custom claims
        token['username'] = User.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    



@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_snippet(request):
    try:
        data = request.data
        try:
            tag = Tag.objects.get(title=data['tag_name'])  # Retrieves an existing tag with the given title from the database.
        except Tag.DoesNotExist:  # Handles the exception when the tag with the given title does not exist.
            tag = Tag.objects.create(title=data['tag_name']) # Creates a new tag with the given title.
            
        snippet = Snippet.objects.create(
            title=data['title'],
            content=data['content'],
            created_by=request.user,
            tag=tag
        )            # Creates a new snippet with the provided data, including the retrieved/created tag.

        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def overview(request):
    try:
        snippets = Snippet.objects.all()   #Retrieves all snippets from the database.
        snippet_list = []
        for snippet in snippets:
            snippet_data = {
                'id': snippet.id,
                'title': snippet.title,
                'created_by': snippet.created_by.username,
            }
            snippet_detail_url = reverse('snippet-detail', args=[snippet.id], request=request)
            snippet_data['detail_url'] = snippet_detail_url
            snippet_list.append(snippet_data)

        data = {
            'snippet_count': len(snippet_list),
            'snippets': snippet_list,
        }
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)  #Retrieves the snippet with the given pk from the database.
        serializer = SnippetSerializer(snippet)  # Initializes the serializer with the retrieved snippet.
        return Response(serializer.data)
    except Snippet.DoesNotExist:
        return Response({"error": "Snippet not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def update_snippet(request,pk):
    data = request.data
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=404)
    tag_name = data.get('tag_name', None)  #Extracts the tag name from the request data.
    if tag_name:
        try:
            tag = Tag.objects.get(title=tag_name)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(title=tag_name)
        snippet.tag = tag
    serializer = SnippetSerializer(snippet,data=data,partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_snippet(request,pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=404)
    snippet.delete()
    
    remaining_snippets = Snippet.objects.all()
    serializer = SnippetSerializer(remaining_snippets,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tags(request):
    try:
        tags = Tag.objects.all()
        serializer = Tagserializer(tags, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def snippet_tag(request,pk):
    try:
        snippets = Snippet.objects.filter(tag=pk) #Retrieves the snippets associated with the given tag ID from the database.
        if not snippets.exists():    # Checks if any snippets exist with the given tag ID.
            return Response({"error": "No snippets found with the given tag ID"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
    
    
        
    
    
    


            