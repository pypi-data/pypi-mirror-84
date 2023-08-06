import time
from typing import List, Optional
from boto3 import Session

from b_delete_cf_stacks.get_all_stacks import GetAllStacks
from b_delete_cf_stacks.stack import Stack


class DeleteStacks:
    __DELETION_INTERVAL = 60

    def __init__(self, boto_session: Session):
        self.__boto_session = boto_session

    def execute(self) -> None:
        self.__execute()

    def __execute(
            self,
            previous_stacks: Optional[List[Stack]] = None,
            same_stacks_iteration: int = 0,
            max_same_stacks_iterations: int = 10
    ) -> None:
        if same_stacks_iteration == max_same_stacks_iterations:
            raise RecursionError('Max iterations reached. Existing script...')

        stacks = GetAllStacks(self.__boto_session).get() or []
        previous_stacks = previous_stacks or []

        if len(previous_stacks) == len(stacks):
            same_stacks_iteration += 1
            print(f'Previous stacks and current stacks are the same. Iteration: {same_stacks_iteration}.')
        else:
            same_stacks_iteration = 0
            print(f'Previous stacks len and current stacks len are different.')

        if stacks:
            self.__delete_stacks(stacks)
            print(f'Sleeping for {self.__DELETION_INTERVAL} seconds...')
            time.sleep(self.__DELETION_INTERVAL)
            self.__execute(stacks, same_stacks_iteration, max_same_stacks_iterations)
        else:
            print('No more stacks to delete.')

    def __delete_stacks(self, stacks: List[Stack]) -> None:
        for stack in stacks:
            print(f'Deleting stack: {stack}...')
            self.__boto_session.client('cloudformation').delete_stack(StackName=stack.stack_name)
