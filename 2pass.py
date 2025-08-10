import subprocess
import sys
import os
from pathlib import Path

if len(sys.argv) != 2 or not (f_in := Path(sys.argv[1])).is_file():
    sys.exit(f'usage: python 2pass.py <video.mp4>')

temp = f'{f_in}_video_stream.h264.temp'

try:
    subprocess.run(['ffmpeg', '-i', f_in, '-map', '0:v:0', '-c', 'copy', '-f', 'data', temp], check=True, capture_output=True)
    subprocess.run(['ffmpeg', *(c := ['-y', '-i', f_in, '-c:v', 'libx264', '-b:v', str(8 * (51380224 - f_in.stat().st_size + Path(temp).stat().st_size) / float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', f_in], text=True))), '-passlogfile', f'{f_in}_ffmpeg2pass']), '-pass', '1', '-an', '-f', 'mp4', os.devnull], check=True)
    subprocess.run(['ffmpeg', *c, '-pass', '2', '-c:a', 'aac', f_in.with_name(f"{f_in.stem}_4pass.mp4")], check=True)
except Exception as e:
    sys.exit(f'error: {e}')
finally:
    os.remove(temp)
    for log in Path.cwd().glob(f'{f_in}_ffmpeg2pass*'):
        log.unlink(missing_ok=True)
