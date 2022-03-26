from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import cv2

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = os.environ['SUBSCRIPTION_KEY'] # Credential
endpoint = os.environ['END_POINT'] # Credential

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Image path
image_path = os.path.join ("static_image", "temporary_captured.jpg")

# Interval to take photos
interval = 10

'''
Get image from webcam
'''
# Choose webcam device
cam_port = 0
cam = cv2.VideoCapture(cam_port)

def capture_image():
    # Take a photo
    # reading the input using the camera
    result, image = cam.read()
    
    # If image will detected without any error, save result
    if result:
        # saving image in local temporary storage
        cv2.imwrite(image_path, image)
        print("New Image Captured!")

'''
End - get image from webcam
'''

'''
OCR: Read File using the Read API, extract text from image
'''

def ocer_from_webcam():
    # Read image from local storage
    read_image = open(image_path, "rb")

    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(read_image, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print ('Waiting for result...\n')
        time.sleep(5)

    # Check for any other errors
    if read_result.status.lower () == 'failed':
        print ('API call failed')
        print (f'Error: {read_result.message}')
    # Check if succeded
    elif read_result.status == OperationStatusCodes.succeeded:
        # Check if there are any lines of text
        if len(read_result.analyze_result.read_results[0].lines) == 0:
            print("Nothing were found!, try again...")
        else:
            for text_result in read_result.analyze_result.read_results:
                # Print results, line by line
                for idx, line in enumerate(text_result.lines):
                    text = line.text
                    print(f'Line - {idx+1}: "{text}"')
                    #print(line.bounding_box)
                
    print("\n")

'''
END - Read File - from local temporary storage
'''

'''
For loop of continuous capture and OCR for 10 seconds interval
'''

while True:
    capture_image()
    time.sleep(1)
    ocer_from_webcam()
    time.sleep(interval)

'''
End - For loop 
'''


