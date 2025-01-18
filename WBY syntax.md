# WBY Renderer

The **WBY Renderer** is a simple Python application that allows dynamic display of text and buttons using the Tkinter GUI. Elements of type `text` and `button` can be displayed with styles interpreted by the code, which are defined in a custom format.

## Table of Contents

- Features
- Usage
- Styles
- Development

## Features

- **text** type elements display text with a specified style.
- **button** type elements display buttons, which also have styles.
- Styles can be applied with various parameters, such as color, font size, background color, width, height, and padding.
- Styles can also be customized using parameters like `padding`, `font-size`, `color`, and more.

## Usage

1. To run the project, ensure that Python 3.x is installed on your system.
2. Copy the code into a Python file (e.g., `renderer.py`).
3. After running the program, text and buttons will appear in the GUI with the configured styles.

Example of displaying text and buttons in the following input format:

```text
text: text="hello hi bye", style=[color="red", font-size="20", padding="10 0"]
/W\ text: text="this is a commented line", style=[color="red", font-size="20"]
text: text="what is this?", style=[color="purple", font-size="20", background-color="red"]
button: text="hi", style=[width="5"]
text: text="just a test", style=[color="purple", font-size="20"]
button: text="hi", style=[width="10"]
```

This input text will display the following elements:

- A red text with 20px font size, 10px horizontal padding, and 0px vertical padding.
- A commented line that will not appear.
- A text with a red background and purple color.
- Two buttons, each with different widths.

## Styles

The styles can have the following parameters:

- **color**: The text color (e.g., `color="red"`).
- **background-color**: The background color (e.g., `background-color="blue"`).
- **font-size**: The font size (e.g., `font-size="20"`).
- **width**: The widget width (e.g., `width="10"`).
- **height**: The widget height (e.g., `height="5"`).
- **padding**: The padding setting (e.g., `padding="10 0"`).

If padding contains two values (e.g., `"10 0"`), you can set different values for horizontal and vertical padding. If only one value is given (e.g., `"10"`), it will apply to both directions.

## Development

The project uses the **Tkinter** library to create the graphical user interface (GUI). The widgets (texts and buttons) are dynamically generated based on the input text and displayed with the specified styles.

The following files are included in the project:

- `renderer.py`: Contains the renderer logic that handles styles and widgets.
- `app.py`: The main application that handles the GUI and events.

### Future Improvements

- Support for more widget types (e.g., list, input field).
- Advanced style and layout management.
- Additional color and layout templates.
