#!/usr/bin/env python

import picamera
import time
import os
import ConfigParser
from datetime import datetime
import boto3


# Read globals
CONFIG_FILE = 'timelapse.ini'
CONFIG = ConfigParser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE))

TIMELAPSE_IMAGE_DIR = CONFIG.get('global', 'timelapse_image_dir')
# IMGUR_ID = CONFIG.get('global', 'imgur_id')
# IMGUR_TOKEN = CONFIG.get('global', 'imgur_token')
# ACCESS_KEY_ID = CONFIG.get('global', 'Access_Key_ID')
# SECRET_ACCESS_KEY = CONFIG.get('global', 'Secret_Access_Key')

class BioTimeLapse(object):
    def generate_filename(self):
        return '/home/pi/images/diybio_{0}.jpg'.format(datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f"))

    def upload_to_s3(self,file):
        # requires that credentials and region be set via .aws credentials and config files or env vars
        print
        filename = os.path.basename(file)
        s3 = boto3.resource('s3')
        data = open(file, 'rb')
        result=s3.Bucket('familabbiocam').put_object(Key=filename, Body=data, ContentType='image/jpeg')

        # the following resulted in AccessDenied
        # client = boto3.client(
        #     's3',
        #     aws_access_key_id=ACCESS_KEY_ID,
        #     aws_secret_access_key=SECRET_ACCESS_KEY,
        # )
        # transfer = boto3.s3.transfer.S3Transfer(client)
        # transfer.upload_file(file, 'famduino', filename)
        #this also resulted in AccessDenied
        #client.upload_file(file, 'famduino', filename, ExtraArgs={'ContentType': 'image/jpeg'})
        #client.upload_file(file, 'famduino', ExtraArgs={'ContentType': 'image/jpeg'})
        url = '{}/{}'.format('http://familabbiocam.s3-website-us-east-1.amazonaws.com', filename)
        return url

    def start_capture(self, album_hash = '', seconds = 60, cycles = 100):
        for i in range(cycles):
            filename = self.generate_filename()
            with picamera.PiCamera() as camera:
                camera.capture(filename)
            result_url="placeholder_from_start_capture"
            print("You can find it here: {0}".format(result_url['link']))
            time.sleep(seconds)

    def single_capture(self, album_hash = '', seconds = 60, cycles = 100):
        file_name = self.generate_filename()
        with picamera.PiCamera() as camera:
            camera.capture(file_name)
            result_url=self.upload_to_s3(file_name)

        #result_url="placeholder text should be s3 site"
#        print("You can find it here: {0}".format(result_url['link']))
        return result_url

if __name__ == "__main__":
    biocam = BioTimeLapse()
    albumhash='tmp_hash'
    biocam.start_capture(albumhash)
