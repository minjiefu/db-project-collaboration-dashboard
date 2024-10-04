# Title
Roadmap of Seeking Research Collaborators

# Purpose
- The application serves as a roadmap for users seeking potential research collaborators. 
- Target users include students, professors, researchers, and anyone interested in finding research collaborations. 
- The primary objectives of the application are to assist users in identifying historical and current research trends, defining their research interests, recognizing leading researchers in their field, and establishing networking connections to reach out to potential collaborators.

# Demo
https://mediaspace.illinois.edu/media/t/1_6ohijp9b

# Installation
### Step 1: 
Install the required prerequisite packages, including dash, pandas, dash_bootstrap, dash_cytoscape, plotly.express, pymongo, mysql-connector-python, neo4j
### Step 2:
Upload the databases to MySQL, MongoDB, and Neo4j.
### Step 3:
Execute the queries found in the "install.sql" file to implement database techniques like creating views, indexes, and constraints, with the goal of improving the efficiency of the database.
### Step 4: 
Launch the Dash application by running "python app.py".
The application can be accessed at http://127.0.0.1:8050/.

# Usage
The application is accessible through a dashboard interface on a website. The dashboard is comprised of seven widgets strategically arranged to serve as a roadmap, guiding target users through the process of searching for potential research collaborators step by step. The application is both useful **(R4)** and innovative **(R5)**.
### Widget 1: 
Users begin by gaining an overview of the most popular historical and current research areas. Through the range slider feature, users can select a specific time frame, prompting the display of the top 10 research keywords alongside their respective publication counts.
### Widget 2: 
Users have the option to input a specific keyword from the dropdown list, which will then generate a display showcasing the trends in publication counts related to that keyword.
### Widget 3: 
After gaining an understanding of the broader research landscape through the initial two widgets, users can further refine their focus by selecting their own research interests from the dropdown list. By clicking the "add" button, their chosen research interests will be included in a designated table for potential further exploration.
### Widget 4: 
Simultaneously with the addition of selected research interests to the table in Widget 3, a secondary table will be automatically populated with recommended collaborators based on those research interests. A list of recommended collaborators will be displayed here to foster potential partnerships and collaborative opportunities for the users in their respective research areas.
### Widget 5: 
Upon selecting a recommended collaborator from the table in Widget 4, detailed information such as their photos, name, university, and position will be promptly displayed in this widget for user reference.
### Widget 6: 
This widget serves as a note-taking tool, offering users the flexibility to jot down potential collaborators of interest and other relevant notes. Users can easily add new rows using the "Add Row" function and input notes in editable cells.
### Widget 7: 
This widget is a valuable tool that allows users to establish connections with potential collaborators. By selecting a person they know from the "Collection From" dropdown list and the person they wish to reach out to from the "Collection To" dropdown list, users can click the search button to generate a visual graph illustrating their networking connections.

# Design
- The widgets are arranged in a rectangular space, organized into three rows to optimize usability and user experience. Seven widgets **(R9)** are strategically placed on the dashboard to serve as a roadmap for users. Each widget is carefully arranged to provide step-by-step guidance, helping users navigate through the search process efficiently and effectively. The layout is visually pleasing, informative, and logical **(R12)**.
- The application is user-interactive. All seven widgets take input from users **(R11)**.
- Two of the widgets perform updates of the backend databases **(R10)**. Widget 3 allows users to select potential research interests from a dropdown list and adds them to a table. The user's selections are then saved into the backend database for future reference and analysis. Widget 6 takes input from an editable datatable where users can input specific data related to their interested collaborations. The information entered in this datatable is saved into the backend database, ensuring that all relevant details are securely stored and accessible for future use. 

# Implementation
- The application is developed using the Dash Plotly framework for creating the user interface design. Dash is a Python framework that allows for the development of interactive web applications.
- The primary file for the application is app.py, which leverages Dash along with other libraries such as Pandas, Bootstrap, Cytoscape, and Plotly Express. These libraries are used to declaratively create widgets, define their layout, and style them accordingly.
- The backend of the application contains the Academic World dataset, which is stored in three different types of databases: MySQL(RDBMS) **(R6)**, MongoDB(DocumentDB) **(R7)**, and Neo4j(GraphDB) **(R8)**. 
- The application utilizes Python packages for connecting to various database management systems. Specifically, it employs the 'mysql.connector' package for MySQL connectivity, 'pymongo' for MongoDB interaction, and 'neo4j' for communicating with Neo4j databases.
- To interact with the backend databases, the application utilizes three separate files: mysql_utils.py, mongodb_utils.py, and neo4j_utils.py. These files contain functions that facilitate the querying and manipulation of databases using their respective query languages.
- Widget 1 uses MongoDB. Widget 7 uses Neo4j database. All other widgets use Mysql.



# Database Techniques
Indexing, View, and Constraint are used to improve the performance of Mysql database.
- Indexing **(R13)**: Index was added to the name variable in keyword table.
- View **(R14)**: View partner_info was created. 
- Constraint **(R15)**: Foreign key constraint was added to the faculty_keyword table on keyword_id.

# Contributions
The project was done individually. Total time spent is about 50 hours.
