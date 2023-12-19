class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return f'Тип тренировки: {self.training_type}; ' \
            f'Длительность: {self.duration:.3f} ч.; ' \
            f'Дистанция: {self.distance:.3f} км; ' \
            f'Ср. скорость: {self.speed:.3f} км/ч; ' \
            f'Потрачено ккал: {self.calories:.3f}.'


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOURS_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action,
                 duration,
                 weight) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * self.duration * self.HOURS_IN_MIN)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_COEFF = 0.035
    WEIGHT_COEFF_SECOND = 0.029
    SPEED_MIS = 0.278
    SM_IN_METERS = 100
    # mis = meter in seconds

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.WEIGHT_COEFF * self.weight
                    + (self.SPEED_MIS**2 / self.height * self.SM_IN_METERS)
                    * self.WEIGHT_COEFF_SECOND
                    * self.weight) * self.duration * self.HOURS_IN_MIN)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CONST_SPEED = 1.1
    SPEED_COEFF = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # mis = meter in seconds

        calories = ((self.get_mean_speed() + self.CONST_SPEED)
                    * self.SPEED_COEFF * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_list = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in workout_list.keys():
        if workout_type == 'SWM':
            class_obj = workout_list[workout_type](data[0], data[1],
                                                   data[2], data[3],
                                                   data[4])
        if workout_type == 'RUN':
            class_obj = workout_list[workout_type](data[0], data[1],
                                                   data[2])
        if workout_type == 'WLK':
            class_obj = workout_list[workout_type](data[0], data[1],
                                                   data[2], data[3])
    return class_obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    # Тип тренировки (бег, ходьба или плавание);
    # Длительность тренировки;
    # Дистанция, которую преодолел пользователь, в километрах;
    # Среднюю скорость на дистанции, в км/ч;
    # Расход энергии, в килокалориях.
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
