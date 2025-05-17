import logging

class Config:
  FPS = 60

  screen_size = (1280, 720)

  @staticmethod
  def increase_FPS():
    logging.info("button")
    fps_sizes = [30, 60, 120, 240]
    current = fps_sizes.index(Config.FPS)
    Config.FPS = fps_sizes[(current + 1) % len(fps_sizes)]