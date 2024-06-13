# views.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from django.http import HttpResponse

from rest_framework.parsers import MultiPartParser, FormParser

from PIL import Image

import os

import random

from .stegano import encrypt, encode_lsb,decode_lsb,decrypt

# from .steganalysis import process_image # Import your steganalysis function



class FileUploadView(APIView):

  parser_classes = (MultiPartParser, FormParser)



  def post(self, request, *args, **kwargs):

     try:

         text = request.data['text']

         image = request.FILES['image']

         name=request.data['name']

         # print(text,image)

         save_path = '/Users/ch.benerjeereddy/Desktop/testing/{}_original.png'.format(name)

         with open(save_path, 'wb') as f:

              for chunk in image.chunks():

                  f.write(chunk)

         secret_message = encrypt(text)

         # print(secret_message)

         encoded_image_name = name

         randint=random.randint(1,5)

         img=Image.open(save_path)

         for i in range(1,5):

           if i!=randint:

             img.save('/Users/ch.benerjeereddy/Desktop/testing/{}_original{}.png'.format(name,i))

         x= encode_lsb(save_path, secret_message, '/Users/ch.benerjeereddy/Desktop/testing/{}position.txt'.format(encoded_image_name), encoded_image_name,randint)

         if(x=='success'):

            # img = Image.open('/Users/ch.benerjeereddy/Desktop/testing/{}_original.png'.format(name))

            # for a in range(1,5):

            # if a!=randnum:

            # img.save('/Users/ch.benerjeereddy/Desktop/testing/{}_original{}.png'.format(name,a))

              return HttpResponse("Hello")

          

          

         else:

              return HttpResponse("error bro")

     except KeyError as e:

      return HttpResponse("Error: Required data is missing. {}".format(str(e)), status=status.HTTP_400_BAD_REQUEST)

     



class DecryptView(APIView):

  def post(self, request, *args, **kwargs):



    image = request.FILES['image']

    posfile=request.FILES['file']

     

    img_path='/Users/ch.benerjeereddy/Desktop/testing/'+os.path.splitext(image.name)[0]+'.png'

    file_path="/Users/ch.benerjeereddy/Desktop/testing/"+os.path.splitext(posfile.name)[0]+'.txt'

    print(img_path,file_path)

    encrypted_msg=decode_lsb(img_path,file_path)

    print(encrypted_msg)

    if(encrypted_msg=="nobro"):

         return HttpResponse("Sorry unable to reveal your message")

    msg=decrypt(encrypted_msg)

    print(msg)

    # Return decrypted data as JSON response

    return HttpResponse(msg)

