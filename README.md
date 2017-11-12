Introduction
============

This application is a centralized file storing system. It is a naive
implementation of a cloud storage system such as Google Drive, that
allows users to store a central server and voluntarily share uploaded
files with other users.

Objective
=========

Our objective was to build an application that could provide the
following services:

-   Securely transfer files to personal directories on a central server.

-   Concurrently allow multiple users to access their files.

-   Allow users to share their files with other users.

Assumptions
===========

We made the following assumptions while designing the application:

-   User cannot create new directories.

-   User cannot change his/her account credentials.

-   User cannot edit files on the server directly.

Architecture
============

The application is built keeping a client-server architecture in mind. A
central server is kept running on a designated port, waiting for TCP
connections from clients. Once connected, a child process is forked to
handle each client while the parent waits to accept more connections,
thus allowing concurrent access.

![State Diagram depicting the sequences of possible actions once the
client-server connection is established.](stateDiagram.png "fig:")
[fig:my~l~abel]

Figure [fig:my~l~abel] shows the state diagram which explains the
possible sequences of actions that can take place once the connection is
established. Once authentication is done by the server, it provides a
list of options to the client. The user can provide the number
corresponding to the command he/she wants to execute.

1.  **HELP: **Shows the mapping between the commands and the option
    number.

2.  **List Files: **Shows all the files that a user has uploaded on the
    server. Also shows the files that other users have shared with a
    particular user.

3.  **Upload File: **Asks for file address to upload on the server and
    if that file exists, it will upload it in the users directory on the
    server with the same name. Before uploading the file, server also
    checks if some file with same name exists, if yes then it will
    create a file with same name appended with a number (filename\_num)
    and transfer the data into it.

4.  **Download File: **Asks for file name to download from the server.
    If the file does not exists on the server, it will check if it is
    shared and send “File doesn’t exists!!” if it doesn’t.

5.  **Delete File: **Asks for a file name to delete from the server.
    Only delete if the file name exists in the user directory.

6.  **Give Access: **Asks for a file name and the username to whom
    access will be given. If either of the user or the file does not
    exist then it will show the error, otherwise it will share the given
    file with the given user.

7.  **Revoke Access: **Asks for a file name and the username from whom
    access of the file will be revoked. If either of the user or the
    file does not exist then it will show the error, otherwise it will
    revoke the access of the given file from the given user.

8.  **List Shared Files: **Lists all the files that a user has shared
    with other users.

9.  **Exit: **Logs the user out of the application.

Implementation
==============

We have built the system from scratch using basic socket programming in
python 2.7. We used hashlib library for encrypting the passwords.\
The implementation code can be found at
<https://github.com/rishgoyell/fileServerApp/>

Summary
=======

Our implementation provides several features using which a user can
achieve all the objectives that we had originally set out with.
