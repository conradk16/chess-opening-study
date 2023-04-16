# chess-opening-study
To Use:
* Create a Google Sheet with 'White' and 'Black' tabs, each with opening moves enumerated
    * see [Example White](example_white.png) and [Example Black](example_black.png)
    * Use indentation for deeper moves as shown. Must use official [Chess Algebraic Notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)).
    * Each box should have two moves separated by a space (with the exception of the very first move), with the opponent's move first and the move to learn second.
* Create a Google Workspace project with access to Google Sheets
    * see https://console.cloud.google.com/
    * create an OAuth client id for the project and download the client id and secret into a file 'credentials.json'
* In the main directory,
    * create sheet_id.txt (a single-line text file with the Google Sheet id)
    * add credentials.json (from the Google Workspace step)
