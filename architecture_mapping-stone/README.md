# Architecture_Mapping-Stone

AWS Architecture Mapping and Visualization






As of 8.11.2022--
This is a baby version. 
The presentation is attached - "Stone-Presentation.ppt"

There are some bugs in this version:
1. Mapping.print(self, level) is not working correctly as long as the level is not "container"
2. Somehow, when running Dash Server, the program will be run over and over again, nonstop. Have not figured out why. After self._updateMap() in Mapping.map() is commented, the problem got alleviated, but still running over and over again, ocassionally. 
3. Updating values to Plotly fails. It seems that plotly does not accept strings as values in treemap. An alternative way is using Mapping.show_Value_Of_Layer(self,ids), which can be used in a callback function in app.py to provide a way to display value, but front-end in app.py needs to be set up for it as well. 
4. After running the app: select a specific account, instance, pod. And boom. And deselect Account dropdown list. you will find that the Instance Dropdown list and Pod dropdown list are still populated, which is a bug. 

To proceed to the future scope, bugs documented above are better to be fixed already. 
The Future Scope:
1. Streaming: connecting to Athena. make Query to Athena every several minutes to get the lastest data from the according timestamp. This makes the app run automatically and dynamically. 
2. An input box on UI for users to input what values (column names on dataframe) they want to see from each component from different levels. In backend, there can be a function that add these user-defined values to object or class, so that everytime the app update values to map, these user-defined values can also be updated. 
3. deployment - can be in kubernetes, so that people can access it with a single url. 
4. connect to Athena or create a database, so that how data change for the past two months can be pulled from database through a slider callback function provided by Dash. With this feature, users can choose EKS status on what time they want to see