import re
from typing import List
from configurations import filterOperatorDict, filterTypeDict
import regex


class FilterParser:
    def __init__(self,filterArray):
        self.filterArray=filterArray

         

    def IsNested(self,filter: str):
        isNested = (re.sub("(\\(.*\\))", "",filter).lower() ==
                        "and") or (re.sub("(\\(.*\\))", "",filter).lower() == "or")
        return isNested


    def GetFilterCriteria(self,filter: str, filterIndex: int, parentFilterOperator: str = ""):
            # queryCollection: dict = dict()
        if not self.IsNested(filter):
            self.filterArray.append(self.ConstructFilterString(filter))

        else:
               
            filterOperator = filterOperatorDict.get((re.sub("(\\(.*\\))", "",filter)).lower())
            if (filterOperator == "Default"): raise Exception(
                "Invalid filter criteria")
            # pattern = @"(?>(?<S>\()|(?<-S>\))|[^,()]|(?(S),|(?!)))+(?(S)(?!))";
            filterExtractPranthesis =filter[filter.find("(")+1:filter.rfind(")")]
            # re.search(f"(?<=\().*(?=\))",filter).group(1)
            r = re.compile(r'(?:[^,(]|\([^)]*\))+')
            filterWithCommaSeperated = regex.split(r"(\((?:[^()]++|(?1))*\))(*SKIP)(*F)|,", filterExtractPranthesis)
            filterWithSingleParams: list=list()
            filterWithNonSingleParams: list=list()
            
            for f in filterWithCommaSeperated:
                if f is not None:
                    if(self.IsNested(f)):
                        filterWithNonSingleParams.append(f)
                    else:
                        filterWithSingleParams.append(f)
            if (filterIndex == 0 and len(self.filterArray) == 0):
                self.filterArray = self.GetListofFilters(
                    filterWithSingleParams, filterOperator)
                
                

            else:
                
                self.GetNestedFilter(self.filterArray, filterWithSingleParams, filterOperator
                                    , parentFilterOperator, filterIndex)
                
                    

            if (len(filterWithNonSingleParams)> 0):

                filterIndex = filterIndex+1

                for con in filterWithNonSingleParams:

                    self.GetFilterCriteria(con, filterIndex, filterOperator)


        
        return self.filterArray

        # adds the nested filter
    def GetNestedFilter(self,filterArray: List[dict], filterWithSingleParams: List[str], filterOperator: str, parentFilterOperator: str="", filterIndex: int=0):
        if (filterIndex == 1):
        
            if not parentFilterOperator == "And":
                dictonaryFilter=dict()
                dictonaryFilter["operator"]=parentFilterOperator
                dictonaryFilter["filters"]=self.GetListofFilters(filterWithSingleParams, filterOperator)
                self.filterArray.append(dictonaryFilter)
            else:
                dictonaryFilter=dict()
                
                dictonaryFilter["filters"]=self.GetListofFilters(filterWithSingleParams, filterOperator)
                self.filterArray.append(dictonaryFilter)
                

        else:
            lastOrDefaultArray=[i for i, x in enumerate(self.filterArray)]

            
            # print(next(d for i,d in enumerate(self.filterArray) if "filters" in d).keys())
            res_list:dict =next(d for i,d in enumerate(self.filterArray) if "filters" in d)
            
            for key in res_list.keys():
                nestedFilter = next(d for i,d in enumerate(self.filterArray) if "filters" in d)[key]
                
                nestedFilterList: List[dict] = nestedFilter
                # if isinstance(nestedFilter, List[dict]):
                
                if not "filters" in nestedFilterList[-1]:
                    
                   
                    if not parentFilterOperator == "And":
                        nested_Dict=dict()
                        nested_Dict["operator"]=parentFilterOperator
                        nested_Dict["filters"]= self.GetListofFilters(
                                        filterWithSingleParams, filterOperator)
                                    
                        
                        nestedFilterList.append(nested_Dict)
                    else:
                        nested_Dict=dict()
                        nested_Dict["filters"]= self.GetListofFilters(
                        filterWithSingleParams, filterOperator)
                        nestedFilterList.append(nested_Dict) 
                        continue

                    self.GetNestedFilter(nestedFilterList, filterWithSingleParams,
                                filterOperator, parentFilterOperator)




            return self.filterArray

    def GetListofFilters(self,filters: List[str], filterOperator: str = ""):
        filtersList=list()
        for condition in filters:
            if not self.IsNested(condition):
                if filters[0] == condition:
                    filtersList.append(self.ConstructFilterString(condition))
                else:
                    
                    filtersList.append(self.ConstructFilterString(
                        condition, filterOperator))


        return filtersList

        # extract the each condition and return as a dictionary element

    def ConstructFilterString(self,condition: str, filterOperator: str = ""):
        dictonaryFilter=dict()
        filterType=filterTypeDict.get((re.sub("(\\(.*\\))", "",condition)).lower())
        # filterTypeDict[re.sub("(\\(.*\\))", "",condition)]
        if filterType == "Default":
            raise Exception("Invalid filter criteria")
        if (not filterOperator == "") and (not filterOperator == None) and (not filterOperator == "And"):
            dictonaryFilter["operator"] = filterOperator
            
        filterExtractPranthesis=condition[condition.find("(")+1:condition.rfind(")")]
        r=re.compile(r'(?:[^,(]|\([^)]*\))+')
        filterCondition=r.findall(filterExtractPranthesis)
        if len(filterCondition)> 0:
            dictonaryFilter["name"] = filterCondition[0] if len(filterCondition) > 0 else ""
            dictonaryFilter["type"] = filterType
            dictonaryFilter["value"] = filterCondition[1] if len(filterCondition) > 1 else ""
            

        else:
            dictonaryFilter["name"] = condition
            dictonaryFilter["type"] = filterType
            

        
        return dictonaryFilter

filterParser=FilterParser(list())