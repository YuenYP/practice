# Copyright [2023] [copyright of Yuen Chang]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
class task:

    def __init__(self, items):
        self.id = int(items[0])
        self.priority = int(items[1])
        self.runtime = int(items[2])
        self.arv_time = int(items[3])

if __name__ == '__main__':
    file = open('priority', 'r')
    task_list = []
    wait_list = {}
    is_execute = 0
    execute_task_id = None
    key_number = []

    # not execute
    entire_life_span = 0
    glb_clk_counter = 0
    complete_task_cnt = 0

    for l in file:
        items = l.split(" ")
        local_task = task(items)
        task_list.append(local_task)
        wait_list[local_task.priority] = []

    key_bundle_list = sorted(wait_list.items(), key=lambda d:d[0], reverse=True)
    for i_key_bundle in key_bundle_list:
        key_number.append(i_key_bundle[0])
    # print(task_list)
    total_tasks_cnt = task_list.__len__()

    glb_clk_counter = task_list[0].arv_time
    entire_life_span = task_list[0].arv_time + task_list[0].runtime
    is_execute = 1
    executing_task_id = task_list[0].id
    executing_task_done_time = task_list[0].arv_time + task_list[0].runtime
    task_list.pop(0)


    while complete_task_cnt < total_tasks_cnt:

        if is_execute == 1: # 在忙的时候，要注意任务排序
            # 轮询一下有那些任务可以上线，压任务
            if glb_clk_counter == executing_task_done_time:
                print("The task is done. The task id is " + str(executing_task_id))
                print("The done time is " + str(executing_task_done_time))
                is_execute = 0
                complete_task_cnt += 1
        elif is_execute == 0: # 不忙的时候，开始排任务
            # 上任务，找出优先级最高的
            for prior_i in key_number:
                if wait_list[prior_i].__len__():
                    # pass
                    executing_task_done_time = glb_clk_counter + wait_list[prior_i][0].runtime - 1
                    executing_task_id = wait_list[prior_i][0].id
                    is_execute = 1
                    wait_list[prior_i].pop(0)
                    break
        else:
            print("Error!!!")

        # 任务查询和排任务到任务队列, 轮询一下有那些任务可以上线，压任务
        for i in range(task_list.__len__()):
            # print(glb_clk_counter)
            if glb_clk_counter == task_list[i].arv_time:
                wait_list[task_list[i].priority].append(task_list[i])

        glb_clk_counter += 1
