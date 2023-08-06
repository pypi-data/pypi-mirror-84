from functools import lru_cache

from aws_cdk.aws_iam import PolicyStatement, ServicePrincipal
from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack


class StageDeploymentSingletonFunction(SingletonFunction):
    """
    Custom api gateway stage deployment resource singleton lambda function.
    """

    def __init__(
            self,
            scope: Stack,
            name: str
    ) -> None:
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid=f'{name}-uuid',
            function_name=name,
            code=self.__code(),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_8,
        )

        # Add permission to create deployments. Since this is a singleton lambda function,
        # we can not specify a specific api gateway resource.
        self.add_to_role_policy(PolicyStatement(
            actions=['apigateway:POST', 'apigateway:PATCH'],
            resources=['*']
        ))

    @lru_cache
    def __code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self):
        return self.__name
