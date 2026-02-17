from os import getenv
from common.models.ticket import Ticket

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

    def send_to_spam(self, ticket_id):
        URL = f"https://tracker.ntechlab.com/api/issues/{ticket_id}"
        ATTRIBS = "?fields=description,updater(%40reporter),creator(%40reporter),attachments(%40attachments),mentionedUsers(%40reporter),mentionedIssues(%40mentionedIssues),mentionedArticles(%40mentionedArticles),workItems(id,author(%40user),creator(%40user),text,type(%40value),duration(minutes,presentation),textPreview,created,updated,date,usesMarkdown,attributes(id,name,value(%40value))),usesMarkdown,hasEmail,wikifiedDescription,messages,tags(id,name,color(%40color),query,issuesUrl,isDeletable,isShareable,isUpdatable,isUsable,pinnedByDefault,untagOnResolve,owner(%40user),readSharingSettings(%40updateSharingSettings),tagSharingSettings(%40updateSharingSettings),updateSharingSettings(%40updateSharingSettings)),pinnedComments(author(%40user),id,text,textPreview,deleted,pinned,visibility(%40visibility),attachments(%40attachments),mentionedUsers(%40reporter),mentionedIssues(%40mentionedIssues),mentionedArticles(%40mentionedArticles),reactions(id,reaction,author(%40user)),reactionOrder,usesMarkdown,hasEmail,canUpdateVisibility,suspiciousEmail,created,updated,issue(id,project(id)),markdownEmbeddings(%40markdownEmbeddings)),canUpdateVisibility,canAddPublicComment,widgets(id,key,appId,description,appName,name,collapsed,indexPath,extensionPoint(),iconPath,appIconPath,expectedHeight,expectedWidth),externalIssue(key,name,url),summaryTextSearchResult(%40textSearchResult),descriptionTextSearchResult(%40textSearchResult),channel($type,id,name,mailboxRule(id)),id,reporter(%40reporter),resolved,updated,created,unauthenticatedReporter,fields(%40fields),project(%40project),visibility(%40visibility),votes,voters(hasVote),watchers(hasStar),usersTyping(%40usersTyping),canUndoComment,idReadable,summary,markdownEmbeddings(%40markdownEmbeddings)%3B%40mentionedIssues%3Aid,reporter(%40reporter),resolved,updated,created,unauthenticatedReporter,fields(%40fields),project(%40project),visibility(%40visibility),tags(%40tags),votes,voters(hasVote),watchers(hasStar),usersTyping(%40usersTyping),canUndoComment,idReadable,summary%3B%40attachments%3Aid,name,author(ringId,avatarUrl,canReadProfile,isLocked,login,name),created,updated,mimeType,url,size,visibility(%40visibility),imageDimensions(width,height),thumbnailURL,recognizedText,searchResults(textSearchResult(highlightRanges(%40textRange))),comment(id,visibility(%40visibility)),embeddedIntoDocument(id),embeddedIntoComments(id)%3B%40mentionedArticles%3Aid,idReadable,reporter(%40user),summary,project(%40project),parentArticle(idReadable),ordinal,visibility(%40visibility),hasUnpublishedChanges,hasChildren,tags(%40tags)%3B%40fields%3Avalue(id,minutes,presentation,name,description,localizedName,isResolved,color(%40color),buildIntegration,buildLink,text,issueRelatedGroup(%40permittedGroups),ringId,login,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id),allUsersGroup,icon,teamForProject(name,shortName)),id,$type,hasStateMachine,isUpdatable,projectCustomField($type,id,field(id,name,ordinal,aliases,localizedName,fieldType(id,presentation,isBundleType,valueType,isMultiValue)),bundle(id,$type),canBeEmpty,emptyFieldText,hasRunningJob,ordinal,isSpentTime,isPublic),searchResults(id,textSearchResult(%40textSearchResult)),pausedTime%3B%40visibility%3A$type,implicitPermittedUsers(%40user),permittedGroups(%40permittedGroups),permittedUsers(%40user)%3B%40project%3Aid,ringId,name,shortName,iconUrl,template,pinned,archived,isDemo,organization(),hasArticles,team(%40permittedGroups),fieldsSorted,restricted,plugins(timeTrackingSettings(id,enabled),helpDeskSettings(id,enabled,defaultForm(uuid,title)),vcsIntegrationSettings(hasVcsIntegrations),grazie(disabled))%3B%40updateSharingSettings%3ApermittedGroups(%40permittedGroups),permittedUsers(%40user)%3B%40reporter%3AissueRelatedGroup(%40permittedGroups),id,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id)%3B%40usersTyping%3Atimestamp,user(%40user)%3B%40value%3Aid,name,autoAttach,description,hasRunningJobs,color(%40color),attributes(id,timeTrackingSettings(id,project(id)))%3B%40user%3Aid,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id)%3B%40textSearchResult%3AhighlightRanges(%40textRange),textRange(%40textRange)%3B%40permittedGroups%3Aid,name,ringId,allUsersGroup,icon,teamForProject(name,shortName)%3B%40tags%3Aid,name,color(%40color)%3B%40color%3Aid,background,foreground%3B%40markdownEmbeddings%3Akey,settings,widget(id)%3B%40textRange%3AstartOffset,endOffset"
        full_url = f"{URL}{ATTRIBS}"

        formated_ticket = Ticket.spam(ticket_id)
        
        fields = [
            {
                "$type": "MultiOwnedIssueCustomField",
                "id": "158-10166",
                "value": 
                [
                    {
                    "description": None,
                    "id": "166-796",
                    "kind": "enum",
                    "label": "Spam",
                    "name": "Spam"
                    }
                ]
            },
            {
                "$type": "SingleEnumIssueCustomField",
                "id": "158-10832",
                "value":
                {
                    "description": "",
                    "id": "138-5442",
                    "kind": "enum",
                    "label": "Спам",
                    "name": "Спам"
                }
            },
            {
                "$type": "SimpleIssueCustomField",
                "id": "517-17876",
                "value": "Спам"
            },
        ]
        data = {
            "summary":f"{formated_ticket.name}",
            "description":f"{formated_ticket.description}",
            "usesMarkdown":True,
            "markdownEmbeddings":[],
            "fields": fields
            }

        fields2 = [
            {
                "$type": "StateMachineIssueCustomField",
                "event": {
                    "id": "resolved"
                },
                "id": "158-10165"
            }
        ]
        data2 = {
            "description": f"{formated_ticket.description}",
            "fields": fields2,
            "markdownEmbeddings":[],
            "summary":f"{formated_ticket.name}",
            "usesMarkdown":True
        }

        fields3 = [
            {
                "$type": "StateMachineIssueCustomField",
                "event": {
                    "id": "closed"
                },
                "id": "158-10165"
            }
        ]
        data3 = {
            "description": f"{formated_ticket.description}",
            "fields": fields3,
            "markdownEmbeddings":[],
            "summary":f"{formated_ticket.name}",
            "usesMarkdown":True
        }
        
        response = requests.post(full_url, headers=self.HEADERS, data=json.dumps(data))
        response_2 = requests.post(full_url, headers=self.HEADERS, data=json.dumps(data2))
        response_3 = requests.post(full_url, headers=self.HEADERS, data=json.dumps(data3))
        print("Ticket sent to spam.")

    def _get_open_tickets_ids(self) -> list:
        URL = "https://tracker.ntechlab.com/api/sortedIssues"
        ATTRIBS = "?topRoot=100&skipRoot=0&flatten=true&query=state: {Waiting for L2}, {Waiting for developer}, {Waiting for delivery}, {Waiting for customer}, {On hold}, {Waiting for support} Assignee: -Unassigned&folderId=108-0&fields=tree(id,summaryTextSearchResult(highlightRanges(startOffset,endOffset)))"

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

    def _get_tickets_ids_for_sla_check(self) -> list:
        URL = f"https://tracker.ntechlab.com/api/sortedIssues"
        ATTRIBS = "?topRoot=100&skipRoot=0&flatten=true&query=state: {Waiting for L2}, {Waiting for support} Assignee: -Unassigned&folderId=108-0&fields=tree(id,summaryTextSearchResult(highlightRanges(startOffset,endOffset)))"
        full_url = f"{URL}{ATTRIBS}"
        tickets =  requests.get(full_url, headers=self.HEADERS).json()["tree"]

        formated_dict = []

        for index, ticket in enumerate(tickets):
            formated_dict.append({"id": ticket['id']})

        return formated_dict
    
    def get_tickets_info_for_sla_check(self) -> list:
        URL = "https://tracker.ntechlab.com/api/issuesGetter"
        ATTRIBS = "?$top=-1&$skip=0&fields=id,reporter(issueRelatedGroup(@permittedGroups),id,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id)),resolved,updated,created,unauthenticatedReporter,fields(value(id,minutes,presentation,name,description,localizedName,isResolved,color(@color),buildIntegration,buildLink,text,issueRelatedGroup(@permittedGroups),ringId,login,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id),allUsersGroup,icon,teamForProject(name,shortName)),id,$type,hasStateMachine,isUpdatable,projectCustomField($type,id,field(id,name,ordinal,aliases,localizedName,fieldType(id,presentation,isBundleType,valueType,isMultiValue)),bundle(id,$type),canBeEmpty,emptyFieldText,hasRunningJob,ordinal,isSpentTime,isPublic),searchResults(id,textSearchResult(highlightRanges(@textRange),textRange(@textRange))),pausedTime),project(id,ringId,name,shortName,iconUrl,template,pinned,archived,isDemo,organization(),hasArticles,team(@permittedGroups),fieldsSorted,restricted,plugins(timeTrackingSettings(id,enabled),helpDeskSettings(id,enabled,defaultForm(uuid,title)),vcsIntegrationSettings(hasVcsIntegrations),grazie(disabled))),visibility($type,implicitPermittedUsers(@user),permittedGroups(@permittedGroups),permittedUsers(@user)),tags(id,name,color(@color)),votes,voters(hasVote),watchers(hasStar),usersTyping(timestamp,user(@user)),canUndoComment,idReadable,summary;@user:id,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id);@permittedGroups:id,name,ringId,allUsersGroup,icon,teamForProject(name,shortName);@color:id,background,foreground;@textRange:startOffset,endOffset"
        DATA = json.dumps(self._get_tickets_ids_for_sla_check())
    
        full_url = f"{URL}{ATTRIBS}"

        tickets = requests.post(url=full_url, data=DATA, headers=self.HEADERS).json()
        
        formated_tickets = []

        for ticket in tickets:
            formated_ticket = Ticket.from_json(ticket)
            formated_tickets.append(formated_ticket)
        
        return formated_tickets