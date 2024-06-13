

import numpy as np

from PIL import Image

import random

def encrypt(text):

  key = "zyxwvutsrqponmlkjihgfedcba" 

  substituted_text = substitution_cipher(text, key)

  rev=""

  rev += substituted_text[0:len(substituted_text)//2][::-1]

  rev += substituted_text[len(substituted_text)//2:len(substituted_text)][::-1]

  return rev



def substitution_cipher(text, key):

  cipher_dict = {chr(97 + i): key[i] for i in range(26)}

  keys=['&','*','+','^',"'"]

  j=0

  encrypted_text=""

  for i in text:

    if i==' ':

      encrypted_text+=keys[j%len(keys)]

      j+=1

    else:

      encrypted_text+=i       
  ret_text = ''.join(cipher_dict[char] if char.isalpha() else char for char in encrypted_text.lower())

  return ret_text



def encode_lsb(image_path, secret_message, positions_file,name,post):

  img = Image.open(image_path)

  if img.mode == 'RGBA':

    img = img.convert('RGB')

  width, height = img.size

  pixels = np.array(img)



  secret_binary = ''.join(format(ord(char), '08b') for char in secret_message)



  num_pixels = len(secret_binary)

  pixel_positions = [(random.randint(0, height-1), random.randint(0, width-1)) for _ in range(num_pixels)]



  with open(positions_file, 'w') as file:

    for pos in pixel_positions:

      file.write(','.join(map(str, pos)) + '\n')



  index = 0

  for i, j in pixel_positions:

    if index < len(secret_binary):

      pixel = pixels[i, j]

      pixel = list(pixel)

      pixel[-1] = int(secret_binary[index])

      pixels[i, j] = tuple(pixel)

      index += 1

    else:

      break

  # randnum=random.randint(1,5)

  encoded_img = Image.fromarray(pixels.astype('uint8'))

  encoded_img_path = 'C:/Users/Administrator/Desktop/testing/{}_original{}.png'.format(name,post)

  encoded_img.save(encoded_img_path)

  return "success"



def substitution_decipher(text, key):



  cipher_dict = {key[i]: chr(97 + i) for i in range(26)}

  keys=['&','*','+','^',"'"]



  new_text=""

  for i in text:

     if i in keys:

         new_text+=' '

     else:

         new_text+=i   

  decrypted_text = ''.join(cipher_dict[char] if char.isalpha() else char for char in new_text.lower())

  return decrypted_text

def decrypt(text):

  newrev=""

  newrev+=text[0:len(text)//2][::-1]

  newrev+=text[len(text)//2:len(text)][::-1]

  key = "zyxwvutsrqponmlkjihgfedcba"  

  decrypted_text = substitution_decipher(newrev, key)

   

  return decrypted_text



def bits_to_text(bits):



  n = int(bits, 2)

  return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def decode_lsb(encoded_image_path, positions_file):

  try:

    encoded_img = Image.open(encoded_image_path)

    if encoded_img.mode == 'RGBA':

      encoded_img = encoded_img.convert('RGB')

     

    pixels = np.array(encoded_img)





    with open(positions_file, 'r') as file:

      pixel_positions = [tuple(map(int, line.strip().split(','))) for line in file]



    secret_binary = ''

    for i, j in pixel_positions:

      pixel = pixels[i, j]

      secret_binary += str(pixel[-1])
    secret_message = bits_to_text(secret_binary)

    return secret_message

   

  except Exception as e:

    return "nobro"







