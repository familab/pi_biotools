from timelapse_s3 import BioTimeLapse
import Adafruit_CharLCD as LCD
import tempread
from biodatalogger import Collector
import time
from datetime import datetime


if __name__ == "__main__":
    print "this rug really pulls the room together"
    collector=Collector()
    biocam = BioTimeLapse()
#    album=biocam.create_album()
#    album_url="album url is http://imgur.com/a/{0}".format(album['id'])
    album_url="fake_album_url"
    #print album_url
#    album_hash=album['deletehash']
    lcd = LCD.Adafruit_CharLCDPlate()
    while True:
        lcd.set_color(0.1, 0.0, 0.0)
        lcd.clear()
        lcd.message("taking picture")
        image_url=biocam.single_capture()
        image_url="fake_image_url"
        temp_c, temp_f =tempread.read_temp()
        now = datetime.now()
        data=[now, temp_c, temp_f, album_url, image_url]
        collector.save_console(data)
        collector.save_csv(data)
        #collector.save_thingspeak(data)
        timelapse_start=time.time()
        lcd.set_color(0.0, 0.0, 0.1)
        lcd.clear()
#while time.time() < timelapse_start + 1800:
        while time.time() < timelapse_start + 30:
                print time.time()
                temp_c, temp_f =tempread.read_temp()
                temp_message="{0:3.1f} F {1:3.1f} C\n".format(temp_f, temp_c)
                lcd.message(temp_message)
                date_message=datetime.now().strftime("%H:%M:%S %Y-%m-%d ")
                lcd.message(date_message)
                time.sleep(1)
