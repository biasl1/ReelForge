"""
Visual WYSIWYG template editor for ReelTune.
Mini After Effects-style editor with draggable layers and real-time preview.
"""
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel,
    QComboBox, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QTreeWidget, QTreeWidgetItem, QSplitter, QCheckBox,
    QSlider, QColorDialog, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF, QSizeF
from PyQt6.QtGui import (
    QColor, QPalette, QPainter, QPen, QBrush, QFont,
    QPixmap, QDragEnterEvent, QDropEvent, QMouseEvent
)

class LayerItem:
    """Represents a visual layer on the canvas"""
    def __init__(self, name: str, layer_type: str):
        self.name = name
        self.layer_type = layer_type  # 'background', 'media', 'text', 'overlay'
        self.rect = QRectF(50, 50, 200, 100)  # x, y, width, height
        self.locked = False
        self.visible = True
        self.opacity = 1.0
        self.rotation = 0.0
        self.color = QColor(255, 255, 255, 128)
        self.text = f"Sample {name}"
        self.font_size = 24
        self.asset_id = None  # Reference to project asset
        
    def contains_point(self, point: QPointF) -> bool:
        """Check if point is inside this layer"""
        return self.rect.contains(point)
        
    def move_to(self, point: QPointF):
        """Move layer to new position"""
        if not self.locked:
            self.rect.moveTo(point)

