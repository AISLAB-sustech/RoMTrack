#!/usr/bin/env python3
"""
将目录下所有*.mp4文件的第一帧截取并保存为*.jpeg
"""

import cv2
import os
from pathlib import Path

def extract_first_frame(video_path, output_path):
    """
    从视频文件中提取第一帧并保存为JPEG
    
    Args:
        video_path: 视频文件路径
        output_path: 输出JPEG文件路径
    
    Returns:
        bool: 成功返回True，失败返回False
    """
    try:
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ 无法打开视频文件: {video_path}")
            return False
        
        # 读取第一帧
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print(f"❌ 无法读取第一帧: {video_path}")
            return False
        
        # 保存为JPEG
        cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"✅ {Path(video_path).name} -> {Path(output_path).name}")
        return True
    
    except Exception as e:
        print(f"❌ 处理失败 {video_path}: {str(e)}")
        return False


def main():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 找出所有mp4文件
    mp4_files = sorted(Path(script_dir).glob("*.mp4"))
    
    if not mp4_files:
        print("⚠️  未找到任何MP4文件")
        return
    
    print(f"📹 找到 {len(mp4_files)} 个MP4文件\n")
    
    success_count = 0
    for video_file in mp4_files:
        # 生成输出文件名 (同名但后缀为.jpeg)
        output_file = video_file.with_suffix(".jpeg")
        
        # 跳过已存在的JPEG文件（可选，删除此行则覆盖）
        if output_file.exists():
            print(f"⏭️  已存在，跳过: {output_file.name}")
            continue
        
        if extract_first_frame(str(video_file), str(output_file)):
            success_count += 1
    
    print(f"\n✨ 完成! 成功处理 {success_count}/{len(mp4_files)} 个文件")


if __name__ == "__main__":
    main()
