from os import getenv
from models.ticket import Ticket

import json
import requests

POST_REQ = ""

class TicketsAPI:
    TOKEN = getenv('YOUTRACK_TOKEN')
    HEADERS = {
            'Accept': 'application/json',
            f'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
    
    def __init__(self):
        pass

    def _get_open_tickets_ids(self) -> list:
        URL = "https://tracker.ntechlab.com/api/sortedIssues"
        ATTRIBS = "?topRoot=100&skipRoot=0&flatten=true&query=state: {Waiting for L2}, {Waiting for developer}, {Waiting for delivery}, {Waiting for customer}, {On hold}, {Waiting for support}&folderId=108-0&fields=tree(id,summaryTextSearchResult(highlightRanges(startOffset,endOffset)))"

        full_url = f"{URL}{ATTRIBS}"
        tickets =  requests.get(full_url, headers=self.HEADERS).json()["tree"]

        formated_dict = []

        for index, ticket in enumerate(tickets):
            formated_dict.append({"id": ticket['id']})

        return formated_dict

    def get_open_tickets_info(self) -> list:
        URL = "https://tracker.ntechlab.com/api/issuesGetter"
        ATTRIBS = "?$top=-1&$skip=0&fields=id,reporter(issueRelatedGroup(@permittedGroups),id,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id)),resolved,updated,created,unauthenticatedReporter,fields(value(id,minutes,presentation,name,description,localizedName,isResolved,color(@color),buildIntegration,buildLink,text,issueRelatedGroup(@permittedGroups),ringId,login,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id),allUsersGroup,icon,teamForProject(name,shortName)),id,$type,hasStateMachine,isUpdatable,projectCustomField($type,id,field(id,name,ordinal,aliases,localizedName,fieldType(id,presentation,isBundleType,valueType,isMultiValue)),bundle(id,$type),canBeEmpty,emptyFieldText,hasRunningJob,ordinal,isSpentTime,isPublic),searchResults(id,textSearchResult(highlightRanges(@textRange),textRange(@textRange))),pausedTime),project(id,ringId,name,shortName,iconUrl,template,pinned,archived,isDemo,organization(),hasArticles,team(@permittedGroups),fieldsSorted,restricted,plugins(timeTrackingSettings(id,enabled),helpDeskSettings(id,enabled,defaultForm(uuid,title)),vcsIntegrationSettings(hasVcsIntegrations),grazie(disabled))),visibility($type,implicitPermittedUsers(@user),permittedGroups(@permittedGroups),permittedUsers(@user)),tags(id,name,color(@color)),votes,voters(hasVote),watchers(hasStar),usersTyping(timestamp,user(@user)),canUndoComment,idReadable,summary;@user:id,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id);@permittedGroups:id,name,ringId,allUsersGroup,icon,teamForProject(name,shortName);@color:id,background,foreground;@textRange:startOffset,endOffset"
        DATA = json.dumps(self._get_open_tickets_ids())

        full_url = f"{URL}{ATTRIBS}"

        tickets = requests.post(url=full_url, data=DATA, headers=self.HEADERS).json()
        
        formated_tickets = []

        for ticket in tickets:
            formated_ticket = Ticket.from_json(ticket)
            formated_tickets.append(formated_ticket)
        
        return formated_tickets

    def get_new_ticket(self) -> list:
        URL = "https://tracker.ntechlab.com/api/issues"
        ATTRIBS = "?fields=idReadable,summary,description&query=project:{Support | Служба поддержки}%20 Assignee: Unassigned State: -Closed, -{Waiting for L2}'"
        full_link = f"{URL}{ATTRIBS}"

        tickets = requests.get(url=full_link, headers=self.HEADERS).json()
        new_tickets = []

        for ticket in tickets:
            print(ticket)
            new_ticket = Ticket.new_ticket(ticket)
            new_tickets.append(new_ticket)
        
        return new_tickets
        