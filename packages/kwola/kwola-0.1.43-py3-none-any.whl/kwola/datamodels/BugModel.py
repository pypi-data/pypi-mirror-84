#
#     Kwola is an AI algorithm that learns how to use other programs
#     automatically so that it can find bugs in them.
#
#     Copyright (C) 2020 Kwola Software Testing Inc.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from .errors.BaseError import BaseError
from .CustomIDField import CustomIDField
from .DiskUtilities import saveObjectToDisk, loadObjectFromDisk
from mongoengine import *
import stringdist

class BugModel(Document):
    id = CustomIDField()

    owner = StringField()

    applicationId = StringField()

    testingStepId = StringField()

    testingRunId = StringField(required=False)

    executionSessionId = StringField()

    creationDate = DateField()

    stepNumber = IntField()

    error = EmbeddedDocumentField(BaseError)

    isMuted = BooleanField(default=False)

    mutedErrorId = StringField(default=None)

    reproductionTraces = ListField(StringField())

    def saveToDisk(self, config, overrideSaveFormat=None, overrideCompression=None):
        saveObjectToDisk(self, "bugs", config, overrideSaveFormat=overrideSaveFormat, overrideCompression=overrideCompression)


    @staticmethod
    def loadFromDisk(id, config, printErrorOnFailure=True):
        return loadObjectFromDisk(BugModel, id, "bugs", config, printErrorOnFailure=printErrorOnFailure)

    def generateBugText(self):
        return self.error.generateErrorDescription()

    def isDuplicateOf(self, otherBug):
        return self.error.isDuplicateOf(otherBug.error) >= 0.80
