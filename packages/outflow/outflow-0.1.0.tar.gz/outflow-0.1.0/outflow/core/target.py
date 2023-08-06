# -*- coding: utf-8 -*-
class Target:
    @classmethod
    def output(cls, identifier, *args, **kwargs):
        """
        Define a new output target for a given class

        :param identifier: the target identifier
        :return: the class wrapper
        """

        def wrapper(TaskClass):
            TaskClass.add_output(
                target_class=cls, identifier=identifier, *args, **kwargs
            )
            return TaskClass

        return wrapper

    @classmethod
    def input(cls, identifier, *args, **kwargs):
        """
        Define a new input target for a given class

        :param identifier: the target identifier
        :return: the class wrapper
        """

        def wrapper(TaskClass):
            TaskClass.add_input(
                target_class=cls, identifier=identifier, *args, **kwargs
            )
            return TaskClass

        return wrapper

    @classmethod
    def parameter(cls, identifier, *args, **kwargs):
        """
        Define a new input parameter for a given class

        :param identifier: the target identifier
        :return: the class wrapper
        """

        def wrapper(TaskClass):
            TaskClass.add_parameter(
                target_class=cls, identifier=identifier, *args, **kwargs
            )
            return TaskClass

        return wrapper

    @classmethod
    def parameters(cls, *identifiers):
        """
        Define a list of input parameters for a given class

        :param identifiers: the target identifiers
        :return: the class wrapper
        """

        def wrapper(TaskClass):
            for identifier in identifiers:
                TaskClass.add_parameter(target_class=cls, identifier=identifier)
            return TaskClass

        return wrapper
