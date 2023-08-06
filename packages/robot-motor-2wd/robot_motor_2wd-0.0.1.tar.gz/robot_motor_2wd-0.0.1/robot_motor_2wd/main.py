from robot_motor_2wd import executor

if __name__ == '__main__':
    executor.Motor2wdExecutor().start_forward()

    import time
    time.sleep(1)

    executor.Motor2wdExecutor().stop()
