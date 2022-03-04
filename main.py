from filterparser import filterParser
import re
import regex

# filter: str = "And(eq(FirstName,Shannon),NotInList(A360Identifier,(269245105,269053797,269210731)))"
filter:str="And(eq(Firstname,William),eq(Lastname,richards),OR(eq(Nickname,William),eq(Nickname,sad),AND(lt(A360Identifier,10),gt(A360Identifier,5))))"
criteriajson=filterParser.GetFilterCriteria(filter,0)
print(criteriajson)

# rx_comma = re.compile(r"(?:[^,(]|\([^)]*\))+")
# result = rx_comma.findall(filterExtractPranthesis)
# print(result)

# filter = "eq(Firstname,test),eq(Lastname,ltest),OR(eq(ContactID,12345),eq(ContactID,123456))"
# for s in regex.split(r"(\((?:[^()]++|(?1))*\))(*SKIP)(*F)|,", filter):
#     if s is not None:
#         print( s )
# filter = "eq(Firstname,test),eq(Lastname,ltest),OR(eq(ContactID,12345),eq(ContactID,123456))"
# result= regex.split(r"(\((?:[^()]++|(?1))*\))(*SKIP)(*F)|,", filter)
# print(result)