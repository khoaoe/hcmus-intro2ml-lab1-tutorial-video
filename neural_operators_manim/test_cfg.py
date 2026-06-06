from manim import config, tempconfig
with tempconfig({"video_dir": "media/videos/adjusted_scenes"}):
    print(config.video_dir)
