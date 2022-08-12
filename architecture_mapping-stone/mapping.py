import plotly.express as px
from component import *
from ProcessData import preProcess
import pandas as pd
from objsize import get_deep_size
import inspect

# The argument of this class is supposed to the path to the EKS dataframe
# Note:
# The current DB has no "pod_id" or "container_id". Therefore, all "pod_name" and "container_name" should be changed to "pod_id" & "container_id" accordingly."
# To use this class, check the example in main function at the buttom of this program.

class Mapping:
    __ARCH_LEVEL = ('architecture', 'account', 'node', 'pod', 'container')

    # self._arch: The most important thing this Mapping class provides is the self._arch, 
    #   which is considered an object from Component Class.
    # self._mapBuilt: used to tell the app to rebuild the whole architecture map. 
    def __init__(self, path) -> None:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        print(f"Initializing new object for Architecture in {filename}...")
        self._arch = Architecture("root")
        # self._mapBuilt = False
        # self._df = None
        # self._df_recType_dict = None
        self._setPath(path)

    def getArchitecture(self):
        return self._arch

    def _setPath(self, path):
        if not path:
            raise TypeError(f"The argument of this class is supposed to be the path to the EKS dataframe")
        self._path = path

    def resetMap(self):
        self._mapBuilt = False

    # check if any row has any nan values in container level
    def _preCheck(self, df_recType_dict):
        null_cols = ["account_id", "name_space", "instance_id", "pod_name", "container_name"]
        for col in null_cols:
            null_col = df_recType_dict['Container'][col].isnull().values.any()
            if (null_col):
                raise TypeError(f"{col} has nan value. Cannot access a 'None' object.")

    def _pair(self, row, dad, kid_column_name, kidClass):
        kids = dad.getChildren()
        if row[kid_column_name] not in kids.keys():
            currKid = kidClass(id=row[kid_column_name], parent=dad)
            dad.addChildren(currKid.id(), currKid)
        else:
            currKid = kids.get(row[kid_column_name])
        return currKid

    # Build architecture map, pair each dad Component to kid Component.
    def _buildMap(self):
        print("Building up the EKS Architecture Map")
        df = pd.read_csv(self._path)
        df_recType_dict = preProcess(df, drop_feature = 'default', partition_by = 'rec_type', convert_to_timestamp = 'metric_epochtime')
        self._preCheck(df_recType_dict)

        # Account -> Node -> Pod -> Container
        for index, row in df_recType_dict["Container"].iterrows():
            currAccount = self._pair(row, self._arch, 'account_id', Account)
            currNode = self._pair(row, currAccount, 'instance_id', Node)
            currPod = self._pair(row, currNode, 'pod_name', Pod)
            # currNamespace = self._pair(row, currAccount, 'name_space', Namespace)
            # currPod = self._pair(row, currNamespace, 'pod_name', Pod)
            currContainer = self._pair(row, currPod, 'container_name', Container)
        # self._mapBuilt = True
        print("Finished building up the EKS Architecture Map")

    # If updateMap fails because the mapping is wrong, then reset self._mapBuilt and call map again. But right now 
        # this is not implemented yet because the poor quality of dataset.
    # only values in level_dict will be updated, so may need to adjust it if necessary. 
    def _updateMap(self):
        print("Updating the EKS Architecture Map")
        df = pd.read_csv(self._path)
        df_recType_dict = preProcess(df, drop_feature = 'default', partition_by = 'rec_type', convert_to_timestamp = 'metric_epochtime')
        col_names = ['account_id', 'instance_id', 'pod_name', 'container_name']
        level_dict = {'Node': 2, 'Pod': 3, 'Container': 4}
        for type in df_recType_dict:
            try:
                levelNum = level_dict[type]
            except:
                print(f"the current rec_type {type} will be skipped")
                continue
            print(f"Starting updating components of current rec_type {type}")
            for index, row in df_recType_dict[type].iterrows():
                level = []
                for i in range(levelNum):
                    level.append(row[col_names[i]])
                try: vertex = self._find(level)
                except Exception as e:
                    print(e)
                    continue
                for str in vertex.getAttrName():
                    vertex.getAttr()[str] = row[str]
            print(f"Finished updating components of current rec_type {type}")
        print("Finished updating the EKS Architecture Map")

    def map(self):
        # if self._path != path: self._path = None
        # if self._mapBuilt == False and build==True:
        self._buildMap()
        # if update==True:
        # self._updateMap()

    def _graphAndAppendDFS(self, nameArr, parentArr, vertex):
        if vertex.numOfChildren() == 0: return
        for childName, child in vertex.getChildren().items():
            nameArr.append(childName)
            parentArr.append(child.parent().id())
            self._graphAndAppendDFS(nameArr, parentArr, child)

    # since the value can only accept Integer, I have not figured out how to make plotly to accept string values.
    def _graphAndAppendBFS(self, nameArr, parentArr, vertex, onelayer=False):
        queue = [] #Initialize a queue to explore the components of tree/graph.
        for child in vertex.getChildren().values():
            queue.append(child)
        while queue:
            currVertex = queue.pop(0)
            nameArr.append(currVertex.id())
            parentArr.append(currVertex.parent().id())
            # value =''
            # for s in vertex.getAttrName():
            #     value = value + "\n" + s + ": " + str(vertex.getAttr()[s])
            #     break
            # valueArr.append(value)
            if onelayer == True: continue
            for child in currVertex.getChildren().values():
                queue.append(child)

    # make a graph.
    # The parameter onelayer will determines if only one layer of children of parameter vertex will be graphed. 
    def graph(self, vertex=None, onelayer=False, num=None, sizeT=50, sizeL=25, sizeR=25, sizeB=25):
        if not vertex: vertex = self.getArchitecture()
        name = []
        parent = []
        vertexTemp = vertex
        while vertexTemp.parent() != None:
            name.insert(0, vertexTemp.id())
            parent.insert(0, vertexTemp.parent().id())
            vertexTemp = vertexTemp.parent()
        self._graphAndAppendBFS(name, parent, vertex, onelayer)
        fig = px.treemap(
            names = name[:num] if num else name,
            parents = parent[:num] if num else parent,
        )
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin = dict(t=sizeT, l=sizeL, r=sizeR, b=sizeB))
        #fig.show()
        return fig

    # The parameter vertex needs to be an object of component
    def getParentsId(self, vertex):
        if not isinstance(vertex, Component):
            raise TypeError("The parameter passed into this function needs to be type of Component")
        str = f"{vertex.type()}: {vertex.id()}"
        parentsID = [str]
        while vertex.parent() != None:
            vertex = vertex.parent()
            str = f"{vertex.type()}: {vertex.id()}"
            parentsID.insert(0, str)
        return parentsID

    # This function helps find a specific component among all and return the component object.
    # the parameter ids should be a list of id, ordered by the hierarchy level. (account_id -> instance_id -> pod_id -> container_id)
    def _find(self, ids=None):
        vertex = self.getArchitecture()
        for id in ids:
            if id not in vertex.getChildren():
                print(f"The id: {id} in the input does not exist in {self.getParentsId(vertex)}")
                break
            vertex = vertex.getChildren()[id]
        return vertex

    # see _find()
    def find_name_of_children_of(self, ids):
        return tuple(self._find(ids).getChildren().keys())

    # see _find()
    def graphLayerOf(self, ids, num=None):
        vertex = self._find(ids)
        print(self.find_name_of_children_of(ids))
        return self.graph(vertex=vertex, onelayer=True, num=num, sizeT=50, sizeL=25, sizeR=25, sizeB=25)

    # This function provides a way to UI to display values by using callback function in app.py
        # In the callback function, what this function return is the values dictionary of each component.
    def show_Value_Of_Layer(self,ids):
        vertex = self._find(ids)
        return vertex.getAttr()

    def _print(self, level, originLevel, kids):
        if level < 0: return
        else: level -= 1
        for kidStr in kids.keys():
            kidObj = kids.get(kidStr)
            grandkids = kidObj.getChildren()
            dash = '---' * (4 - level) * 3
            if level > 0:
                print(f'{dash} {kidObj.type()}: {kidStr}: {len(grandkids)} {Mapping.__ARCH_LEVEL[5-level]}')
            else: print(f'{dash} {kidObj.type()}: {kidStr}')
            self._print(level, originLevel, grandkids)

    # This function has some bugs. Not function correctly as long as level is not 'container'
    # The parameter of this function must be one of the string in ('architecture', 'account', 'node', 'pod', 'container')
    # This function is used to print the architecture in text
    def print(self, level):
        if not isinstance(level, str): raise TypeError(f"The input of this function must be one of the string in {Mapping.__ARCH_LEVEL}")
        level = level.lower()
        if level not in Mapping.__ARCH_LEVEL:
            raise TypeError(f"The input of graph() must be one of the strings in {Mapping.__ARCH_LEVEL}")
        else: level = Mapping.__ARCH_LEVEL.index(level)

        archKids = self._arch.getChildren()
        print(f'{self._arch.id()}: {len(archKids)} accounts')
        self._print(level, level, archKids)



if __name__ == '__main__':
    path = 'C:/Users/Xiaohai.Chen/Desktop/Intern_Work_Summer_2022/memory-leak-robust/EKS-1million.csv'
    map = Mapping()
    map.map(path)
    # map.graph(num=80, sizeT=50, sizeL=25, sizeR=25, sizeB=25)
    # map.find_name_of_children_of([675136609689, 'i-0b1842d240befd13a', 'udm01-http2lb'])
    map.graphLayerOf([675136609689, 'i-0b1842d240befd13a', 'udm01-http2lb'])
    # map.print("container")
