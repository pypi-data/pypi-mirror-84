from typing import Any, Dict, Union, TypeVar

from spark_auto_mapper.data_types.amount import AutoMapperAmountDataType
from spark_auto_mapper.data_types.boolean import AutoMapperBooleanDataType
from spark_auto_mapper.data_types.column import AutoMapperDataTypeColumn
from spark_auto_mapper.data_types.complex.complex import AutoMapperDataTypeComplex
from spark_auto_mapper.data_types.concat import AutoMapperConcatDataType
from spark_auto_mapper.data_types.data_type_base import AutoMapperDataTypeBase
from spark_auto_mapper.data_types.date import AutoMapperDateDataType
from spark_auto_mapper.data_types.expression import AutoMapperDataTypeExpression
from spark_auto_mapper.data_types.if_not_null import AutoMapperIfNotNullDataType
from spark_auto_mapper.data_types.literal import AutoMapperDataTypeLiteral
from spark_auto_mapper.data_types.number import AutoMapperNumberDataType
from spark_auto_mapper.data_types.complex.struct import AutoMapperDataTypeStruct
from spark_auto_mapper.type_definitions.defined_types import AutoMapperAnyDataType, AutoMapperBooleanInputType, \
    AutoMapperAmountInputType, AutoMapperNumberInputType, AutoMapperDateInputType
from spark_auto_mapper.type_definitions.native_types import AutoMapperNativeTextType, AutoMapperNativeSimpleType
from spark_auto_mapper.type_definitions.wrapper_types import AutoMapperWrapperType


class AutoMapperHelpers:
    @staticmethod
    def struct(value: Dict[str, Any]) -> AutoMapperDataTypeStruct:
        """
        Creates a struct
        :param value: A dictionary to be converted to a struct
        :return: A struct automapper type
        """
        return AutoMapperDataTypeStruct(value=value)

    @staticmethod
    def complex(**kwargs: AutoMapperAnyDataType) -> AutoMapperDataTypeComplex:
        """
        Creates a complex type.
        :param kwargs: parameters to be used to create the complex type
        :return: A complex automapper type
        """
        return AutoMapperDataTypeComplex(**kwargs)

    @staticmethod
    def column(value: str) -> AutoMapperDataTypeColumn:
        """
        Specifies that the value parameter should be used as a column name
        :param value: name of column
        :return: A column automapper type
        """
        return AutoMapperDataTypeColumn(value)

    @staticmethod
    def text(value: str) -> AutoMapperDataTypeLiteral:
        """
        Specifies that the value parameter should be used as a literal text
        :param value: literal text value
        :return: a literal automapper type
        """
        return AutoMapperDataTypeLiteral(value)

    @staticmethod
    def expression(value: str) -> AutoMapperDataTypeExpression:
        """
        Specifies that the value parameter should be executed as a sql expression in Spark
        :param value: sql
        :return: an expression automapper type
        """
        return AutoMapperDataTypeExpression(value)

    @staticmethod
    def date(value: AutoMapperDateInputType) -> AutoMapperDateDataType:
        """
        Specifies that value should be parsed into a date.  We currently support the following formats:
        yyyy-MM-dd
        yyyyMMdd
        MM/dd/yy
        (For adding more, go to AutoMapperDateDataType)
        :param value: text
        :return: a date automapper type
        """
        return AutoMapperDateDataType(value)

    @staticmethod
    def amount(value: AutoMapperAmountInputType) -> AutoMapperAmountDataType:
        """
        Specifies the value should be used as an amount
        :param value:
        :return: an amount automapper type
        """
        return AutoMapperAmountDataType(value)

    @staticmethod
    def boolean(
        value: AutoMapperBooleanInputType
    ) -> AutoMapperBooleanDataType:
        """
        Specifies the value should be used as a boolean
        :param value:
        :return: a boolean automapper type
        """
        return AutoMapperBooleanDataType(value)

    @staticmethod
    def number(value: AutoMapperNumberInputType) -> AutoMapperNumberDataType:
        """
        Specifies value should be used as a number
        :param value:
        :return: a number automapper type
        """
        return AutoMapperNumberDataType(value)

    @staticmethod
    def concat(
        *args: Union[AutoMapperNativeTextType, AutoMapperWrapperType]
    ) -> AutoMapperConcatDataType:
        """
        concatenates a list of values.  Each value can be a string or a column
        :param args: string or column
        :return: a concat automapper type
        """
        return AutoMapperConcatDataType(*args)

    _T = TypeVar(
        "_T", bound=Union[AutoMapperNativeSimpleType, AutoMapperDataTypeBase]
    )

    @staticmethod
    def if_not_null(check: AutoMapperDataTypeColumn,
                    value: _T) -> AutoMapperIfNotNullDataType[_T]:
        """
        concatenates a list of values.  Each value can be a string or a column


        :param check: column to check for null
        :param value: what to return if the value is not null
        :return: an if_not_null automapper type
        """
        return AutoMapperIfNotNullDataType(check=check, value=value)
