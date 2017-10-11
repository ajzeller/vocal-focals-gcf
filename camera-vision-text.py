"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import argparse
import base64
import picamera
import json
import subprocess
import time

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def takephoto():
    camera = picamera.PiCamera()
    camera.resolution = (1600, 1200) # sets camera resolution to 1600 x 1200 px
    camera.capture('image.jpg')

def main():
    start_time = time.time() # begin timer

    takephoto() # First take a picture
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [
                    {
                        'type': 'TEXT_DETECTION',
                        'maxResults': 500
                    },
                    {
                        'type': 'LABEL_DETECTION',
                        'maxResults': 100
                    }
                ]
            }]
        })
        response = service_request.execute()
        # api_response = json.load(response)

        image_text = response["responses"][0]["fullTextAnnotation"]["text"] # parse the text annotations from the image
        image_text = image_text.replace('\n',' ') # remove newlines from text annotations
        image_text = 'I found the following text: ' + image_text
        image_labels = 'This object is most likely ' + response["responses"][0]["labelAnnotations"][0]["description"] + '.'

        finish_time = time.time() # stop timer



        print(image_text)
        print
        print(image_labels)
        print

        elapsed = finish_time - start_time # calculate elapsed time

        elapsed = 'Elapsed time: ' + str(round(elapsed, 3)) + ' seconds.'

        print(elapsed)

        # subprocess.call('echo ' + image_text + ' ' + image_labels + ' |festival --tts', shell=True)

        # print json.dumps(response, indent=4, sort_keys=True)	#Print it out and make it somewhat pretty.

if __name__ == '__main__':

    main()
