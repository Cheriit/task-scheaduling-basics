from typing import List

from commons import RSTask, SwitchTimes, Task


def exit_error(parameters: str):
    print(parameters)
    exit(0)


def parser_function(parser_fn):
    def parse(input_string):
        try:
            task_parameters = parse_input_string(input_string)
            return parser_fn(task_parameters)
        except ValueError:
            print('Cannot parse given string to integer')
            exit_error(input_string)
        except IndexError:
            print('File has an incorrect format')
            exit_error(input_string)

    return parse


@parser_function
def parse_task(task_parameters: List[str]) -> Task:
    return Task(int(task_parameters[0]))


@parser_function
def parse_rs_task(task_parameters: List[str]) -> RSTask:
    return RSTask(int(task_parameters[1]), int(task_parameters[0]), int(task_parameters[2]))


@parser_function
def parse_switch_times(switch_times: List[str]) -> SwitchTimes:
    int_times = list(map(lambda x: int(x), switch_times))
    return SwitchTimes(int_times)


def parse_input_string(string: str) -> List[str]:
    return string.replace('\n', '').strip().split(' ')
