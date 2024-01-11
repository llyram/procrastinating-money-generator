# views.py
import os
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Reel
from .serializers import ReelSerializer
from instaloader import Instaloader, Post
import shutil
from .uploadtoyt import upload_youtube_video

class ReelViewSet(viewsets.ModelViewSet):
    queryset = Reel.objects.all()
    serializer_class = ReelSerializer
    

    def create(self, request, *args, **kwargs):
        # Extract the string parameter from the request data
        reel_id = request.data.get('reel_id', '')
        print(reel_id)


        # os.chdir('instatoyt')
        # print(os.getcwd())

        # Delete the entire folder
        try:
            shutil.rmtree('current_reel')
            print(f"The folder current_reel has been deleted.")
        except Exception as e:
            print(f"Failed to delete the folder current_reel. Reason: {e}")
        self.downloadReel(reel_id)

        # # Path to the directory containing MP4 files
        # target_dir = "current_reel"

        # # Get a list of all files in the directory
        # all_files = os.listdir(target_dir)

        file_path = "current_reel/reels.mp4"
        title_path = "current_reel/reels.txt"
        title = None
        description = None
        if os.path.isfile(title_path):
            try:
                with open(title_path, 'r') as file:
                    title = file.readline()
                    description = file.read()
                    print(f"The first line of the file is: {title}")
            except FileNotFoundError:
                print(f"Error: File '{title_path}' not found.")
            except IOError as e:
                print(f"Error reading the file: {e}")

        # title = "My Uploaded Video 2"
        category = "22"
        keywords = "keyword1,keyword2"
        privacy_status = "private"
        try:
            upload_youtube_video(file_path, title, description, category, keywords, privacy_status)
        except Exception as e:
            print(f"File could not be uploaded\n\n {e}")

        # Create a new instance of Reel with the provided string parameter
        instance = Reel(**request.data)
        instance.save()

        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    def downloadReel(self, SHORTCODE):
        # Get instance
        L = Instaloader(filename_pattern="reels")
        # You can perform additional validation or processing here
        post = Post.from_shortcode(L.context, SHORTCODE)
        L.download_post(post, target='current_reel')
