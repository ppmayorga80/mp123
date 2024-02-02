# Copyright (c) 2021-present Divinia, Inc.logger
import time

import pyperclip


def main():
    recent_value = ""
    while True:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            transformed_value = ",".join([x.strip() for x in recent_value.split("\n")])
            print(f"COPY -> {transformed_value}")
            pyperclip.copy(transformed_value)

        time.sleep(0.1)


if __name__ == '__main__':
    main()
