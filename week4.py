import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, 
                             QLineEdit, QPushButton, QVBoxLayout, 
                             QListWidget, QMessageBox)
from PyQt5.QtCore import Qt

class TokoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cart = []

    def initUI(self):
        self.setWindowTitle('Toko Onlen')
        self.resize(500, 500)
        layout = QVBoxLayout()

        # Product Selection
        self.productLabel = QLabel('Select Product:')
        self.productComboBox = QComboBox()
        self.productComboBox.addItems([
            '<>', 'Bimoli (Rp 20,000)', 'Kecap ABC (Rp 7,000)', 
            'Indomie Goreng (Rp 3,500)', 'Beras Enak 5kg (Rp 65,000)', 
            'Susu Dancow 400g (Rp 45,000)', 'Gula Pasir 1kg (Rp 14,000)', 
            'Teh Kotak (Rp 5,000)'
        ])

        # Quantity Input
        self.quantityLabel = QLabel('Quantity:')
        self.quantityInput = QLineEdit()

        # Discount Selection
        self.discountLabel = QLabel('Select Discount (%):')
        self.discountComboBox = QComboBox()
        self.discountComboBox.addItems(['0%', '5%', '10%', '15%', '20%', '25%'])

        # Buttons
        self.addButton = QPushButton('Add to Cart')
        self.addButton.clicked.connect(self.addToCart)
        self.clearButton = QPushButton('Clear')
        self.clearButton.clicked.connect(self.clearFields)

        # Cart Display
        self.cartDisplay = QListWidget()
        self.totalLabel = QLabel('Total: Rp. 0')

        # Layout Arrangement
        layout.addWidget(self.productLabel)
        layout.addWidget(self.productComboBox)
        layout.addWidget(self.quantityLabel)
        layout.addWidget(self.quantityInput)
        layout.addWidget(self.discountLabel)
        layout.addWidget(self.discountComboBox)
        layout.addWidget(self.addButton)
        layout.addWidget(self.clearButton)
        layout.addWidget(self.cartDisplay)
        layout.addWidget(self.totalLabel)

        self.setLayout(layout)

    def format_currency(self, value):
        return f'Rp. {value:,.0f}'.replace(',', '.')

    def addToCart(self):
        product = self.productComboBox.currentText()
        quantity = self.quantityInput.text()
        discount = int(self.discountComboBox.currentText().strip('%'))

        if product == '<>' or not quantity.isdigit() or int(quantity) <= 0:
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid product and quantity.')
            return
        
        # Extract price
        price = int(product.split('Rp ')[1].replace(',', '').strip(')'))
        total_price = price * int(quantity)
        discounted_price = total_price - (total_price * discount / 100)

        # Update cart display
        cart_item = f"{product} - {quantity} x Rp. {price:,} (disc {discount}%)"
        self.cartDisplay.addItem(cart_item + f" = {self.format_currency(discounted_price)}")
        self.updateTotal()

    def clearFields(self):
        self.productComboBox.setCurrentIndex(0)
        self.quantityInput.clear()
        self.discountComboBox.setCurrentIndex(0)
        self.cartDisplay.clear()
        self.totalLabel.setText('Total: Rp. 0')

    def updateTotal(self):
        total = 0
        for index in range(self.cartDisplay.count()):
            item_text = self.cartDisplay.item(index).text()
            try:
                total_value = item_text.split('= ')[1].replace('Rp. ', '').replace('.', '').strip()
                total += float(total_value)
            except (ValueError, IndexError):
                continue  # Skip jika parsing error atau index tidak ditemukan
        
        self.totalLabel.setText(f'Total: {self.format_currency(total)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    TokoApp = TokoApp()
    TokoApp.show()
    sys.exit(app.exec_())
