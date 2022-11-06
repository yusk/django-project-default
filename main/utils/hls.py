import os
import subprocess

import numpy as np
import cv2


class HLSHelper:
    def playlist(self, duration, seq):
        pl = [
            "#EXTM3U",
            "#EXT-X-VERSION:3",
            f"#EXT-X-TARGETDURATION:{duration}",  # 分割された.tsの中で最大の長さに最も近い整数値
            f"#EXT-X-MEDIA-SEQUENCE:{seq}",  # その.m3u8にかかれている一番最初の.tsが放送全体で何番目の.tsであるか
        ]
        return "\n".join(pl) + "\n"

    def __init__(self, name, basedir, duration, seq):
        filedir = os.path.join(basedir, name)
        os.makedirs(filedir, exist_ok=True)
        m3u8_filepath = os.path.join(filedir, "stream.m3u8")
        if not os.path.exists(m3u8_filepath):
            with open(m3u8_filepath, "w") as f:
                f.write(self.playlist(duration, seq))

        self.name = name
        self.basedir = basedir
        self.filedir = filedir
        self.m3u8_filepath = m3u8_filepath
        self.duration = m3u8_filepath
        self.seq = seq

    def _write_video(self, bytes_list, file_path):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        img_buf = np.frombuffer(bytes_list[0], dtype=np.uint8)
        img = cv2.imdecode(img_buf, cv2.IMREAD_UNCHANGED)
        h = img.shape[0]
        w = img.shape[1]
        fps = len(bytes_list)  # wip

        video = cv2.VideoWriter(file_path, fourcc, fps, (w, h))
        for b in bytes_list:
            img_buf = np.frombuffer(b, dtype=np.uint8)
            img = cv2.imdecode(img_buf, cv2.IMREAD_UNCHANGED)
            video.write(img)
        video.release()

    def _video2ts(self, video_path, ts_path):
        subprocess.run([
            "ffmpeg",
            "-i",
            video_path,
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-bsf:v",
            "h264_mp4toannexb",
            "-f",
            "mpegts",
            "-crf",
            "32",
            ts_path,
        ],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL)

    def write_ts(self, bytes_list):
        filename = f"stream{self.seq:08d}"
        self.seq += 1
        filepath = os.path.join(self.filedir, filename)
        mp4_filepath = filepath + ".mp4"
        ts_filepath = filepath + ".ts"
        self._write_video(bytes_list, mp4_filepath)
        self._video2ts(mp4_filepath, ts_filepath)
        os.remove(mp4_filepath)

        with open(self.m3u8_filepath, "a") as f:
            pl = [
                "#EXTINF:1.0,",
                "#EXT-X-DISCONTINUITY",
                "/static/%s" % os.path.join(self.name, filename + ".ts"),
            ]
            f.write("\n".join(pl) + "\n")
