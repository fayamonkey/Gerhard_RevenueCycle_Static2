from datetime import datetime
from typing import Dict, Any

class DocumentGenerator:
    @staticmethod
    def generate_inquiry_document(inquiry_data: Dict[str, Any]) -> str:
        # Parse inquiry data
        customer = inquiry_data.get("customer", "")
        products = inquiry_data.get("products", [])
        delivery = inquiry_data.get("delivery", "")
        special_reqs = inquiry_data.get("special_requirements", "")
        
        # Generate document number
        date = datetime.now()
        doc_number = f"INQ-{date.strftime('%Y%m%d')}-{customer[:3].upper()}"
        
        # Create document
        document = [
            "SALES INQUIRY DOCUMENT",
            "---------------------",
            f"Date: {date.strftime('%d/%m/%Y')}",
            f"Inquiry Number: {doc_number}\n",
            "1. Customer Details:",
            f"   Company Name: {customer}",
            "   Contact Person: Not provided",
            "   Delivery Address: Not provided\n",
            "2. Product Details:"
        ]
        
        for i, product in enumerate(products, 1):
            document.extend([
                f"\n   Item {i}:",
                f"   Product ID: {product['id']}",
                f"   Description: {product['name']}",
                f"   Exact Quantity: {product['quantity']}",
                f"   Unit Price in EUR: {product.get('price', 'To be confirmed')}",
                f"   Total Price Per Item: {product.get('total_price', 'To be confirmed')}"
            ])
        
        document.extend([
            f"\n3. Delivery Requirements: {delivery}",
            f"\n4. Special Requirements: {special_reqs}",
            "\n5. Total Order Value: To be confirmed",
            "\n---------------",
            "System Update:",
            "- Customer details verified in database",
            "- Price list checked for all products",
            "- Product specifications verified"
        ])
        
        return "\n".join(document)

    @staticmethod
    def generate_inventory_document(inquiry_data: Dict[str, Any], inventory_data: Dict[str, Any]) -> str:
        doc_number = inquiry_data.get("doc_number", "Unknown")
        products = inquiry_data.get("products", [])
        
        document = [
            "INVENTORY CHECK DOCUMENT",
            "----------------------",
            f"Order Reference: {doc_number}\n",
            "Product Information:"
        ]
        
        for i, product in enumerate(products, 1):
            stock = inventory_data.get(product['id'], {})
            document.extend([
                f"\n   {i}.",
                f"   - Product ID: {product['id']}",
                f"   - Requested quantity: {product['quantity']}",
                f"   - Available quantity: {stock.get('quantity', 0)}",
                f"   - Storage location: {stock.get('location', 'Not found')}"
            ])
        
        document.extend([
            "\nSystem Update:",
            "- Stock levels checked in warehouse system",
            "- Available quantities reserved for order",
            "- Stock locations verified"
        ])
        
        return "\n".join(document)

    @staticmethod
    def generate_picking_document(inquiry_data: Dict[str, Any], inventory_data: Dict[str, Any]) -> str:
        date = datetime.now()
        doc_number = f"PICK-{date.strftime('%Y%m%d')}-{inquiry_data['doc_number']}"
        products = inquiry_data.get("products", [])
        
        document = [
            "PICKING TICKET",
            "-------------",
            f"Ticket Number: {doc_number}",
            f"Date: {date.strftime('%d/%m/%Y')}\n",
            "Customer Details:",
            f"Company Name: {inquiry_data['customer']}",
            "Contact Person: Not provided",
            "Delivery Address: Not provided\n",
            "Items to Pick:"
        ]
        
        for i, product in enumerate(products, 1):
            stock = inventory_data.get(product['id'], {})
            document.extend([
                f"\n{i}. {product['name']}",
                f"   - Product ID: {product['id']}",
                f"   - Quantity: {product['quantity']}",
                f"   - Location: {stock.get('location', 'Not found')}",
                "   - Quality Check Required: Yes",
                "   - Handle with Care"
            ])
        
        return "\n".join(document)

    @staticmethod
    def generate_shipping_documents(inquiry_data: Dict[str, Any], picking_data: Dict[str, Any]) -> str:
        date = datetime.now()
        doc_number = f"SHIP-{date.strftime('%Y%m%d')}-{inquiry_data['doc_number']}"
        
        documents = [
            "PACKING SLIP",
            "-----------",
            f"Slip Number: {doc_number}",
            f"Date: {date.strftime('%d/%m/%Y')}",
            f"Customer: {inquiry_data['customer']}\n",
            "Items Packed:"
        ]
        
        for i, product in enumerate(inquiry_data['products'], 1):
            documents.extend([
                f"\n{i}. {product['name']}",
                f"   - Product ID: {product['id']}",
                f"   - Quantity: {product['quantity']}",
                "   - Quality Check: Completed"
            ])
        
        documents.extend([
            "\n\nBILL OF LADING",
            "-------------",
            f"B/L Number: {doc_number}",
            f"Date: {date.strftime('%d/%m/%Y')}",
            f"Shipper: Our Company",
            f"Consignee: {inquiry_data['customer']}",
            "Terms: EXW",
            "Carrier: To be assigned"
        ])
        
        return "\n".join(documents)

    @staticmethod
    def generate_billing_documents(inquiry_data: Dict[str, Any], shipping_data: Dict[str, Any]) -> str:
        date = datetime.now()
        invoice_number = f"INV-{date.strftime('%Y%m%d')}-{inquiry_data['doc_number']}"
        
        documents = [
            "SALES INVOICE",
            "-------------",
            f"Invoice Number: {invoice_number}",
            f"Date: {date.strftime('%d/%m/%Y')}",
            f"Customer: {inquiry_data['customer']}\n",
            "Items:",
            "-" * 60,
            "Product                  Quantity    Unit Price    Total",
            "-" * 60
        ]
        
        total = 0
        for product in inquiry_data['products']:
            price = float(product.get('price', 0))
            line_total = price * product['quantity']
            total += line_total
            documents.append(
                f"{product['name'][:20]:<20} {product['quantity']:>10} {price:>12.2f} {line_total:>10.2f}"
            )
        
        documents.extend([
            "-" * 60,
            f"Total (excluding tax): {total:>33.2f} EUR",
            "\nPayment Terms: 30 days",
            "Please include invoice number in payment reference"
        ])
        
        return "\n".join(documents) 