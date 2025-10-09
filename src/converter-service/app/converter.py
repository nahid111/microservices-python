import json
import os
import tempfile

import gridfs
from moviepy import VideoFileClip
from bson.objectid import ObjectId
from pymongo import MongoClient

from app.config import settings
from app.publisher import rabbitmq_publisher
from app import logger

client = MongoClient(settings.MONGODB_URL)
gfs_bucket = gridfs.GridFS(client.videos)
gfs_bucket_mp3 = gridfs.GridFS(client.mp3s)


def convert(message):
    try:
        message = json.loads(message)

        # Empty temp file
        with tempfile.NamedTemporaryFile() as tf:
            file_id = ObjectId(message["video_fid"])

            # Get video content
            try:
                video_data = gfs_bucket.get(file_id)
            except Exception as err:
                logger.error(f"Failed to download the video, {err}")
                return "Failed to download the video"

            # Add video contents to empty file
            tf.write(video_data.read())
            # Create audio from temp video file
            audio = VideoFileClip(tf.name).audio

            # Create a temporary MP3 file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf_mp3:
                tf_mp3_path = tf_mp3.name
                audio.write_audiofile(tf_mp3_path)
            # write audio to the file
            tf_mp3_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
            audio.write_audiofile(tf_mp3_path)

            # Save file to MongoDB GridFS
            try:

                with open(tf_mp3_path, "rb") as f:
                    data = f.read()
                    fid = gfs_bucket_mp3.put(data)
            except Exception as err:
                logger.error(f"Failed to upload the mp3, {err}")
                return "Failed to upload the mp3"

            # Remove the temporary MP3 file
            os.remove(tf_mp3_path)

            message["mp3_fid"] = str(fid)

            try:
                rabbitmq_publisher.publish(message)
            except Exception as err:
                logger.error(f"Failed to publish message, {err}")
                gfs_bucket_mp3.delete(fid)
                return "Failed to publish message"

    except Exception as err:
        logger.error(f"An error occurred during conversion, {err}")
        return "An error occurred during conversion"
