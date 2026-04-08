class RenovationEnv:
    def init(self):
        self.reset()

    def reset(self, task=None):
        # Default values
        self.state_data = {
            "budget": 50000,
            "style": "modern",
            "items_selected": []
        }

        # Apply task overrides
        if task:
            self.state_data["budget"] = task.get("budget", 50000)
            self.state_data["style"] = task.get("style", "modern")

        self.done = False
        return self.state()

    def state(self):
        return self.state_data

    def step(self, action):
        reward = 0.0
        error = None

        ITEM_COST = {
            "chair": 5000,
            "table": 10000,
            "paint": 7000,
            "light": 3000
        }

        STYLE_MATCH = {
            "modern": ["chair", "table", "light"],
            "classic": ["paint"]
        }

        try:
            item = action

            if item not in ITEM_COST:
                reward = -0.5
                error = "invalid_item"
            else:
                cost = ITEM_COST[item]

                if self.state_data["budget"] < cost:
                    reward = -1.0
                    error = "budget_exceeded"
                else:
                    self.state_data["items_selected"].append(item)
                    self.state_data["budget"] -= cost

                    if item in STYLE_MATCH[self.state_data["style"]]:
                        reward = 0.8
                    else:
                        reward = 0.3

        except:
            reward = -0.5
            error = "invalid_action"

        if self.state_data["budget"] <= 0 or len(self.state_data["items_selected"]) >= 5:
            self.done = True

        return self.state(), reward, self.done, {"error": error}