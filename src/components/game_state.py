from enum import Enum

class GameState(Enum):
  MAIN_MENU = 0
  SETTINGS = 1
  GAME = 2

class AsteroidBelt(Enum):
  EASY = "easy"
  MEDIUM = "medium"
  HARD = "hard"

  @staticmethod
  def get_color(state):
    match state:
      case AsteroidBelt.EASY:
        return "green"
      case AsteroidBelt.MEDIUM:
        return "orange"
      case AsteroidBelt.HARD:
        return "red"