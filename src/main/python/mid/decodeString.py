import sys

def decodeString(s):
    num_stack = []
    str_stack = []
    cur_num = 0
    cur_str = ""
    for char in s:
        if char.isdigit():
            cur_num = cur_num * 10 + int(char)
        elif char == '[':
            num_stack.append(cur_num)
            str_stack.append(cur_str)
            cur_num = 0
            cur_str = ""
        elif char == ']':
            num = num_stack.pop()
            prev_str = str_stack.pop()
            cur_str = prev_str + cur_str * num
        else:
            cur_str += char
    return cur_str

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(decodeString(line.strip()))
