from PySide6.QtWidgets import QTableWidgetItem

class TableHelper:
    @staticmethod
    def populate_table(table_widget, results):
        if not results:
            return

        table_widget.setRowCount(len(results))
        table_widget.setColumnCount(len(results[0]))

        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(row_idx, col_idx, item)
