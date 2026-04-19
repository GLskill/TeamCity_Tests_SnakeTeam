# Единая точка входа для всех стэпов ( AdminSteps, UserSteps )


class ApiManager:
    def __init__(self, created_objects: list):
        self.admin_steps = AdminSteps(created_objects)
        self.user_steps = UserSteps(created_objects)
        self.deposit_steps = DepositSteps(created_objects)

