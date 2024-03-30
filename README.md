# Curves editor

Curve editor is a program that can draw and edit cubic splines and bezier curves. The project was created by Mikołaj Karapka for a **Numercial Analysis** course. The program was written in python and utilizes **PyQt6**, **Matplotlib** and **NumPy** libraries.

## Screenshots

### Plot of Bezier curve

![bezier](./screenshots/Bezier_curve_pic.png)

### Plot of Cubic spline

![cubic_spline](./screenshots/Cubic_spline_pic.png)

### Plot with pasted img

![pasted_img](./screenshots/Pasted_img.png)

## Features

- Drawing and Editing Multiple Bézier Curves (Bézier with a capital "B")
- Drawing and Editing Multiple Cubic Splines
- Pasting Image into Plot
- Saving Created Curves to File
- Reducing the Number of Sharp Edges in the Function (Rozmiar u)
- Moving Drawn Points on the Axis by a Specific Amount
- Zooming Drawn Curves

## Installation

```
poetry install
```

## Usage

### To start program:

```
poetry run project
```

### Shortcuts:

- **Draw a point**: Ctrl + left mouse button

- **Remove the last point**: Alt + left mouse button
