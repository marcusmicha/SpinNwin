from round import Round

class Game:
    def __init__(self, rules: dict,
                 level_config: dict,
                 vip_level: int = 1, 
                 number_of_rounds: int = 1, 
                 round_spins: int = 5) -> None:
        "We initialize all the prerequisites values"
        self.rules = rules
        self.level_config = level_config
        self.vip_level = vip_level
        self.min_reward = self.level_config[self.vip_level]['min']
        self.max_reward = self.level_config[self.vip_level]['max']
        self.number_of_rounds = number_of_rounds
        self.round_spins = round_spins
        self.last_round_free_spin = 0
        self.total_earnings = 0
        self.average_earnings = 0
        self.rewards = []

    def start(self, allow_free_spin = True) -> None:
        "The method that starts the game"
        for present_round in range(self.number_of_rounds):
            round = Round(self.rules, self.level_config, self.vip_level, self.round_spins, allow_free_spin)
            left_spins = self.round_spins
            while left_spins > 0:
                rewards, left_spins = round.spin()
            allow_free_spin = self.check_free_spin_for_next_round(rewards, present_round, allow_free_spin)
            earnings = sum(earning for _, earning in rewards)
            self.total_earnings += earnings
            self.rewards.append(rewards)
        self.average_earnings = self.total_earnings / self.number_of_rounds

    def check_free_spin_for_next_round(self, rewards: list, present_round: int, allow_free_spin: bool) -> bool:
        "rule 8 no Free Spins - 10 consecutive rounds after Free Spin Won"
        if allow_free_spin == False and present_round - self.last_round_free_spin < 10:
            return False

        items = [item[:-2] for item, _ in rewards]
        if 'free_spin' in items:
            self.last_round_free_spin = present_round
            return False
        else:
            return True

    def results(self) -> tuple:
        return self.total_earnings, self.average_earnings, self.rewards, self.min_reward, self.max_reward
