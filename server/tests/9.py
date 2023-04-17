from _assets.Test import Test

import _assets.lib as lib

test = Test()

test.new_task(*lib.generate_task_1_1())
test.new_task(*lib.generate_task_1_2())
test.new_task(*lib.generate_task_1_3())
test.new_task(*lib.generate_task_2_1())
test.new_task(*lib.generate_task_2_2())

test.new_task(*lib.generate_task_3_1())

test.new_task(*lib.generate_task_4_1())

test.new_task(*lib.generate_task_5_1())

test.new_task(*lib.generate_task_6_1())

test.new_task(*lib.generate_task_7_ip(4))

test.new_task(*lib.generate_task_7_file())


print(test)
