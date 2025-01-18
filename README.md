# Wolimby Search

This project provides a simple web application that uses its own protocol and description language to render user interfaces. The project consists of three main files: `server.py`, `renderer.py`, and `browser.py`. The `.wby` files contain the layout descriptions, and the program reads and displays these files to the user.

## Files

1. **server.py**

    This file contains the server that listens for incoming requests on a specified port and responds with the requested `.wby` files.

    **How it works:**
    - The server creates a TCP connection to localhost on a specified port (default port: 5000).
    - The server accepts requests, and if the request is for a `.wby` file, it serves the file based on its availability.
    - If the file is not found, an error message is sent back to the client.

    **Usage:**
    To start the server, run the following command:
    ```sh
    python server.py
    ```

2. **renderer.py**

    This file is responsible for rendering the elements (such as button, label, entry, etc.) from the `.wby` files using the `tkinter` library to create the GUI widgets.

    **How it works:**
    - The file interprets the description in the `.wby` file and creates the appropriate `tkinter` widgets (e.g., buttons, labels, input fields).
    - It also applies styles and layout configurations based on the style parameters specified in the file.

3. **browser.py**

    This file handles user interactions and file loading. The browser communicates with the server and displays the appropriate `.wby` files to the user.

    **How it works:**
    - The user enters a URL (e.g., `localhost:5000/example.wby`), and the browser requests a file from the server.
    - After loading the file, the renderer displays its content on the user interface.

## How to create your own `.wby` file

A `.wby` file contains descriptions of the user interface elements and their corresponding styles. Below is an example of the layout descriptions in a `.wby` file:

```text
text: text="Hello world!", style=[color="blue", font-size="18", padding="10"]
button: text="Push me!", style=[color="white", background-color="green", padding="10"]
entry: text="Write something", style=[width="30"]
radiobutton: text="First option", style=[color="red"], options=[value=1]
combobox: text="Choose", style=[width="20"], options=[values=One|Two|Three]
listbox: text="Elem 1|Elem 2|Elem 3", style=[height="5"]
scale: text="Slider", style=[width="200"], options=[from=0, to=100, orient=vertical]
progressbar: text="Description", style=[width="500", padding="10"], options=[value=50]
message: text="This is a message", style=[font-size="16", color="darkgreen", padding="10"]
\W/ message: text="This is a message which is commented", style=[font-size="16", color="darkgreen"]
```

In the example above:
- `text` represents a label with text.
- `button` defines a button element.
- `entry` is an input field.
- `radiobutton`, `combobox`, `listbox`, `scale`, `progressbar`, and `message` define their respective widgets.

The `style` parameter allows for customization of the appearance of each element, such as color, font size, and padding. The `\W/` syntax is used for comments in the `.wby` file.

You can create and modify these files to define the layout and appearance of your interface. Save the file with the `.wby` extension and load it through the browser interface.

**Notes:**
- Ensure that the `.wby` file is available in the specified directory, and the server is running to serve the file.
- The elements in the `.wby` file will be rendered based on the configuration set in the `renderer.py` file.