import asyncio
import aiohttp
import urllib.parse
import re
import os
from youtube_transcript_api import YouTubeTranscriptApi

API_KEY = os.getenv("YOUTUBE_API_KEY") or "AIzaSyBejvvt97IB4Cs4Sdd2ce92uM9H-ragVl8"

def iso8601_duration_to_seconds(duration):
    match = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", duration)
    minutes = int(match.group(1)) if match.group(1) else 0
    seconds = int(match.group(2)) if match.group(2) else 0
    return minutes * 60 + seconds

async def fetch_video_details(session, video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={API_KEY}"
    async with session.get(url) as resp:
        data = await resp.json()
        if 'items' in data and data['items']:
            item = data['items'][0]
            return {
                'video_id': video_id,
                'title': item['snippet']['title'],
                'views': int(item['statistics'].get('viewCount', 0)),
                'duration': iso8601_duration_to_seconds(item['contentDetails']['duration']),
                'url': f"https://www.youtube.com/embed/{video_id}"
            }
        return None

async def search_youtube(session, query, max_results=10):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults={max_results}&q={encoded_query}&key={API_KEY}"
    async with session.get(url) as resp:
        data = await resp.json()
        return [item['id']['videoId'] for item in data.get('items', []) if 'videoId' in item['id']]

async def fetch_top_2_videos_async(query: str):
    async with aiohttp.ClientSession() as session:
        video_ids = await search_youtube(session, query, max_results=20)

        tasks = [fetch_video_details(session, vid) for vid in video_ids]
        video_data = await asyncio.gather(*tasks)

        eligible = [v for v in video_data if v and v['duration'] >= 60 and v['views'] >= 10000]
        eligible.sort(key=lambda x: x['views'], reverse=True)
        return eligible[:1]

def fetch_top_2_videos(query: str):
    return asyncio.run(fetch_top_2_videos_async(query))



