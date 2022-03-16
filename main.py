from filterparser import filterParser
import re
import regex
import pyparsing as pp

filter:str = "And(eq(FirstName,Shannon),NotInList(A360Identifier,(269245105,269053797,269210731)))"
# filter:str="And(eq(Firstname,William),eq(Lastname,richards),OR(eq(Nickname,William),eq(Nickname,sad),AND(lt(A360Identifier,10),gt(A360Identifier,5))))"
criteriajson=filterParser.GetFilterCriteria(filter,0)
print(criteriajson)

# # rx_comma = re.compile(r"(?:[^,(]|\([^)]*\))+")
# # result = rx_comma.findall(filterExtractPranthesis)
# # print(result)

# filter = "eq(Firstname,William),eq(Lastname,richards),OR(eq(Nickname,William),eq(Nickname,sad),AND(lt(A360Identifier,10),gt(A360Identifier,5)))"
# for s in regex.split(r"(\((?:[^()]++|(?1))*\))(*SKIP)(*F)|,", filter):
#     if s is not None:
#         print( s )
# # filter = "eq(Firstname,test),eq(Lastname,ltest),OR(eq(ContactID,12345),eq(ContactID,123456))"
# # result= regex.split(r"(\((?:[^()]++|(?1))*\))(*SKIP)(*F)|,", filter)
# # print(result)

# # s = "eq(Firstname,test),eq(Lastname,ltest),OR(eq(ContactID,12345),eq(ContactID,123456))"
# s="eq(Firstname,William),eq(Lastname,richards),OR(eq(Nickname,William),eq(Nickname,sad),AND(lt(A360Identifier,10),gt(A360Identifier,5)))"
# expr = pp.delimited_list(pp.original_text_for(pp.Regex(r'.*?(?=\()') + pp.nested_expr('(', ')')))
# output = expr.parse_string(s).as_list()
# print(output)
# assert output == ['eq(Firstname,test)', 'eq(Lastname,ltest)', 'OR(eq(ContactID,12345),eq(ContactID,123456))']