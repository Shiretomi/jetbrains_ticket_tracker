from os import getenv

import requests

POST_REQ = "https://tracker.ntechlab.com/api/issuesGetter?$top=-1&$skip=0&fields=id,reporter(issueRelatedGroup(@permittedGroups),id,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id)),resolved,updated,created,unauthenticatedReporter,fields(value(id,minutes,presentation,name,description,localizedName,isResolved,color(@color),buildIntegration,buildLink,text,issueRelatedGroup(@permittedGroups),ringId,login,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id),allUsersGroup,icon,teamForProject(name,shortName)),id,$type,hasStateMachine,isUpdatable,projectCustomField($type,id,field(id,name,ordinal,aliases,localizedName,fieldType(id,presentation,isBundleType,valueType,isMultiValue)),bundle(id,$type),canBeEmpty,emptyFieldText,hasRunningJob,ordinal,isSpentTime,isPublic),searchResults(id,textSearchResult(highlightRanges(@textRange),textRange(@textRange))),pausedTime),project(id,ringId,name,shortName,iconUrl,template,pinned,archived,isDemo,organization(),hasArticles,team(@permittedGroups),fieldsSorted,restricted,plugins(timeTrackingSettings(id,enabled),helpDeskSettings(id,enabled,defaultForm(uuid,title)),vcsIntegrationSettings(hasVcsIntegrations),grazie(disabled))),visibility($type,implicitPermittedUsers(@user),permittedGroups(@permittedGroups),permittedUsers(@user)),tags(id,name,color(@color)),votes,voters(hasVote),watchers(hasStar),usersTyping(timestamp,user(@user)),canUndoComment,idReadable,summary;@user:id,ringId,login,name,email,isEmailVerified,guest,fullName,avatarUrl,online,banned,banBadge,canReadProfile,isLocked,userType(id);@permittedGroups:id,name,ringId,allUsersGroup,icon,teamForProject(name,shortName);@color:id,background,foreground;@textRange:startOffset,endOffset"

def get_tickets_ids():
    TOKEN = getenv('YOUTRACK_TOKEN')
    URL = "https://tracker.ntechlab.com/api/sortedIssues"
    ATTRIBS = "?topRoot=100&skipRoot=0&flatten=true&query=state: {Waiting for L2}, {Waiting for developer}, {Waiting for delivery}, {Waiting for customer}, {On hold}, {Waiting for support}&folderId=108-0&fields=tree(id,summaryTextSearchResult(highlightRanges(startOffset,endOffset)))"
    HEADERS = {
        'Accept': 'application/json',
        f'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    full_url = f"{URL}{ATTRIBS}"
    tickets = requests.get(full_url, headers=HEADERS).json()["tree"]

    formated_dict = []

    for index, ticket in enumerate(tickets):
        print(index, ticket['id'])
        formated_dict.append({'id': ticket['id']})

    print(formated_dict)
