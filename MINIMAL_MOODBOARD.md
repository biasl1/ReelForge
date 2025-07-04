# 📸 Minimal Moodboard Implementation

## ✅ What's Implemented

### 🎯 **Simple & Clean**
- **Upload Button**: Click to select image file
- **Preview Area**: Shows uploaded image (hidden when no image)
- **File Status**: Displays filename when uploaded
- **Clear Button**: Remove uploaded moodboard
- **Auto-Save**: Project automatically saves moodboard path

### 📁 **File Management**
- Images copied to `project/moodboard/` directory
- Path saved as `project.moodboard_path`
- Supports: JPG, JPEG, PNG, GIF, BMP formats

### 🎨 **UI Features**
- Preview area appears only when image is uploaded
- Clean, minimal design
- No complex backgrounds or effects
- Simple error handling

## 📋 **How It Works**

1. **Upload**: Click "Upload Image" → Select file → Image copied to project
2. **Preview**: Preview area becomes visible showing scaled image
3. **Save**: File path automatically saved to project data
4. **Clear**: Click "Clear" → Remove image and hide preview
5. **Reload**: When project loads, moodboard is restored if available

## 🔧 **Technical Details**

### Files Modified:
- `ui/plugin_dashboard.py`: Added minimal preview section and upload logic

### Key Functions:
- `_upload_moodboard()`: Handle file selection and copying
- `_load_moodboard_preview()`: Scale and display image
- `_update_moodboard_display()`: Show/hide preview area
- `_clear_moodboard()`: Remove image and reset state

### No Background Effects:
- Preview only in moodboard section
- No timeline/calendar background changes
- No complex visual effects
- Focus on functionality only

## ✅ **Ready to Use**
The moodboard feature is now minimal, functional, and ready for testing!
