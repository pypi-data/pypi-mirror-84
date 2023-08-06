from typing import Optional, Tuple, List

from boto3 import Session

from b_delete_cf_stacks.stack import Stack


class GetAllStacks:
    __ALLOWED_STACK_STATUSES = [
        'CREATE_IN_PROGRESS',
        'CREATE_FAILED',
        'CREATE_COMPLETE',
        'ROLLBACK_FAILED',
        'ROLLBACK_COMPLETE',
        'UPDATE_COMPLETE',
        'UPDATE_ROLLBACK_FAILED',
        'UPDATE_ROLLBACK_COMPLETE',
        'IMPORT_COMPLETE',
        'IMPORT_ROLLBACK_FAILED',
        'IMPORT_ROLLBACK_COMPLETE',
    ]

    def __init__(self, boto_session: Session) -> None:
        self.__cf = boto_session.client('cloudformation')

    def get(self) -> List[Stack]:
        stacks, next_token = self.__get()

        while next_token:
            next_stacks, next_token = self.__get(next_token)
            stacks.extend(next_stacks)

        return stacks

    def __get(self, next_token: Optional[str] = None) -> Tuple[List[Stack], Optional[str]]:
        """
        Wrapper function to call boto3 command list_stacks. Returns a list of stack
        names and a next continuation token.

        :param next_token: Next continuation token to fetch next results.

        :return: A tuple consisting of two values:
            1. List of stack names.
            2. Next continuation token.
        """
        kwargs = dict(StackStatusFilter=self.__ALLOWED_STACK_STATUSES)

        if next_token:
            kwargs['NextToken'] = next_token

        response = self.__cf.list_stacks(**kwargs)
        stacks = [Stack(stack) for stack in response['StackSummaries']]
        return stacks, response.get('NextToken')
