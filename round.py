import random
import re
import copy

class Round:
    def __init__(self, rules: dict,
                 level_config: dict,
                 vip_level: int,
                 round_spins: int,
                 allow_free_spin = bool) -> None:
        "We initialize all the prerequisites values"
        self.rules = copy.deepcopy(rules)
        self.level_config = level_config
        if allow_free_spin == False:
            "rule_8 : no Free Spins - 10 consecutive rounds after Free Spin Won"
            self.update_probability('free_spin', 0.0)
        self.items, self.probabilities = self.get_new_probability_distribution()
        self.vip_level = vip_level
        self.round_spins = self.left_spins = round_spins
        self.spins = 0
        self.mandatory_empty = False
        self.rewards = []

    def get_new_probability_distribution(self) -> tuple:
        "Updates items array and probabilities array used for the spin"
        items = []
        probabilities = []
        for item in self.rules:
            items.append(item)
            probabilities.append(self.rules[item]['probability'])
        return items, probabilities

    def spin(self) -> tuple:
        "This method generates a spin an call all the logic rules after each spin"
        if self.left_spins > 0:
            if self.mandatory_empty == True:
                reward = 'empty'
                self.mandatory_empty == False
            else:
                reward = random.choices(self.items, weights=self.probabilities)[0]
            self.rewards.append((reward, self.rules[reward]['value']))
            self.left_spins -= 1
            self.spins += 1
            self.apply_rules()
            self.set_new_probability_distribution()
            self.items, self.probabilities = self.get_new_probability_distribution()
            return self.rewards, self.left_spins
        else:
            return self.rewards, self.left_spins

    def apply_rules(self) -> None:
        "Different rules applied one by one"
        self.rule_2()
        self.rule_3()
        self.rule_4()
        self.rule_5()
        self.rule_6()
        self.rule_7()
        self.free_spin_rule()

    def rule_2(self) -> None:
        "Possible amount of Empty spins (No Reward) - up to 3"
        count_empty = len([reward for reward in self.rewards if reward=='empty'])
        if count_empty == 3:
            self.update_probability('empty', 0.0)
    
    def rule_3(self) -> None:
        "At least 1 spin out of 5 must be EMPTY - No Reward"
        if len(self.rewards) == 4 and len([item for item, _ in self.rewards if item == 'empty']) == 0:
            self.mandatory_empty = True

    def rule_4(self) -> None:
        "MAX 1 Gem Reward per Round (Out of 5 spins up to 1 Gem Reward)"
        gems_items = len([item for item, _ in self.rewards if item.startswith('gems')])
        if gems_items >= 1:
            self.update_probability('gems', 0.0)

    def rule_5(self) -> None:
        "MAX amount of items from the same Reward Type Group - MAX amount of coin items =2, max amount of given eggs = 2"
        rewarded_item_types_list = [i[:3] for i, _ in self.rewards if i != 'empty']
        rewarded_item_types = dict((item ,rewarded_item_types_list.count(item)) for item in set(rewarded_item_types_list))
        for item in rewarded_item_types:
            if rewarded_item_types[item] >= 2:
                self.update_probability(item, 0.0)
    
    def rule_6(self) -> None:
        """
        MAX amount for each item to be double selected per round is 2 (2 hammers, 2 silver eggs)\
        rule_5() already filled the logic for rule_6()
        """
        pass

    def rule_7(self) -> None:
        "MAX amount of ´empty´ slots during ´free spins´ is 1 per round"
        if self.spins > self.round_spins and self.rewards[-1][0] == 'empty':
            self.update_probability('empty', 0.0)


    def free_spin_rule(self) -> None:
        "We add the free spins to the available spins"
        if re.search('free_spin_\d', self.rewards[-1][0]):
            self.left_spins += int(self.rewards[-1][0][-1])
        

    def update_probability(self, item, new_probability) -> None:
        "Updates a specific or a group probability"
        for i in self.rules:
            if i.startswith(item):
                self.rules[i]['probability'] = new_probability

    def set_new_probability_distribution(self) -> None:
        "Determines how the probability shoud be updated based on the target and the present rewards value"
        reward_value = sum([val for _, val in self.rewards])
        if self.spins > self.round_spins:
            target = self.level_config[self.vip_level]['target']
        else:
            target = self.level_config[self.vip_level]['target'] / self.round_spins * self.spins
        
        order = target - reward_value
        self.change_probability_distribution(order)

    def change_probability_distribution(self, order: float) -> None:
        "Updates the probability of the rewards based on the present rewards value compared to the target"
        for i in self.rules:
            prob = self.rules[i]['probability']
            vol = self.rules[i]['volatility']
            val = self.rules[i]['value']
            if order < 0:
                if val <= 0:
                    self.rules[i]['probability'] = prob * (1 + vol)
                if val > 0:
                    self.rules[i]['probability'] = prob * (1 - vol)
            if order > 0:
                if val <= 0:
                    self.rules[i]['probability'] = prob * (1 - vol)
                if val > 0:
                    self.rules[i]['probability'] = prob * (1 + vol)