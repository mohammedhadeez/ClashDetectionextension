# Clash Detection Extension for PyRevit

## Overview
Advanced clash detection tools for Autodesk Revit, providing automated clash detection, visualization, and reporting capabilities.

## Features

### Detection Panel
- **Run Detection**: Comprehensive clash detection between selected elements
- **Quick Check**: Fast bounding-box based clash detection for active view
- **Settings**: Configure detection parameters and tolerances

### Reports Panel
- **Export Report**: Export clash results to CSV, HTML, or JSON formats
- **View History**: Track clash detection history and resolution status

### Visualization Panel
- **Highlight Clashes**: Visually highlight and isolate clashing elements

## Installation

1. Copy the entire `ClashDetection.extension` folder to your PyRevit extensions directory:
   - Typically: `%APPDATA%\pyRevit\Extensions\`
   
2. Reload PyRevit or restart Revit

3. The "Clash Detection" tab should appear in your Revit ribbon

## Usage

### Basic Clash Detection
1. Select elements to check for clashes
2. Click "Run Detection" in the Clash Detection tab
3. Review results in the dialog

### Quick Check
1. Open a view with the elements you want to check
2. Click "Quick Check" for fast preliminary detection
3. Use this for rapid iteration during design

### Exporting Reports
1. After running detection, click "Export Report"
2. Choose format (CSV, HTML, JSON)
3. Select save location
4. Open in Excel or web browser to review

### Visualization
1. Select clashing elements
2. Click "Highlight Clashes"
3. Choose highlight color or isolation mode
4. Use "Reset View" to restore original display

## Configuration

Access Settings to configure:
- Detection tolerance (in mm)
- Categories to check (MEP, Structure, Architecture)
- Export format preferences
- Visualization colors
- Auto-isolation options

## Technical Details

### Supported Elements
- Walls
- Columns
- Structural Framing
- Floors
- Roofs
- Doors & Windows
- MEP Elements (Ducts, Pipes, etc.)

### Detection Methods
1. **Solid Intersection**: Accurate geometric intersection
2. **Bounding Box**: Fast preliminary detection
3. **Tolerance-based**: Configurable proximity detection

## Requirements
- Revit 2020 or later
- PyRevit 4.8 or later
- IronPython 2.7

## Troubleshooting

### Extension not appearing
- Verify installation path
- Check PyRevit is properly installed
- Reload PyRevit (Ctrl+F5)

### Detection running slowly
- Use Quick Check for initial screening
- Reduce selection size
- Adjust tolerance settings

### No clashes detected
- Verify elements have solid geometry
- Check tolerance settings
- Ensure elements are in same coordinate system

## Development

### File Structure
```
ClashDetection.extension/
├── ClashDetection.tab/
│   ├── Detection.panel/
│   │   ├── Run Detection.pushbutton/
│   │   ├── Quick Check.pushbutton/
│   │   └── Settings.pushbutton/
│   ├── Reports.panel/
│   │   ├── Export Report.pushbutton/
│   │   └── View History.pushbutton/
│   └── Visualization.panel/
│       └── Highlight Clashes.pushbutton/
├── lib/
│   └── clash_utils.py
├── hooks/
│   └── doc-opened.py
└── extension.json
```

### Customization
- Modify `clash_utils.py` to add custom detection algorithms
- Edit button scripts to add functionality
- Update `extension.json` for metadata

## License
MIT License - Feel free to modify and distribute

## Author
Your Name

## Version
1.0.0

## Support
For issues or questions, please contact: your.email@example.com
