import boto3

from b_delete_cf_stacks.delete_stacks import DeleteStacks
from b_delete_cf_stacks.get_all_stacks import GetAllStacks


def main() -> None:
    """
    Command that deletes all AWS CloudFormation stacks in a specified account.

    :return: No return.
    """
    profile = input('Name of the AWS profile: ')
    region = input('AWS region: ')
    ans = input('Are you absolutely sure you want to delete all stacks? [y/n]: ')

    if ans == 'y':
        boto_session = boto3.session.Session(
            profile_name=profile,
            region_name=region
        )

        try:
            DeleteStacks(boto_session=boto_session).execute()
        except RecursionError:
            stacks = GetAllStacks(boto_session).get()
            stacks_readable = '\n'.join([stack.stack_name for stack in stacks])

            print(f'Script finished execution. Stacks that were not deleted:\n{stacks_readable}.')
