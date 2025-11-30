from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import QSize, QTimer


class MyWidget_HistoryList(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setUniformItemSizes(False)  # different height for rows
        self._relayout = False  # flag

    def _adjust_item_size(self, item: QListWidgetItem):

        widget = self.itemWidget(item)

        if widget is None:
            return

        # CURRENT WIDTH LIST = NEW WIDTH for ITEM LIST
        new_width = self.viewport().width()
        widget.setFixedWidth(new_width)

        layout = widget.layout()

        # HEIGHT for NEW WIDTH
        if layout is not None and layout.hasHeightForWidth():
            new_height = layout.heightForWidth(new_width)
        else:
            if layout is not None:
                # Delete layout cache.
                layout.invalidate()
                # New layout cache.
                layout.activate()
            # Update size for widget.
            widget.updateGeometry()
            new_height = widget.sizeHint().height()

        # UPDATE SIZE for ITEM LIST
        item.setSizeHint(
            QSize(new_width, new_height + 25)
        )  # margin-bottom: 25px in style

    def _do_relayout(self):

        self._relayout = False

        for item in range(self.count()):
            self._adjust_item_size(self.item(item))

        self.doItemsLayout()

    def schedule_relayout(self):

        if self._relayout == True:
            return

        self._relayout = True
        QTimer.singleShot(0, self._do_relayout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.schedule_relayout()

    def setItemWidget(self, item: QListWidgetItem, widget):
        super().setItemWidget(item, widget)
        self.schedule_relayout()
