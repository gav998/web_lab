from _assets.Test import Test

import _assets.lib as lib

test = Test()

test.new_task(*lib.generate_task_1_1())
test.new_task(*lib.generate_task_1_2())
test.new_task(*lib.generate_task_1_3())
test.new_task(*lib.generate_task_2_1())

print(test)