class VisualCanvas(QWidget):
    """Interactive canvas for visual layer editing"""
    layer_selected = pyqtSignal(object)  # LayerItem
    layer_moved = pyqtSignal(object)     # LayerItem
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enable keyboard events
        
        self.layers = []
        self.selected_layer = None
        self.dragging = False
        self.drag_offset = QPointF()
        self.canvas_size = QSizeF(405, 720)  # 9:16 default
        self.show_grid = True
        self.snap_to_grid = True
        self.grid_size = 25
        
        # Canvas styling
        self.setMinimumSize(int(self.canvas_size.width()), int(self.canvas_size.height()))
        self.setStyleSheet("background-color: #1a1a1a; border: 2px solid #444;")
        
    def set_aspect_ratio(self, content_type: str):
        """Set canvas dimensions based on content type"""
        if content_type.lower() in ["reel", "story", "tutorial"]:
            self.canvas_size = QSizeF(405, 720)  # 9:16
        elif content_type.lower() == "post":
            self.canvas_size = QSizeF(600, 600)  # 1:1
            
        self.setFixedSize(int(self.canvas_size.width()), int(self.canvas_size.height()))
        self.update()
        
    def add_layer(self, layer: LayerItem):
        """Add a new layer to the canvas"""
        self.layers.append(layer)
        self.update()
        
    def remove_layer(self, layer: LayerItem):
        """Remove layer from canvas"""
        if layer in self.layers:
            self.layers.remove(layer)
            if self.selected_layer == layer:
                self.selected_layer = None
            self.update()
            
    def clear_layers(self):
        """Clear all layers"""
        self.layers.clear()
        self.selected_layer = None
        self.update()
        
    def paintEvent(self, event):
        """Paint the canvas and all layers"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw canvas background
        painter.fillRect(self.rect(), QColor(26, 26, 26))
        
        # Draw grid (optional)
        if self.show_grid:
            painter.setPen(QPen(QColor(60, 60, 60), 1, Qt.PenStyle.DotLine))
            for x in range(0, int(self.canvas_size.width()), self.grid_size):
                painter.drawLine(x, 0, x, int(self.canvas_size.height()))
            for y in range(0, int(self.canvas_size.height()), self.grid_size):
                painter.drawLine(0, y, int(self.canvas_size.width()), y)
            
        # Draw layers bottom to top
        for layer in self.layers:
            self._draw_layer(painter, layer)
            
    def _draw_layer(self, painter: QPainter, layer: LayerItem):
        """Draw a single layer"""
        if not layer.visible:
            return
            
        painter.save()
        painter.setOpacity(layer.opacity)
        
        # Highlight selected layer
        if layer == self.selected_layer:
            painter.setPen(QPen(QColor(0, 120, 255), 2))
        else:
            painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
            
        # Draw based on layer type
        if layer.layer_type == 'background':
            painter.fillRect(layer.rect, layer.color)
            painter.drawRect(layer.rect)
        elif layer.layer_type == 'text':
            painter.fillRect(layer.rect, QColor(50, 50, 50, 100))
            painter.drawRect(layer.rect)
            painter.setPen(QPen(QColor(255, 255, 255)))
            font = QFont("Arial", layer.font_size)
            painter.setFont(font)
            painter.drawText(layer.rect, Qt.AlignmentFlag.AlignCenter, layer.text)
        elif layer.layer_type == 'media':
            painter.fillRect(layer.rect, QColor(100, 100, 100))
            painter.drawRect(layer.rect)
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.drawText(layer.rect, Qt.AlignmentFlag.AlignCenter, f"Media\n{layer.name}")
        else:  # overlay
            painter.fillRect(layer.rect, layer.color)
            painter.drawRect(layer.rect)
            
        # Draw resize handles for selected layer
        if layer == self.selected_layer:
            self._draw_handles(painter, layer.rect)
            
        painter.restore()
        
    def _draw_handles(self, painter: QPainter, rect: QRectF):
        """Draw resize handles around selected layer"""
        handle_size = 8
        half_handle = handle_size // 2
        
        # Convert to integers for fillRect
        painter.fillRect(int(rect.topLeft().x() - half_handle), int(rect.topLeft().y() - half_handle), 
                        handle_size, handle_size, QColor(0, 120, 255))
        painter.fillRect(int(rect.topRight().x() - half_handle), int(rect.topRight().y() - half_handle),
                        handle_size, handle_size, QColor(0, 120, 255))
        painter.fillRect(int(rect.bottomLeft().x() - half_handle), int(rect.bottomLeft().y() - half_handle),
                        handle_size, handle_size, QColor(0, 120, 255))
        painter.fillRect(int(rect.bottomRight().x() - half_handle), int(rect.bottomRight().y() - half_handle),
                        handle_size, handle_size, QColor(0, 120, 255))
                        
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for layer selection and dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            point = QPointF(event.position())
            
            # Find topmost layer at click point (reverse order)
            for layer in reversed(self.layers):
                if layer.contains_point(point) and not layer.locked:
                    self.selected_layer = layer
                    self.dragging = True
                    self.drag_offset = point - layer.rect.topLeft()
                    self.layer_selected.emit(layer)
                    self.update()
                    return
                    
            # No layer clicked - deselect
            self.selected_layer = None
            self.layer_selected.emit(None)
            self.update()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for dragging"""
        if self.dragging and self.selected_layer:
            point = QPointF(event.position())
            new_pos = point - self.drag_offset
            
            # Apply grid snapping if enabled
            if self.snap_to_grid:
                new_pos = self.snap_to_grid_pos(new_pos)
                
            self.selected_layer.move_to(new_pos)
            self.layer_moved.emit(self.selected_layer)
            self.update()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accept asset drops"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle asset drop to create new layer"""
        asset_id = event.mimeData().text()
        pos = QPointF(event.position())
        
        # Create new media layer
        layer = LayerItem(f"Asset {asset_id}", "media")
        layer.rect.moveTo(pos)
        layer.asset_id = asset_id
        self.add_layer(layer)
        self.selected_layer = layer
        self.layer_selected.emit(layer)
        event.acceptProposedAction()

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        from PyQt6.QtGui import QKeySequence
        from PyQt6.QtCore import Qt
        
        if event.key() == Qt.Key.Key_Delete and self.selected_layer:
            # Delete selected layer
            self.remove_layer(self.selected_layer)
            self.layer_selected.emit(None)
        elif event.key() == Qt.Key.Key_G:
            # Toggle grid
            self.show_grid = not self.show_grid
            self.update()
        elif event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_D and self.selected_layer:
                # Duplicate layer (Ctrl+D)
                self._duplicate_layer()
            elif event.key() == Qt.Key.Key_A:
                # Select all layers (Ctrl+A)
                if self.layers:
                    self.selected_layer = self.layers[-1]  # Select top layer
                    self.layer_selected.emit(self.selected_layer)
                    self.update()
        elif event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right]:
            # Arrow key nudging
            if self.selected_layer and not self.selected_layer.locked:
                nudge_amount = 10 if event.modifiers() & Qt.KeyboardModifier.ShiftModifier else 1
                dx, dy = 0, 0
                
                if event.key() == Qt.Key.Key_Left:
                    dx = -nudge_amount
                elif event.key() == Qt.Key.Key_Right:
                    dx = nudge_amount
                elif event.key() == Qt.Key.Key_Up:
                    dy = -nudge_amount
                elif event.key() == Qt.Key.Key_Down:
                    dy = nudge_amount
                    
                new_pos = self.selected_layer.rect.topLeft() + QPointF(dx, dy)
                self.selected_layer.move_to(new_pos)
                self.layer_moved.emit(self.selected_layer)
                self.update()
        else:
            super().keyPressEvent(event)
            
    def _duplicate_layer(self):
        """Duplicate the selected layer"""
        if not self.selected_layer:
            return
            
        original = self.selected_layer
        
        # Create new layer with copied properties
        layer = LayerItem(f"{original.name} Copy", original.layer_type)
        layer.rect = QRectF(original.rect.x() + 20, original.rect.y() + 20, 
                          original.rect.width(), original.rect.height())
        layer.visible = original.visible
        layer.opacity = original.opacity
        layer.color = QColor(original.color)
        
        if hasattr(original, 'text'):
            layer.text = original.text
        if hasattr(original, 'font_size'):
            layer.font_size = original.font_size
        if hasattr(original, 'asset_id'):
            layer.asset_id = original.asset_id
            
        self.add_layer(layer)
        self.selected_layer = layer
        self.layer_selected.emit(layer)
        
    def snap_to_grid_pos(self, pos: QPointF) -> QPointF:
        """Snap position to grid if enabled"""
        if not self.snap_to_grid:
            return pos
            
        snapped_x = round(pos.x() / self.grid_size) * self.grid_size
        snapped_y = round(pos.y() / self.grid_size) * self.grid_size
        return QPointF(snapped_x, snapped_y)

