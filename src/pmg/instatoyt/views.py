# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Reel
from .serializers import ReelSerializer
from instaloader import Instaloader, Post

class ReelViewSet(viewsets.ModelViewSet):
    queryset = Reel.objects.all()
    serializer_class = ReelSerializer
    

    def create(self, request, *args, **kwargs):
        # Extract the string parameter from the request data
        reel_id = request.data.get('reel_id', '')
        print(reel_id)
        
        self.downloadReel(reel_id)
        # self.uploadToYT()

        # Create a new instance of Reel with the provided string parameter
        instance = Reel(**request.data)
        instance.save()

        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    def downloadReel(self, SHORTCODE):
        # Get instance
        L = Instaloader()
        # You can perform additional validation or processing here
        post = Post.from_shortcode(L.context, SHORTCODE)
        L.download_post(post, target='current_reel')

        # self.uploadToYT()
