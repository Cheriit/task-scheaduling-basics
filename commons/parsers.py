from typing import List

from commons import RSTask, SwitchTimes, Task, RWTask


def exit_error(parameters: str):
    print(parameters)
    exit(0)


def parser_function(parser_fn):
    def parse(input_string):
        try:
            task_parameters = parse_input_string(input_string)
            return parser_fn(task_parameters)
        # except ValueError:
        #     print('Cannot parse given string to integer')
        #     exit_error(input_string)
        except IndexError:
            print('File has an incorrect format')
            exit_error(input_string)

    return parse


@parser_function
def parse_task(task_parameters: str) -> Task:
    return Task(int(float(task_parameters[0])))


@parser_function
def parse_rs_task(task_parameters: str) -> RSTask:
    return RSTask(int(float(task_parameters[1])), int(float(task_parameters[0])), int(float(task_parameters[2])))


@parser_function
def parse_rw_task(task_parameters: str) -> RWTask:
    return RWTask(
        int(float(task_parameters[1])),
        int(float(task_parameters[0])),
        int(float(task_parameters[2])),
        int(float(task_parameters[3])))


@parser_function
def parse_switch_times(switch_times: str) -> SwitchTimes:
    int_times = list(map(lambda x: int(float(x)), switch_times))
    return SwitchTimes(int_times)


def parse_input_string(string: str) -> List[str]:
    return list(filter(None, string.replace('\n', '').strip().split(' ')))
