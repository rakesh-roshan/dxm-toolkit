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
#
# Copyright (c) 2018 by Delphix. All rights reserved.
#
# Author  : Edward de los Santos
# Author  : Marcin Przepiorowski
# Date    : March 2018


import logging
import sys
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxApplication.DxApplication import DxApplication
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from masking_apis.apis.application_api import ApplicationApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error


class DxApplicationList(object):

    __applicationList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxApplicationList object")

    @classmethod
    def LoadApplications(self):
        """
        Load a list of applications into memory
        return None if OK
        return 1 if not OK
        """

        self.__applicationList.clear()
        try:
            api_instance = ApplicationApi(self.__engine.api_client)
            a = paginator(
                    api_instance,
                    "get_all_applications",
                    _request_timeout=self.__engine.get_timeout())

            if a.response_list:
                for c in a.response_list:
                    application = DxApplication(self.__engine)
                    application.application_name = c.application_name
                    self.__applicationList[c.application_name] = application
            else:
                print_error("No applications found")
                return 1

        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return an Application object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__applicationList[reference]

        except KeyError as e:
            self.__logger.debug("can't find Application object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__applicationList.keys()

    def get_applicationId_by_name(self, name):
        return get_objref_by_val_and_attribute(name, self, 'application_name')

    def add(self, application):
        """
        Add an application to a list and Engine
        :param application: Application object to add to Engine and list
        return None if OK
        """

        if (application.add() is None):
            self.__logger.debug("Adding application %s to list" % application)
            self.__applicationList[application.application_name] = application
            return None
        else:
            return 1