class VisualTemplateEditor(QWidget):
    """
    A WYSIWYG editor for creating and managing content templates.
    Inspired by After Effects, with a visual canvas and layer-based controls.
    """
    template_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.current_content_type = "reel"
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Set up the main UI components."""
        main_layout = QHBoxLayout(self)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        # --- Center Panel: Canvas and Controls ---
        center_panel = QFrame()
        center_layout = QVBoxLayout(center_panel)
        
        # Content Type Selector
        selector_frame = QFrame()
        selector_layout = QHBoxLayout(selector_frame)
        selector_layout.addWidget(QLabel("Content Type:"))
        self.content_type_selector = QComboBox()
        self.content_type_selector.addItems(["Reel", "Story", "Post", "Tutorial"])
        selector_layout.addWidget(self.content_type_selector)
        selector_layout.addStretch()
        center_layout.addWidget(selector_frame)

        # Visual Canvas
        canvas_wrapper = QFrame()
        canvas_wrapper.setStyleSheet("background-color: #2d2d2d; border: 1px solid #555;")
        canvas_layout = QVBoxLayout(canvas_wrapper)
        canvas_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.canvas = VisualCanvas()
        canvas_layout.addWidget(self.canvas)
        center_layout.addWidget(canvas_wrapper)

        # Timeline
        self.timeline_widget = QFrame()
        self.timeline_widget.setFixedHeight(120)
        self.timeline_widget.setStyleSheet("background-color: #333; border: 1px solid #555;")
        timeline_layout = QVBoxLayout(self.timeline_widget)
        timeline_label = QLabel("Timeline")
        timeline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline_layout.addWidget(timeline_label)
        center_layout.addWidget(self.timeline_widget)
        main_splitter.addWidget(center_panel)

        # --- Right Panel: Layers and Properties ---
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_panel.setMinimumWidth(320)
        right_panel.setStyleSheet("background-color: #2a2a2a;")

        # Layer Management
        self.layer_box = QGroupBox("Layers")
        layer_layout = QVBoxLayout(self.layer_box)
        # Layer controls
        layer_controls = QFrame()
        layer_controls_layout = QHBoxLayout(layer_controls)
        self.add_text_btn = QPushButton("+ Text")
        self.add_shape_btn = QPushButton("+ Shape")
        self.delete_layer_btn = QPushButton("Delete")
        layer_controls_layout.addWidget(self.add_text_btn)
        layer_controls_layout.addWidget(self.add_shape_btn)
        layer_controls_layout.addWidget(self.delete_layer_btn)
        layer_layout.addWidget(layer_controls)
        self.layer_tree = QTreeWidget()
        self.layer_tree.setHeaderLabels(["Layer", "👁", "🔒"])
        layer_layout.addWidget(self.layer_tree)
        right_layout.addWidget(self.layer_box)

        # Property Editor
        self.property_box = QGroupBox("Properties")
        property_layout = QVBoxLayout(self.property_box)
        self.property_widget = QWidget()
        self.property_layout = QFormLayout(self.property_widget)
        property_layout.addWidget(self.property_widget)
        right_layout.addWidget(self.property_box)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([700, 320])

    def _setup_connections(self):
        """Connect signals and slots."""
        self.content_type_selector.currentTextChanged.connect(self._on_content_type_changed)
        self.canvas.layer_selected.connect(self._on_layer_selected)
        self.canvas.layer_moved.connect(self._on_layer_moved)
        self.layer_tree.itemClicked.connect(self._on_layer_tree_clicked)
        self.add_text_btn.clicked.connect(self._add_text_layer)
        self.add_shape_btn.clicked.connect(self._add_shape_layer)
        self.delete_layer_btn.clicked.connect(self._delete_selected_layer)

    def set_project(self, project):
        """Load project data into the editor."""
        self.project = project
        from core.content_generation import ContentGenerationManager
        if self.project and not hasattr(self.project, 'content_generation_manager'):
            self.project.content_generation_manager = ContentGenerationManager()
        self._load_template_for_current_type()

    def _on_content_type_changed(self, content_type: str):
        """Handle switching between content types."""
        self.current_content_type = content_type.lower()
        
        # Adjust canvas aspect ratio and timeline visibility
        self.canvas.set_aspect_ratio(content_type)
        
        if self.current_content_type in ["reel", "story", "tutorial"]:
            self.timeline_widget.setVisible(True)
        elif self.current_content_type == "post":
            self.timeline_widget.setVisible(False)
        
        self._load_template_for_current_type()

    def _load_template_for_current_type(self):
        """Load the layers and properties for the selected content type."""
        if not self.project:
            return
            
        # Clear existing layers
        self.canvas.clear_layers()
        self._refresh_layer_tree()
        
        # Add default layers based on content type
        if self.current_content_type in ["reel", "story", "tutorial"]:
            # Video content layers
            bg_layer = LayerItem("Background", "background")
            bg_layer.rect = QRectF(0, 0, 405, 720)
            bg_layer.color = QColor(20, 20, 20)
            self.canvas.add_layer(bg_layer)
            
            media_layer = LayerItem("Main Video", "media")
            media_layer.rect = QRectF(50, 100, 305, 400)
            self.canvas.add_layer(media_layer)
            
            subtitle_layer = LayerItem("Subtitles", "text")
            subtitle_layer.rect = QRectF(50, 550, 305, 100)
            subtitle_layer.text = "Sample subtitle text"
            self.canvas.add_layer(subtitle_layer)
            
        elif self.current_content_type == "post":
            # Static post layers
            bg_layer = LayerItem("Background", "background")
            bg_layer.rect = QRectF(0, 0, 600, 600)
            bg_layer.color = QColor(240, 240, 240)
            self.canvas.add_layer(bg_layer)
            
            media_layer = LayerItem("Main Image", "media")
            media_layer.rect = QRectF(100, 100, 400, 300)
            self.canvas.add_layer(media_layer)
            
            text_layer = LayerItem("Title Text", "text")
            text_layer.rect = QRectF(100, 450, 400, 100)
            text_layer.text = "Post Title"
            text_layer.font_size = 32
            self.canvas.add_layer(text_layer)
            
        self._refresh_layer_tree()
        print(f"Loaded {len(self.canvas.layers)} layers for {self.current_content_type}")

    def _refresh_layer_tree(self):
        """Refresh the layer tree widget"""
        self.layer_tree.clear()
        
        for i, layer in enumerate(reversed(self.canvas.layers)):  # Top to bottom
            item = QTreeWidgetItem(self.layer_tree)
            item.setText(0, layer.name)
            item.setData(0, Qt.ItemDataRole.UserRole, layer)
            
            # Visibility checkbox
            visibility_item = QTreeWidgetItem()
            visibility_item.setText(1, "👁" if layer.visible else "👁‍🗨")
            item.addChild(visibility_item)
            
            # Lock checkbox  
            lock_item = QTreeWidgetItem()
            lock_item.setText(2, "🔒" if layer.locked else "🔓")
            item.addChild(lock_item)
            
        self.layer_tree.expandAll()

    def _on_layer_selected(self, layer: LayerItem):
        """Handle layer selection from canvas"""
        self._update_properties_for_layer(layer)
        
        # Select in tree
        for i in range(self.layer_tree.topLevelItemCount()):
            item = self.layer_tree.topLevelItem(i)
            tree_layer = item.data(0, Qt.ItemDataRole.UserRole)
            if tree_layer == layer:
                self.layer_tree.setCurrentItem(item)
                break
                
    def _on_layer_moved(self, layer: LayerItem):
        """Handle layer movement"""
        self.template_changed.emit()
        
    def _on_layer_tree_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle layer tree clicks"""
        layer = item.data(0, Qt.ItemDataRole.UserRole)
        if layer:
            if column == 1:  # Visibility toggle
                layer.visible = not layer.visible
                self.canvas.update()
                self._refresh_layer_tree()
            elif column == 2:  # Lock toggle
                layer.locked = not layer.locked
                self._refresh_layer_tree()
            else:  # Select layer
                self.canvas.selected_layer = layer
                self.canvas.update()
                self._update_properties_for_layer(layer)

    def _add_text_layer(self):
        """Add a new text layer"""
        layer = LayerItem(f"Text {len(self.canvas.layers) + 1}", "text")
        layer.rect = QRectF(100, 100, 200, 50)
        layer.text = "New Text Layer"
        self.canvas.add_layer(layer)
        self._refresh_layer_tree()
        self.template_changed.emit()
        
    def _add_shape_layer(self):
        """Add a new shape/overlay layer"""
        layer = LayerItem(f"Shape {len(self.canvas.layers) + 1}", "overlay")
        layer.rect = QRectF(150, 150, 100, 100)
        layer.color = QColor(255, 0, 0, 128)
        self.canvas.add_layer(layer)
        self._refresh_layer_tree()
        self.template_changed.emit()
        
    def _delete_selected_layer(self):
        """Delete the currently selected layer"""
        if self.canvas.selected_layer:
            self.canvas.remove_layer(self.canvas.selected_layer)
            self._refresh_layer_tree()
            self._update_properties_for_layer(None)
            self.template_changed.emit()

    def _update_properties_for_layer(self, layer: LayerItem):
        """Update the property editor for the selected layer"""
        # Clear existing properties
        while self.property_layout.count():
            child = self.property_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        if not layer:
            self.property_layout.addRow(QLabel("No layer selected"))
            return
            
        # Layer name
        name_edit = QLineEdit(layer.name)
        name_edit.textChanged.connect(lambda text: setattr(layer, 'name', text))
        name_edit.textChanged.connect(lambda: self._refresh_layer_tree())
        self.property_layout.addRow("Name:", name_edit)
        
        # Position
        x_spin = QDoubleSpinBox()
        x_spin.setRange(-1000, 2000)
        x_spin.setValue(layer.rect.x())
        x_spin.valueChanged.connect(lambda v: self._update_layer_x(layer, v))
        
        y_spin = QDoubleSpinBox()
        y_spin.setRange(-1000, 2000)  
        y_spin.setValue(layer.rect.y())
        y_spin.valueChanged.connect(lambda v: self._update_layer_y(layer, v))
        
        self.property_layout.addRow("X:", x_spin)
        self.property_layout.addRow("Y:", y_spin)
        
        # Size
        w_spin = QDoubleSpinBox()
        w_spin.setRange(1, 2000)
        w_spin.setValue(layer.rect.width())
        w_spin.valueChanged.connect(lambda v: self._update_layer_width(layer, v))
        
        h_spin = QDoubleSpinBox()
        h_spin.setRange(1, 2000)
        h_spin.setValue(layer.rect.height())
        h_spin.valueChanged.connect(lambda v: self._update_layer_height(layer, v))
        
        self.property_layout.addRow("Width:", w_spin)
        self.property_layout.addRow("Height:", h_spin)
        
        # Opacity
        opacity_slider = QSlider(Qt.Orientation.Horizontal)
        opacity_slider.setRange(0, 100)
        opacity_slider.setValue(int(layer.opacity * 100))
        opacity_slider.valueChanged.connect(lambda v: self._update_layer_opacity(layer, v/100))
        self.property_layout.addRow("Opacity:", opacity_slider)
        
        # Layer-specific properties
        if layer.layer_type == "text":
            text_edit = QLineEdit(layer.text)
            text_edit.textChanged.connect(lambda text: setattr(layer, 'text', text))
            text_edit.textChanged.connect(lambda: self.canvas.update())
            text_edit.textChanged.connect(lambda: self.template_changed.emit())
            self.property_layout.addRow("Text:", text_edit)
            
            font_size_spin = QSpinBox()
            font_size_spin.setRange(8, 200)
            font_size_spin.setValue(layer.font_size)
            font_size_spin.valueChanged.connect(lambda v: setattr(layer, 'font_size', v))
            font_size_spin.valueChanged.connect(lambda: self.canvas.update())
            font_size_spin.valueChanged.connect(lambda: self.template_changed.emit())
            self.property_layout.addRow("Font Size:", font_size_spin)
            
            # Text color
            text_color_btn = QPushButton()
            text_color = getattr(layer, 'text_color', QColor(255, 255, 255))
            text_color_btn.setStyleSheet(f"background-color: {text_color.name()}; border: 1px solid #ccc;")
            text_color_btn.clicked.connect(lambda: self._choose_text_color(layer, text_color_btn))
            self.property_layout.addRow("Text Color:", text_color_btn)
            
        elif layer.layer_type in ["background", "overlay"]:
            color_btn = QPushButton()
            color_btn.setStyleSheet(f"background-color: {layer.color.name()}; border: 1px solid #ccc;")
            color_btn.clicked.connect(lambda: self._choose_layer_color(layer, color_btn))
            self.property_layout.addRow("Color:", color_btn)
            
        elif layer.layer_type == "media":
            # Media-specific properties
            media_label = QLabel("📷 Media Layer")
            media_label.setStyleSheet("font-weight: bold; color: #0078d4;")
            self.property_layout.addRow("Type:", media_label)
            
            # Placeholder for asset selection
            asset_btn = QPushButton("Choose Asset...")
            asset_btn.clicked.connect(lambda: self._choose_media_asset(layer))
            self.property_layout.addRow("Asset:", asset_btn)
            
        # Layer visibility and lock controls
        visibility_checkbox = QCheckBox("Visible")
        visibility_checkbox.setChecked(layer.visible)
        visibility_checkbox.toggled.connect(lambda checked: setattr(layer, 'visible', checked))
        visibility_checkbox.toggled.connect(lambda: self.canvas.update())
        visibility_checkbox.toggled.connect(lambda: self._refresh_layer_tree())
        visibility_checkbox.toggled.connect(lambda: self.template_changed.emit())
        self.property_layout.addRow("", visibility_checkbox)
        
        lock_checkbox = QCheckBox("Locked")
        lock_checkbox.setChecked(layer.locked)
        lock_checkbox.toggled.connect(lambda checked: setattr(layer, 'locked', checked))
        lock_checkbox.toggled.connect(lambda: self._refresh_layer_tree())
        lock_checkbox.toggled.connect(lambda: self.template_changed.emit())
        self.property_layout.addRow("", lock_checkbox)
        
    def _update_layer_x(self, layer, value):
        layer.rect.moveLeft(value)
        self.canvas.update()
        self.template_changed.emit()
        
    def _update_layer_y(self, layer, value):
        layer.rect.moveTop(value)
        self.canvas.update()
        self.template_changed.emit()
        
    def _update_layer_width(self, layer, value):
        layer.rect.setWidth(value)
        self.canvas.update()
        self.template_changed.emit()
        
    def _update_layer_height(self, layer, value):
        layer.rect.setHeight(value)
        self.canvas.update()
        self.template_changed.emit()
        
    def _update_layer_opacity(self, layer, value):
        layer.opacity = value
        self.canvas.update()
        self.template_changed.emit()
        
    def _choose_layer_color(self, layer, button):
        """Open color dialog for layer"""
        color = QColorDialog.getColor(layer.color, self)
        if color.isValid():
            layer.color = color
            button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            self.canvas.update()
            self.template_changed.emit()
            
    def _choose_text_color(self, layer, button):
        """Open color dialog for text color"""
        current_color = getattr(layer, 'text_color', QColor(255, 255, 255))
        color = QColorDialog.getColor(current_color, self)
        if color.isValid():
            layer.text_color = color
            button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            self.canvas.update()
            self.template_changed.emit()
            
    def _choose_media_asset(self, layer):
        """Choose media asset for layer"""
        # TODO: Integrate with asset management system
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Choose Media Asset",
            "",
            "Media Files (*.mp4 *.mov *.avi *.jpg *.jpeg *.png *.gif)"
        )
        
        if file_path:
            layer.asset_id = file_path
            layer.name = f"Media: {file_path.split('/')[-1]}"
            self._refresh_layer_tree()
            self.template_changed.emit()

    def save_template_to_project(self):
        """Save current visual template to project's content generation manager"""
        if not self.project or not hasattr(self.project, 'content_generation_manager'):
            return
            
        # Convert visual layers to content generation template
        from core.content_generation import ContentTemplate, ConfigParameter, ConfigMode
        
        template = self.project.content_generation_manager.get_content_template(self.current_content_type)
        
        # Update template based on visual layers
        for layer in self.canvas.layers:
            if layer.layer_type == "text" and "subtitle" in layer.name.lower():
                # Update subtitle template
                template.subtitle.font_size.value = f"{layer.font_size}px"
                template.subtitle.position.value = self._get_position_name(layer.rect)
                if hasattr(layer, 'text_color') and layer.text_color != QColor(255, 255, 255):
                    template.subtitle.color.value = layer.text_color.name()
                    
            elif layer.layer_type == "background":
                # Update overlay template for background
                template.overlay.background_style.value = layer.color.name()
                
            elif layer.layer_type == "overlay":
                # Update overlay elements
                template.overlay.overlay_elements.value = "custom"
                template.overlay.color_scheme.value = layer.color.name()
        
        # Save timing information based on content type
        if self.current_content_type == "reel":
            template.timing.duration.value = "15-30s"
        elif self.current_content_type == "story":
            template.timing.duration.value = "5-15s" 
        elif self.current_content_type == "post":
            template.timing.duration.value = "static"
        elif self.current_content_type == "tutorial":
            template.timing.duration.value = "60-120s"
            
        # Store visual layer data as custom parameters
        layer_data = []
        for layer in self.canvas.layers:
            layer_dict = {
                "name": layer.name,
                "type": layer.layer_type,
                "rect": [layer.rect.x(), layer.rect.y(), layer.rect.width(), layer.rect.height()],
                "visible": layer.visible,
                "locked": layer.locked,
                "opacity": layer.opacity,
                "color": layer.color.name() if hasattr(layer, 'color') else None,
                "text": getattr(layer, 'text', None),
                "font_size": getattr(layer, 'font_size', None),
                "text_color": getattr(layer, 'text_color', QColor(255, 255, 255)).name() if hasattr(layer, 'text_color') else None
            }
            layer_data.append(layer_dict)
            
        template.custom_parameters["visual_layers"] = ConfigParameter(
            value=layer_data,
            mode=ConfigMode.FIXED,
            description="Visual layer configuration from template editor"
        )
        
        print(f"Template saved for {self.current_content_type}")
        
    def load_template_from_project(self):
        """Load visual template from project's content generation manager"""
        if not self.project or not hasattr(self.project, 'content_generation_manager'):
            return
            
        template = self.project.content_generation_manager.get_content_template(self.current_content_type)
        
        # Check if we have saved visual layers
        if "visual_layers" in template.custom_parameters:
            layer_data = template.custom_parameters["visual_layers"].value
            
            # Clear current layers
            self.canvas.clear_layers()
            
            # Recreate layers from saved data
            for layer_dict in layer_data:
                layer = LayerItem(layer_dict["name"], layer_dict["type"])
                layer.rect = QRectF(*layer_dict["rect"])
                layer.visible = layer_dict["visible"]
                layer.locked = layer_dict["locked"]
                layer.opacity = layer_dict["opacity"]
                
                if layer_dict["color"]:
                    layer.color = QColor(layer_dict["color"])
                if layer_dict["text"]:
                    layer.text = layer_dict["text"]
                if layer_dict["font_size"]:
                    layer.font_size = layer_dict["font_size"]
                if layer_dict["text_color"]:
                    layer.text_color = QColor(layer_dict["text_color"])
                    
                self.canvas.add_layer(layer)
                
            self._refresh_layer_tree()
            print(f"Template loaded for {self.current_content_type}")
        else:
            # Load default template for content type
            self._load_template_for_current_type()
            
    def _get_position_name(self, rect: QRectF) -> str:
        """Convert rect position to semantic name"""
        canvas_height = self.canvas.canvas_size.height()
        y_center = rect.center().y()
        
        if y_center < canvas_height * 0.33:
            return "top"
        elif y_center > canvas_height * 0.67:
            return "bottom"
        else:
            return "center"
            
    def export_template_config(self) -> dict:
        """Export current template as configuration dictionary"""
        if not self.project or not hasattr(self.project, 'content_generation_manager'):
            return {}
            
        # Save current template first
        self.save_template_to_project()
        
        # Get resolved configuration
        manager = self.project.content_generation_manager
        config = manager.resolve_config(self.current_content_type)
        
        # Add visual metadata
        config["content_type"] = self.current_content_type
        config["canvas_size"] = {
            "width": self.canvas.canvas_size.width(),
            "height": self.canvas.canvas_size.height()
        }
        config["layer_count"] = len(self.canvas.layers)
        
        return config
        
    def generate_ai_prompt(self) -> str:
        """Generate AI prompt for current template configuration"""
        if not self.project or not hasattr(self.project, 'content_generation_manager'):
            return ""
            
        self.save_template_to_project()
        manager = self.project.content_generation_manager
        
        base_prompt = f"Create {self.current_content_type} content using the following template specifications:"
        return manager.generate_ai_prompt(self.current_content_type, base_prompt=base_prompt)
