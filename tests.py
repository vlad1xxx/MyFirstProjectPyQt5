import contextlib
from io import StringIO


class PythonExecutor:
    @staticmethod
    def execute(code):
        with StringIO() as output_buffer, contextlib.redirect_stdout(output_buffer):
            try:
                exec(code)
            except Exception as e:
                return f'Error: {e}'
            return output_buffer.getvalue()


def test_createvar_1(part_code):
    code = f'''
{part_code}
print(car)
    '''
    result = PythonExecutor.execute(code)
    if result == 'Porsche\n':
        return True
    return False


def test_createvar_2(part_code):
    code = f'''
{part_code}
    '''
    result = PythonExecutor.execute(code)
    if result == 'Hello, Qt!\n' and 'print(name)':
        return True
    return False


def test_num_1(part_code):
    code = f'''
private = 3
public = 10
total = {part_code}
print('Total posts:')
print(total)
    '''
    result = PythonExecutor.execute(code)
    if result == 'Total posts:\n13\n':
        return True
    return False


def test_loop_1(part_code):
    code = f'''
num = 6
{part_code}
    print(num)
    num = num + 1
    '''
    result = PythonExecutor.execute(code)
    if result == '6\n7\n':
        return True
    return False


def test_loop_2(part_code):
    code = f'''
{part_code}
    print(i)
    '''
    result = PythonExecutor.execute(code)
    if result == '0\n1\n2\n3\n4\n':
        return True
    return False


def test_str_1(part_code, part_code2):
    code = 'animals = {"fox", "cat", "dog"}\n' + f'animals{part_code}\n' + f'animals{part_code2}\n' + 'print(animals)'
    result = PythonExecutor.execute(code)
    print(result)
    if 'crow' in result and 'dog' in result and 'fox' in result:
        return True
    return False
