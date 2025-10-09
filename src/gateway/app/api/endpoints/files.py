from bson import ObjectId
from fastapi import HTTPException, APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse
from gridfs.errors import NoFile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.api.deps import require_token
from app.api.publisher import rabbitmq_publisher
from app.core.config import settings

router = APIRouter()

client = AsyncIOMotorClient(settings.MONGODB_URL)
gfs_bucket = AsyncIOMotorGridFSBucket(client.videos)
gfs_bucket_mp3 = AsyncIOMotorGridFSBucket(client.mp3s)


@router.post("/")
async def upload_video(video: UploadFile, token: dict[str, str] = Depends(require_token)):
    # Upload the video
    try:
        async with gfs_bucket.open_upload_stream(filename=video.filename) as upload_stream:
            await upload_stream.write(video.file.read())
            file_id = upload_stream._id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="File upload failed")

    # Publish Message to the Topic
    try:
        rabbitmq_publisher.publish({
            "video_fid": str(file_id),
            "mp3_fid": None,
            "email": token["email"],
        })
    except Exception as e:
        print(e)
        # delete if publishing fails
        await gfs_bucket.delete(ObjectId(file_id))
        raise HTTPException(status_code=500, detail="Publishing failed")

    return {"file_id": str(file_id), "filename": video.filename}


@router.get("/{file_id}")
async def download_video(file_id: str):
    temp_file_path = f"/tmp/{file_id}.mp3"
    try:
        grid_out = await gfs_bucket_mp3.open_download_stream(ObjectId(file_id))
        # Create a temporary file to write the content
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await grid_out.read())
        return FileResponse(temp_file_path, filename=f"{file_id}.mp3")
    except NoFile:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)
