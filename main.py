import yaml
from pathlib import Path
from game import Game

def main():
    """ Main program """
    rules = yaml.safe_load(Path('config.yml').read_text())
    level_config = yaml.safe_load(Path('level-config.yml').read_text())
    spinwin = Game(rules,level_config, number_of_rounds=100, vip_level=7)
    spinwin.start()
    total, average, rewards, min_reward, max_reward = spinwin.results()
    return 0

if __name__ == "__main__":
    main()