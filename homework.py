class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Выводит сообщение в соотвествии с типом тренировки"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Длинна шага в метрах
    M_IN_KM: int = 1000  # Константа для перевода метров в км
    H_IN_MIN: int = 60  # Константа для перевода часов в минуты

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод реализуется в дочерних классах')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # Множитель скорости
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # Константа для учета сдвига скорости

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        duration_m = self.duration * self.H_IN_MIN
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * duration_m)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035  # Коэффициент расчета каллорий 1
    SQRT_SPEED_AND_HEIGHT = 0.029  # Коэффициент расчета каллорий 2
    SPEED_IN_M_SEC = 0.278  # Константа для перевода скорости в м/с
    SM_IN_METERS = 100  # Константа для перевода см в м

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        speed_m_in_sec = speed * self.SPEED_IN_M_SEC
        height_m = self.height / self.SM_IN_METERS
        duration_m = self.duration * self.H_IN_MIN
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                 + (speed_m_in_sec**2 / height_m)
                 * self.SQRT_SPEED_AND_HEIGHT * self.weight) * duration_m)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Длинна шага в метрах
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1  # Коэффициент учета сдвига скорости
    DOUBLE_MEAN_SPEED: int = 2  # Коэффициент для удвоения скорости

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool   # в метрах
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.DOUBLE_MEAN_SPEED * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking}

    if workout_type in trainings:
        return trainings[workout_type](*data)

    raise ValueError('Тренировка не найдена.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
