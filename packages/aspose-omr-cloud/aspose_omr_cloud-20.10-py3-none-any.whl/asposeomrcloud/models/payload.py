# coding: utf-8
# """Copyright
# --------------------------------------------------------------------------------------------------------------------
# <copyright company="Aspose" file="payload.py">
# Copyright (c) 2020 Aspose.OMR for Cloud
# </copyright>
# <summary>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# </summary>
# --------------------------------------------------------------------------------------------------------------------
# """

from asposeomrcloud.models import BaseModel


class Payload(BaseModel):
    """
    Attributes:
        model_types (dict):   The key is attribute name
                            and the value is attribute type.
        attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    model_types = {
        'result': 'OmrResponseContent'
    }

    attribute_map = {
        'result': 'result'
    }

    def __init__(self, result=None):

        self._result = None
        self.result = result

    @property
    def result(self):
        """
        Gets the result of this Payload.
        OMR result

        :return: The result of this Payload.
        :type: OmrResponseContent
        """
        return self._result

    @result.setter
    def result(self, result):
        """
        Sets the result of this Payload.
        OMR result
        
        :param result: The result of this Payload.
        :type: OmrResponseContent
        """
        if result is None:
            raise ValueError("Invalid value for `result`, must not be `None`")

        self._result = result