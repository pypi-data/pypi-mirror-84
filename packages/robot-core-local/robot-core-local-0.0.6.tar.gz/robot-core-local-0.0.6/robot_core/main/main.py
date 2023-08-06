
def boot():
    from robot_core.config import robot_config
    robot_config.start_config("boulder_mobile")

def executor():
    from robot_core.executor import executor_factory
    eye = executor_factory.create_executor("Boulder Mobile", "eye")
    eye.execute(command="start")
    frame = eye.execute(command="capture")


if __name__ == '__main__':
    boot()
    # executor()
